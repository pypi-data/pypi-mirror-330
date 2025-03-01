# Django-Jestit Documentation

Django-Jestit is a streamlined set of Django applications and a lightweight REST framework designed to simplify user authentication, authorization, and efficient API testing. This documentation provides descriptions and examples to help you get started quickly.

## Why Django-Jestit?

We built Django-Jestit to address the complexity and overhead of existing REST frameworks. Many frameworks are feature-heavy, making them cumbersome for projects that require simplicity, speed, and robust security.

## Key Differentiators

- **Lightweight Framework:** Django-Jestit is minimalistic, providing an easy way to add REST APIs to your Django models without unnecessary complexity.

- **Built-in Security:** Security is integral to Django-Jestit. We offer an alternative to Django's built-in permissions system, automatically protecting your REST APIs and data.

- **Robust Object-Level Permission System:** Unlike Django's native model-level permissions, Django-Jestit provides a simple yet robust permission system at the object level. This allows fine-grained control, enabling permissions to be applied to individual objects and extended to both user and group levels.

- **Effortless Integration:** Adding REST endpoints to your models is straightforward, enabling rapid development without compromising security or performance.

With Django-Jestit, you get a simple, efficient framework with powerful security features designed for developers who value speed and control.
## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Authit - Authentication and Authorization](#authit)
   - [JWT Authentication Middleware](#jwt-authentication)
   - [Models](#models)
   - [REST API](#authit-rest-api)
4. [Jestit - REST framework](#jestit)
   - [URL Decorators](#url-decorators)
   - [GraphSerializer](#graphserializer)
5. [Testit - Testing Suite](#testit)
   - [Writing Tests](#writing-tests)
   - [Running Tests](#running-tests)
6. [Taskit - Task Runner](#taskit)
7. [Utilities](#utilities)

## Overview

Django-Jestit is a collection of Django-based applications focused on authentication, task management, and testing. These tools are built to enhance development efficiency by providing utilities for common requirements such as user management, token-based authentication, and automated testing.

## Installation

```bash
pip install django-jestit
```

## Authit

The **Authit** application manages authentication and authorization using JSON Web Tokens (JWT). It includes models to represent users and groups, and middleware to handle JWT authentication.

### JWT Authentication

The `JWTAuthenticationMiddleware` is a critical component that checks the validity of JWT tokens accompanying HTTP requests.

**Example: Middleware Setup**

To use the JWT middleware, add it to the middleware list in your Django settings:

```python
MIDDLEWARE = [
    # other middleware classes
    'authit.middleware.jwt.JWTAuthenticationMiddleware',
]
```

The middleware checks for JWT tokens in the `Authorization` header of requests and validates them. If validation fails, it returns an appropriate JSON response with an error message.

### Models

Authit's models define the structure of users and groups in the system.

- **User**: The primary model for user management with fields like `username`, `email`, `password`, and `permissions`.
- **Group**: Represents groups that users can belong to, with a hierarchical structure.
- **GroupMember**: Manages the membership of users in groups, along with specific group permissions.

### Authit REST API

Authit provides RESTful endpoints for managing users and groups. These endpoints leverage Django's request handling framework and custom decorators for URL routing.

**Example: User REST API**

Users can be managed through RESTful operations. Here’s how you can interact with the user API:

- **Create a User**: POST to `/api/authit/user` with user data.
- **Retrieve Users**: GET from `/api/authit/user` to fetch all users or `/api/authit/user/<int:id>` for a specific user.
- **Update a User**: PUT to `/api/authit/user/<int:id>` with updated user data.
- **Delete a User**: DELETE from `/api/authit/user/<int:id>`.

## Jestit

Jestit offers a lightweight framework for building REST APIs in Django. It features decorators for automatic URL mapping and serialization tools for data transfer.

### URL Decorators

The `@jd.URL` and other suffix decorators like `@jd.GET`, `@jd.POST`, etc., register view functions with specific URL patterns and HTTP methods.

**Example: Registering a URL**

```python
from jestit.decorators import URL, GET

@URL('myresource')
@GET
def my_view_function(request):
    # handle GET request for /myresource
    return JsonResponse({'message': 'Hello, Jestit!'})
```

### GraphSerializer

`GraphSerializer` is a custom serialization mechanism that uses model-defined graphs for data conversion.

**Example: Using GraphSerializer**

```python
serializer = GraphSerializer(instance=my_model_instance, graph='default')
json_data = serializer.to_json()
```

This approach allows customization of serialized output by defining graphs in your model's `RestMeta` class.

## Testit

Testit is a testing suite designed to run unit tests for your Django applications efficiently.

### Writing Tests

Testit facilitates organizing tests in modules, with decorators to mark and describe each test.

**Example: Using the Test Decorator**

```python
from testit.helpers import unit_test

@unit_test("Verifying addition logic")
def test_addition():
    assert 1 + 1 == 2, "Addition failed"
```

### Running Tests

You can run tests using `testit.runner.main()` by specifying options.

```bash
python jestit/testit/runner.py --module authit --verbose
```

These tests streamline application and API validation with clear summaries upon completion.

## Taskit

Taskit includes the `RedisSubscriber` class for subscribing to Redis channels. It processes messages asynchronously using multithreading.

**Example: Subscribing to a Redis Channel**

```python
from redis import Redis
from taskit.runner import RedisSubscriber

def process_task(data):
    # handle incoming task
    task_type = data['type']
    # do something with the task

redis_subscriber = RedisSubscriber(redis_connection=Redis(), channels=['my_channel'])
redis_subscriber.start_listening()
```

## Utilities

Django-Jestit also offers various helper utilities, ranging from logging (`logit`) to cryptographic operations. Familiarize yourself with these utilities to further refine your project's functionality.

---

Django-Jestit optimizes the way you handle authentication, build REST APIs, and conduct testing. By using these integrated applications and utilities, you can significantly enhance your development workflow in a Django environment.
