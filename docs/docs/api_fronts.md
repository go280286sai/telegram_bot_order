# Fronts 
## Create a carousel item :param request: :param carousel: :return:
#### url: /front/carousel/create
#### method: POST
#### request: JSON
#### response: 200
````
{
  "title": "string",
  "description": "string",
  "image": "string"
}
````
## Update a carousel item :param request: :param idx: :param carousel: :return:
#### url: /front/carousel/update/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
{
  "title": "string",
  "description": "string",
  "image": "string"
}
````
## Get all carousel items :return:
#### url: /front/carousel/gets
#### method: GET
## Delete item
#### url: /front/carousel/delete/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
````
