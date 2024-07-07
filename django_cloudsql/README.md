## Django
I used the VIEW class of Django which provides features to create a view including request , response handling, and error handling , database is used to store the data.ORM feature is used to design the database schema. Defined a model Django models are Python classes that represents database tables. Each model class corresponds to a table, and the class attributes define the table's fields.

## ORM
I have used Django's object relation maping in my project. ORM is a way to interact with database using classes. We can create class, object and use them to interact with database instead of writing naked DB queries.

For example:
```
class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
```

- we created a class Roles, above class will create table in database

- if we want to insert data in above table then we don't need to write database query. Instead we will create object of the above class, mention below.

- new_obj=Roles(name="web");

- Then new_obj.save() ->this function will save above entry in Roles table.

- So as you can see I created Database table , inserted data in table using object oriented.

# Authentication

## I have custom user model in my project.

To create a custom user model, you need to create two classes in models. Let's say one class is User, and it inherits the AbstractBaseUser class from django.contrib.auth.models. The User class should contain fields for the user table, such as firstname, lastname, etc , with some methods like has_perm() to check permissions, has_module_perm() to check the permission of a given app, and user serializer. The User class should also contain an object of the UserManager class.

Let's say another class is the UserManager class, which contains two methods: create_user and create_superuser, to create two different types of users. The UserManager class should inherit from BaseUserManager from django.contrib.auth.models. Inside the view, call the function get_user_model(), which returns the user model that is currently active in your project. Later, you can use this user model to make queries in that model, such as find(), get(), findAll(), etc. get_user_model() is located in django.contrib.auth.

## I have used token based authentication using rest_framework_simplejwt app of django rest framework.
To impliment jwt authentication of django rest framework we have to apply some configuration in setting file of project.
1. add rest_framework_simplejwt to your INSTALLED_APP section of setting file
2. add below section in you setting file at any where 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
} 

3. To generate a token. Inside the login view, verify the user using the authenticate() method, which is located in django.contrib.auth, then call the login() method of the same module to set the user session. Then, generate the reference token using the for_user() method of the RefreshToken class, which is located in rest_framework_simplejwt.tokens.

    ```
    def put(self, request)
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        is_auth_user = authenticate(request, username=username, password=password)

        if is_auth_user:
            login(request, is_auth_user)
            refresh = RefreshToken.for_user(is_auth_user)
            return JsonResponse(
                {
                    "message": "Logged in successfully",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=200,
            )
    ```
# Pagination
I have used pagination of django rest framework.To setup the pagination in project to impliment pagination use following steps.

### step1
1. add below code in setting file of your project.Where PAGE_SIZE is number of items to display per page.this is default in whole project

```
REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'PAGE_QUERY_PARAMETER': 'limit',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 
}
```
### step2 
In a view, use the PageNumberPagination class from Django Rest Framework. PageNumberPagination is a built-in class in Django REST framework designed to handle pagination automatically. You just need to provide some parameters, such as the page size and the query parameters for page and page size if necessary. The rest of the pagination work, including dividing the data into pages and returning the appropriate page based on the request, will be handled by the PageNumberPagination class.

paginate_queryset(): The primary purpose of paginate_queryset is to take a large queryset and split it into smaller chunks (pages). Determine the appropriate page of data to return based on the current request. Provide metadata about the pagination, such as the current page, total pages, and the number of items per page. In most cases, you don't need to call paginate_queryset directly. DRF handles it automatically when you set a pagination class in your view. In custom implementations, you can call paginate_queryset to control pagination more precisely. Use get_paginated_response to generate a response with pagination metadata

Implimantation
```
class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 100
```
```
def get(self, request: HttpRequest) -> JsonResponse:
    data = request.GET
    client_id = data.get("client_id")

    users = User.objects.filter(client_id=client_id)
    paginator = CustomPagination()
    paginated_users = paginator.paginate_queryset(users, request)
    serialized_data = [user.user_serializer() for user in paginated_users]

    return paginator.get_paginated_response(serialized_data)

```
# caching
"I have used Redis cache in this project. Cache is used to improve the performance of the application by reducing the access time of data. Cache stores frequently accessed data in memory, so next time a user accesses the same data, instead of hitting the database query, the data will be returned directly from the memory stored by the cache. Redis cache is an in-memory data structure that stores cached data in memory (RAM)

### steps to impliment redis cache in project 
### step1: 
configure the cache in setting file of your project
```
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis_service:6379/2',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'MAX_MEMORY_POLICY': 'volatile-lru',
        },
    }
}
```

### step2: 
 import the cache from django.core.cache import cache in your view. In the view, create a unique key to store cache data in memory, where the value will be the cached data. A user accesses the data from the database for the first time, and before returning the data, we create a unique key and store the accessed data with the key in Redis. Next time the user accesses the same data, we look for the same key in Redis; if it is available, we will return the data from Redis and do not need to hit the database query

```
def get(self, request: HttpRequest) -> JsonResponse:
    user_id = request.GET.get("id")
    cache_key = f"user_data_{user_id}"

    cached_data = cache.get(cache_key)
    if cached_data:
        response_data = cached_data
        return JsonResponse(response_data, status=200)
        
    serialized_data = user.user_serializer()
    cache.set(cache_key, serialized_data, timeout=300)
    return JsonResponse(serialized_data, status=200)
```