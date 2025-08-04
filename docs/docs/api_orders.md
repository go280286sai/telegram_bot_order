# Orders 
## Create a new order.
#### url: /order/create
#### method: POST
#### request: JSON
````
{
  "transaction": "string",
  "cardTotal": 0
}
````
## Get orders user :param request: :return:
#### url: /order/get_orders_user
#### method: POST
````
{
  "success": true,
  "data": {
    "orders": [
      {
        "id": 1,
        "total": 13942,
        "status": 0,
        "created_at": "2025-08-04"
      },
      {
        "id": 2,
        "total": 29321,
        "status": 0,
        "created_at": "2025-08-04"
      }
    ]
  },
  "error": null
}
````
## Create a payment. :param pay_: :return:
#### url: /order/pay
#### method: POST
#### request: JSON
````
{
  "cardTotal": 0,
  "cardNumber": "string",
  "cardMonth": "string",
  "cardYear": "string",
  "cardKey": "string"
}
````
## Get orders user :param request: :return:
#### url: /order/pay
#### method: POST
## Send invoice :param background_task: :param order_id: :param idx: :param invoice: :param request: :return:
#### url: /order/send_invoice/{idx}/{order_id}
#### method: POST
#### request: JSON
````
idx: int
order_id: int

{
  "body": "string"
}
````
## Add comment :param comment: :param idx: :param request: :return:
#### url: /order/add_comment/{idx}
#### method: POST
#### request: JSON
````
idx: int

{
  "body": "string"
}
````
## Get order view :param idx: :param request: :return:
#### url: /order/get_view/{idx}
#### method: POST
#### request: JSON
````
idx: int
````
## Get predict :param n: :param request: :return:
#### url: /order/get_predict/{n}
#### method: POST
#### request: JSON
````
n: int
````
## Delete order :param idx: :param request: :return:
#### url: /order/delete/{idx}
#### method: POST
#### request: JSON
````
idx: int
````
