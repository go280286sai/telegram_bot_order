# Settings 
## Create setting :param request: :param setting_: :return:
#### url: /setting/create
#### method: POST
#### request: JSON
#### response: 200
````
{
  "name": "string",
  "value": "string"
}
````
#### Comment: Create new setting
## Create auto settings :return:
#### url: /setting/auto_create
#### method: POST
#### Comment: Create autoload settings
## Update setting :param request: :param idx: :param setting_: :return:
#### url: /setting/update/{idx}
#### method: POST
#### request: JSON
#### response: 200
#### Comment: Update settings
````
idx: int
{
  "name": "string",
  "value": "string"
}
````
## Get settings :return:
#### url: /setting/gets
#### method: GET
#### Comment: Get all settings
## Get settings :return:
#### url: /setting/get/discount
#### method: GET
#### Comment: Fet setting
## Delete setting :param request: :param idx: :return:
#### url: /setting/delete/{idx}
#### method: POST
#### request: JSON
#### response: 200
#### Comment: Delete setting
````
idx: int
````
## Get settings :return:
#### url: /setting/truncate
#### method: POST
#### Comment: Delete all data from database
## Get settings :return:
#### url: /setting/demo
#### method: POST
#### Comment: Load dema data to database