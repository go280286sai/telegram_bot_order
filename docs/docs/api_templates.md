# Templates 
## Create template :param request: :param tmp: :return:
#### url: /template/create
#### method: POST
#### request: JSON
#### response: 200
````
{
  "header": "string",
  "title": "string",
  "body": "string"
}
````
## Update template :param request: :param idx: :param tmp: :return:
#### url: /template/update/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
{
  "header": "string",
  "title": "string",
  "body": "string"
}
````
## Get all templates. :return:
#### url: /template/gets
#### method: GET
## Get template. :param idx: :return:
#### url: /template/get/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
````
## Get template. :param idx: :return:
#### url: /template/delete/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
````
## Send users message :param background_task: :param request: :param idx: :return:
#### url: /template/send_users/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
````