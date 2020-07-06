# Installation

PizzaApp requires python3.8,  Node.js 12.16

The first step to running PizzAapp locally is downloading the code by cloning the repository.
```bash
git clone https://gitlab.com/aykutarslantas/pizzaapp.git
```
# DOCKER (Development)

You can start both api and frontend development servers by typing `docker-compose up -d`.
## Backend

Django Rest Framework used to create API functionality. 

``` bash
cd python
pip install -r requirements_file.txt
```

## Frontend

The frontend created using Vue framework and yarn as dependency manager.


``` bash
cd vuejs
yarn install
yarn global add @vue/cli 
yarn upgrade vue cli service / plugins 
```


# Running App Locally


## Backend

Backend serves on 8000 port.

```bash
cd python
python manage.py migrate
python manage.py loaddata user
python manage.py runserver
```

## Frontend

Frontend serves on 8080 port. The default user credentials username: testuser , password: testpasswd

```bash
cd vuejs
yarn serve
```


# API Usage


## Register a new user

**Request**

`POST /api/v1/users/register`

**Arguments**

- `"username":string` unique name or unique email for user
- `"password":string` password for user

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/users/register/' \
--form 'username=newuser' \
--form 'password=newpassword'
```

**Response**
- 201: created
- 400: user already exists or fields are missing

## Get auth token for user (login)

**Request**

`POST /api/v1/auth-jwt/`

**Arguments**

- `"username":string`
- `"password":string`

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/auth-jwt/' \
--data-urlencode 'username=useradmin' \
--data-urlencode 'password=userpasswd'
```

**Response**

- 200: logged in successfully
- 400: invalid credentials

```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg",
    "username": "testuser",
    "email": "test@pizza.com",
    "is_staff": true
}
``` 

### Verify user token

**Request**

`POST /api/v1/auth-verify-jwt/`

**Arguments**

- `"token":string` 

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/auth-jwt-verify/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```

**Response**

- 200: verified the token
- 400: signature expired or invalid

### Refresh user token

**Request**

`POST /api/v1/auth-jwt-refresh/`

**Arguments**

- `"token":string` 

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/auth-jwt-refresh/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```

**Response**

- 200: returns new token
- 400: signature expired or invalid

```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg",
    "username": "testuser",
    "email": "test@pizza.com",
    "is_staff": true
}
```

### Get user data with token

**Request**

`POST /api/v1/current_user`

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/v1/current_user/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```

**Response**

- 200: returns user data
- 400: signature expired or invalid

```json
{
    "username": "testuser",
    "email": "test@pizza.com",
    "is_staff": true
}
```

### List all users

**Request**

`GET /api/v1/user_list`


```bash
curl --location --request GET 'http://127.0.0.1:8000/api/v1/user_list/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```

**Response**

- 200: returns list of users 
- 401: unauthorized, invalid or expired token

```json 
[
    {
        "username": "testuser",
        "email": "test@pizza.com",
        "is_staff": true
    },
    {
        "username": "test",
        "email": "",
        "is_staff": false
    },
]
```

### List all tasks

**Request**

`GET /api/v1/task_list/`

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/v1/task_list/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMSwidXNlcm5hbWUiOiJ0ZXRldGUzNDEyIiwiZXhwIjoxNTg0MzA3NjE4LCJlbWFpbCI6IiIsIm9yaWdfaWF0IjoxNTg0MzA2NjE4fQ.UOxZvmpei4KrK8W1_hC4ujoix83wKIpi37TU2PhiXaA'
```

**Response**

- 200: success
- 400: signature expired, invalid or missing field

```json
{
"task_list": [
	{
		"id" : 1,
		"name" : "test123",
		"failure_reason" : null,
		"created" : "2020-04-07 16:17:30.749439",
		"started" : "2020-04-07 16:40:10.529759",
		"finished" : "2020-04-07 16:40:11.606818",
		"status" : "success",
		"step" : 12,
		"data_filepath" : "uploaded_tasks\/instance.xlsx",
		"result" : ""
	},
	{
		"id" : 2,
		"name" : "test123",
		"failure_reason" : null,
		"created" : "2020-04-08 14:17:30.749439",
		"started" : "2020-04-08 14:40:10.529759",
		"finished" : "2020-04-08 14:40:11.606818",
		"status" : "success",
		"step" : 12,
		"data_filepath" : "uploaded_tasks\/testx.xlsx",
		"result" : ""
	}
]}
```

### Retrieve a spesific task

**Request**

`GET /api/v1/task_list/:id/`

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/v1/task_list/1/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMSwidXNlcm5hbWUiOiJ0ZXRldGUzNDEyIiwiZXhwIjoxNTg0MzA3NjE4LCJlbWFpbCI6IiIsIm9yaWdfaWF0IjoxNTg0MzA2NjE4fQ.UOxZvmpei4KrK8W1_hC4ujoix83wKIpi37TU2PhiXaA'
```

