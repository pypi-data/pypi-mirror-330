from .base import JestitBase
from django.db import models as dm
from jestit.helpers import logit
logger = logit.get_logger("requests", "requests.log")


class JestitLog(dm.Model, JestitBase):
    created = dm.DateTimeField(auto_now_add=True, db_index=True)
    kind = dm.CharField(max_length=200, default=None, null=True, db_index=True)
    method = dm.CharField(max_length=200, default=None, null=True)
    path = dm.TextField(default=None, null=True, db_index=True)
    ip = dm.CharField(max_length=32, default=None, null=True, db_index=True)
    uid = dm.IntegerField(default=0, db_index=True)
    log = dm.TextField(default=None, null=True)
    model_name = dm.TextField(default=None, null=True, db_index=True)
    model_id = dm.IntegerField(default=0, db_index=True)

    @classmethod
    def logit(cls, request, log, kind="log", model_name=None, model_id=0):
        if isinstance(log, bytes):
            log = log.decode("utf-8")
        uid = request.user.id if request.user.is_authenticated else 0
        path = request.get_full_path()
        ip_address = request.META.get('REMOTE_ADDR', None)
        # logger.info(f"Logging {kind}: path={path}, ip={ip_address}, uid={uid}, model={model_name}.{model_id}\n{log}")
        return cls.objects.create(
            kind=kind,
            method=request.method,
            path=path,
            ip=ip_address,
            uid=uid,
            log=log,
            model_name=model_name,
            model_id=model_id
        )
