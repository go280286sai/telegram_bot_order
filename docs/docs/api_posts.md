# Posts 
## Create post :param request: :param post_: :return:
#### url: /post/create
#### method: POST
#### request: JSON
#### response: 200
````
{
  "name": "string"
}
````
## Update post :param request: :param idx: :param post_: :return:
#### url: /post/update/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
{
  "name": "string"
}
````
## Get posts :return:
#### url: /post/gets
#### method: GET
## Delete post :param request: :param idx: :return:
#### url: /post/delete/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
````