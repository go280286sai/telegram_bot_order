# Users 
## Register a new user. :param background_task: :param request: :param user: :return:
#### url: /user/register
#### method: POST
#### request: JSON
#### response: 200
````
{
  "username": "string",
  "password": "string",
  "email": "string",
  "phone": "string"
}
````
## Check if user is authenticated. :param request: :return:
#### url: /user/is_auth
#### method: POST
#### request: JSON
#### response: 200
````
{
  "success": true,
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@admin.com",
    "phone": "+000000000",
    "status": 1,
    "is_admin": 1,
    "first_name": "first_name",
    "last_name": "last_name",
    "bonus": 594
  },
  "error": null
}
````
## Login a new user. :param request: :param user: :return:
#### url: /user/login
#### method: POST
#### request: JSON
#### response: 200
````
{
  "username": "string",
  "password": "string"
}
````
## Logout a user. :param request: :return:
#### url: /user/logout
#### method: POST
#### request: JSON
#### response: 200
## Update profile data. :param request: :param user: :return:
#### url: /user/update_profile
#### method: POST
#### request: JSON
#### response: 200
````
{
  "password": "string"
}
````
## Update profile first name and last name. :param request: :param user: :return:
#### url: /user/add_contact_profile
#### method: POST
#### request: JSON
#### response: 200
````
{
  "first_name": "string",
  "last_name": "string"
}
````
## Set status users :param idx: :param request: :return:
#### url: /user/delete/{idx}
#### method: POST
#### request: JSON
#### response: 200
## Confirm user's data.' :param idx: :param token: :return:
#### url: /user/confirm/{idx}/{token}
#### method: GET
#### response: 200
## Recover user's data.' :param background_task: :param recovery_: :return:
#### url: /user/recovery
#### method: POST
#### request: JSON
#### response: 200
````
{
  "username": "string",
  "email": "string"
}
````
## Get all user's data.' :return:
#### url: /user/gets
#### method: POST
#### response: 200
## Get user data. :return:
#### url: /user/get/{dx}
#### method: POST
#### response: 200
## Update users :return:
#### url: /user/update
#### method: POST
#### request: JSON
#### response: 200
````
{
  "username": "string",
  "email": "string",
  "phone": "string",
  "comments": "string",
  "first_name": "string",
  "last_name": "string"
}
````
## Set status users :param idx: :param stat: :param request: :return:
#### url: /user/set_status/{idx}/{stat}
#### method: POST
````
idx: int
stat: 0 | 1
````
## Set status users :param idx: :param stat: :param request: :return:
#### url: /user/set_status_admin/{idx}/{stat}
#### method: POST
````
idx: int
stat: 0 | 1
````
## Send email :param background_task: :param tmp: :param idx: :param request: :param email: :return:
#### url: /user/send_email/{idx}/{email}
#### method: POST
````
idx: int
email: string

{
  "header": "string",
  "title": "string",
  "body": "string"
}
````
## Set status users :param idx: :param stat: :param request: :return:
#### url: /user/delete_user
#### method: POST
## Send email for delete user :param idx: :param token: :return:
#### url: /user/delete_confirm/{idx}/{token}
#### method: GET
````
idx: int
token: string
````
