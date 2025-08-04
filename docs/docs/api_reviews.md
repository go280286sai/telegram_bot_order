# Reviews 
## Create a new review. :param request: :param item: :return:
#### url: /review/create
#### method: POST
#### request: JSON
#### response: 200
````
{
  "name": "string",
  "text": "string",
  "gender": 0
}
````
## Update an existing review. :param request: :param idx: :param item: :return:
#### url: /review/update/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
{
  "name": "string",
  "text": "string",
  "gender": 0
}
````
## Get all reviews. :return:
#### url: /review/reviews
#### method: GET
## Delete an existing review. :param request: :param idx: :return:
#### url: /review/delete/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
````