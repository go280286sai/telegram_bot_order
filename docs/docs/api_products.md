# Products 
## Create a new product. :param request: :param item: :return:
#### url: /product/create
#### method: POST
#### request: JSON
#### response: 200
````
{
  "name": "string",
  "description": "string",
  "price": 0,
  "amount": 0,
  "service": 0
}
````
## Update an existing product. :param request: :param idx: :param item: :return:
#### url: /product/update/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
{
  "name": "string",
  "description": "string",
  "price": 0,
  "amount": 0,
  "service": 0
}
````
## Get all products. :return:
#### url: /products/products
#### method: GET
## Create a new product. :param idx: :return:
#### url: /product/product/{idx}
#### method: POST
## Delete an existing product. :param request: :param idx: :return:
#### url: /product/delete/{idx}
#### method: POST
#### request: JSON
#### response: 200
````
idx: int
````