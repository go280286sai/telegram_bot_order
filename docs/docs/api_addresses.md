# Addresses 
## Create address :param request: :param address: :return:
#### url: /address/create
#### method: POST
#### request: JSON
#### response: 200
#### Comment: Create a new address
````
{
  "name": "string",
  "city_id": 0
}
````
## Update address :param request: :param idx: :param address: :return:
#### url: /address/update/{idx}
#### method: POST
#### request: JSON
#### response: 200
#### Comment: Update address
````
idx: int
{
  "name": "string",
  "city_id": 0
}
````
## Get addresses :return:
#### url: /address/gets
#### method: GET
#### Comment: Load all addresses
## Get address :return:
#### url: /address/get/{citi_id}
#### method: GET
#### request: JSON
#### response: 200
#### Comment: Load addresses from select city
````
citi_id: int
````
## Delete address :param request: :param idx: :return:
#### url: /address/delete/{idx}
#### method: POST
#### request: JSON
#### response: 200
#### Comment: Delete select address
````
idx: int
````
