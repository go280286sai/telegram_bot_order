# Subscribers 
## Create subscriber route. :param sub: :param background_task: :return:
#### url: /subscriber/create
#### method: POST
#### request: JSON
#### response: 200
````
{
  "email": "string"
}
````
## Confirm subscriber route. :param idx: :param token: :return:
#### url: /subscriber/confirm/{idx}/{token}
#### method: GET
````
idx: int
token: str
````
## Destroy subscriber route. :param idx: :param token: :return:
#### url: /subscriber/destroy/{idx}/{token}
#### method: GET
#### request: JSON
#### response: 200
````
idx: int
token: str
````
## Send email route. :param idx: :return:
#### url: /subscriber/send_email/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
````
## Send users message :param request: :param background_tasks: :param idx: :return:
#### url: /subscriber/send_subscribers/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
````
