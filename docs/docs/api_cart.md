# Carts 
## Create a new delivery. :return:
#### url: /cart/delivery/create
#### method: POST
#### request: JSON
#### response: 200
#### Comment: Create a new delivery
````
{
  "post_id": 0,
  "address_id": 0,
  "city_id": 0
}
````
## Add discount to cart. :return:
#### url: /cart/discount/add/{discount}
#### method: POST
#### request: JSON
#### response: 200
````
{
  "success": true,
  "data": null,
  "error": null
}
````
## Get a delivery. :param request: :return:
#### url: /cart/discount/get
#### method: POST
#### request: JSON
#### response: 200
````
{
  "success": true,
  "data": {
    "post_name": "Nash Inc",
    "city_name": "Pricestad",
    "address_name": "044 Schaefer Forest\nJohnburgh, SC 88372"
  },
  "error": null
}
````
## Delete delivery cookie from session
#### url: /cart/discount/get
#### method: POST
#### request: JSON
#### response: 200
````
{
  "success": true,
  "data": null,
  "error": null
}
````
## Increase the amount of the cart :param request: :param product_id: :return:
#### url: /cart/increase/{product_id}
#### method: POST
#### request: JSON
#### response: 200
````
http://localhost:8000/cart/increase/1
{
  "success": true,
  "data": {
    "cart": {
      "1": 1
    }
  },
  "error": null
}
````
## Decrease the amount of the cart :param product_id: :param request: :return:
#### url: /cart/decrease/{product_id}
#### method: POST
#### request: JSON
#### response: 200
````
http://localhost:8000/cart/decrease/1

{
  "success": true,
  "data": {
    "cart": {}
  },
  "error": null
}
````
## Remove product from cart :param product_id: :param request: :return:
#### url: /cart/remove/{product_id}
#### method: POST
#### request: JSON
#### response: 200
````
http://localhost:8000/cart/remove/1

{
  "success": true,
  "data": {
    "cart": {}
  },
  "error": null
}
````
## Set total bonus :param cart: :param request: :return:
#### url: /cart/total_bonus
#### method: POST
#### request: JSON
#### response: 200
````
{
  "total": 0,
  "bonus": 0
}
http://localhost:8000/cart/total_bonus

{
  "success": true,
  "data": null,
  "error": null
}
````
## Get cart :param request: :return:
#### url: /cart/
#### method: POST
#### request: JSON
#### response: 200
````
http://localhost:8000/cart/

{
  "success": true,
  "data": {
    "cart": [],
    "bonus": 594,
    "pay_bonus": "0",
    "total": "0.0"
  },
  "error": null
}
````