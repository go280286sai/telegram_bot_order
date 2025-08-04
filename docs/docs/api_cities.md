# Cities 
## Create city :param request: :param city: :return:
#### url: /city/create
#### method: POST
#### request: JSON
#### response: 200
````
{
  "name": "string",
  "post_id": 0
}
````
## Update city :param request: :param idx: :param city: :return:
#### url: /city/update/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
{
  "name": "string",
  "post_id": 0
}
````
## Get cities :return:
#### url: /city/get/{post_id}
#### method: GET
````
post_id: int
````
## Get cities :return:
#### url: /city/gets
#### method: GET
## Get cities :return:
#### url: /city/delete/{idx}
#### method: POST
````
idx: int
````