**Response**

- 200: success
- 400: signature expired, invalid or missing field
- 401: signature expires, unauthenticated
- 404: not found

```json
{
	"id" : 1,
	"name" : "test123",
	"failure_reason" : null,
	"created" : "2020-04-07 16:17:30.749439",
	"started" : "2020-04-07 16:40:10.529759",
	"finished" : "2020-04-07 16:40:11.606818",
	"status" : "success",
	"step" : 12,
	"data_filepath" : "uploaded_tasks\/instance.xlsx",
	"result" : ""
},
```



### Create a task

**Request**

`POST /api/v1/task_list`

**Arguments**

- `"name":string` kask name
- `"data_filepath":file` excel file 
- `"step":int` prediction step 

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/task_list/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTg0MzA2MDEzLCJlbWFpbCI6ImFkbWluQHBpenphLmNvbSIsIm9yaWdfaWF0IjoxNTg0MzA1MDEzfQ.U8WDIrHqPe7E1W6fZVMdbYSJuLyqnviOSrZyGOdwa7c' \
--header 'Content-Type: multipart/form-data; boundary=--------------------------334404378599425904282926' \
--form 'name=starttask' \
--form 'data_filepath=@/C:/example.xlsx' \
--form 'step=12'
```

**Response**

- 201: created successfully
- 400: signature expired, invalid or missing field
- 401: unauthorized

```json
{
    "id": 1,
    "name": "starttask",
    "failure_reason": null,
    "created": "2020-04-08 16:17:30.749439",
    "started": null,
    "finished": null,
    "status": "not_started",
    "step": 12,
    "data_filepath": "http://127.0.0.1:8000/api/v1/task_list/uploaded_tasks/example.xlsx",
    "result": null
}
```

### Start a task

**Request**

`POST /api/v1/task_list/:id/start_task/`

**Arguments**
- `"id":int` task id

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/task_list/1/start_task/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTg0MDkxNjk5LCJlbWFpbCI6ImFkbWluQHBpenphLmNvbSIsIm9yaWdfaWF0IjoxNTg0MDkwNjk5fQ.6bKH2XBo87btU7ssjLz1Exz-d7sa7GXAAW0zzDiY3pM'
```

**Response**

- 200: task started
- 400: signature expired, invalid or missing field
- 401: unauthorized
- 404: no task found by given id

```json
{
    "id": 1,
    "name": "starttask",
    "failure_reason": null,
    "created": "2020-04-08 16:17:30.749439",
    "started": "2020-04-08 16:21:30.749439",
    "status": "continue",
    "finished": null,
    "step": 12,
    "data_filepath": "http://127.0.0.1:8000/api/v1/task_list/uploaded_tasks/example.xlsx",
    "result": null
}
```

### Delete a task

**Request**

`DELETE /api/v1/task_list/`

**Arguments**

- `"id":int` task id

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/task_list/1/start_task/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTg0MDkxNjk5LCJlbWFpbCI6ImFkbWluQHBpenphLmNvbSIsIm9yaWdfaWF0IjoxNTg0MDkwNjk5fQ.6bKH2XBo87btU7ssjLz1Exz-d7sa7GXAAW0zzDiY3pM'
```

**Response**
- 204: task deleted
- 401: unauthorized
- 404: no task found by given id

### Update a task

**Request**

`PATCH /api/v1/task_list/:id/`

**Arguments**
- `"name":string`  optional
- `"failure_reason":string`  optional
- `"created":string` optional
- `"started":string`  optional
- `"finished":string`  optional
- `"status":string`  optional
- `"step":int`  optional
- `"data_filepath":file`  optional
- `"result":string`  optional

```bash
curl --location --request PATCH 'http://127.0.0.1:8000/api/v1/task_list/1/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTg0MzA2MzMwLCJlbWFpbCI6ImFkbWluQHBpenphLmNvbSIsIm9yaWdfaWF0IjoxNTg0MzA1MzMwfQ.L4MHdxEk71wymsv73FvpIA77Sc5b3L9Wru2WS8CUVaY' \
--header 'Content-Type: application/json' \
--data-raw '{
    "failure_reason": "",
    "name": "update_name"
}'
```

**Response**

- 200: task updated
- 401: unauthorized
- 404: no task found by given id

```json
{
    "id": 1,
    "name": "update_name",
    "failure_reason": "",
    "created": "2020-04-08 16:17:30.749439",
    "started": "2020-04-08 16:21:30.749439",
    "finished": null,
    "status": "failure",
    "step": 12,
    "data_filepath": "http://127.0.0.1:8000/api/v1/task_list/uploaded_tasks/example_2.xlsx",
    "result": null
}
```