import requests
from requests_oauthlib import OAuth1

from flask import current_app as app

from app.helpers.common import welfare
from app.models.attribute import AttributeModel

def _generate_headers():
    return {
        'Content-Type': 'application/json'
    }

def _url():
    return app.config.get("WS_URL")

'''
Attributes from database
'''
def _attr_map(attridibute_id):
    return AttributeModel.get_attr_by_id(attridibute_id)

def _delivery_map(d):
    delivery = {
        "flatrate_flatrate": "Достава со такси"
    }
    return delivery.get(d, "")

'''
A method for getting attribute value by given id
'''
def _item_all_attr(attr):
    all_attrs = []
    for a in attr:
        all_attrs_str = str(a['option_value'])
        all_attrs_list = [int(x) for x in all_attrs_str.split(',')]
        for l in all_attrs_list:
            all_attrs.append(_attr_map(l))

    return all_attrs

'''
A method for collecting product items
'''
def _items(items):
    all_items = {}
    num = 0
    for item in items:
        # Check if the product has custom attributes
        if 'product_option' in item:
            all_items.update(
                { 
                    num: {
                        "name": item['name'],
                        "qty": item['qty_ordered'],
                        "itemPrice": item['row_total_incl_tax'],
                        "attributes": _item_all_attr(item['product_option']['extension_attributes']['custom_options'])
                    }
                }
            )
        else:
            all_items.update(
                { 
                    num: {
                        "name": item['name'],
                        "qty": item['qty_ordered'],
                        "itemPrice": item['row_total_incl_tax'],
                    }
                }
            )
        num += 1

    return all_items

'''
A method for pushing printer data to external socket proxy
'''
def socket_printer(order, prep_time):

    path = '/api/printer'
    url = _url() + path
    headers = _generate_headers()

    items = _items(order['response']['items'])
    delivery = _delivery_map(order['response']['extension_attributes']['shipping_assignments'][0]['shipping']['method'])

    json = {
            "creationDate":order['response']['created_at'],
            "deliveryDate":order['response']['extension_attributes']['delivery_date'],
            "customerFirstName":order['response']['extension_attributes']['shipping_assignments'][0]['shipping']['address']['firstname'],
            "customerLastName":order['response']['extension_attributes']['shipping_assignments'][0]['shipping']['address']['lastname'],
            "customerPhoneNumber":order['response']['extension_attributes']['shipping_assignments'][0]['shipping']['address']['telephone'],
            "items":items,
            "totalPrice":order['response']['subtotal_incl_tax'],
            "delivery":delivery,
            "preparingTime":prep_time
    }

    r = requests.post(url=url, headers=headers, json=json)

    return r.json()

'''
A method for pushing customer SMS message details to external socket proxy
'''
def socket_sms(order, content):
    
    path = '/api/message'
    url = _url() + path
    headers = _generate_headers()

    phone = order['response']['extension_attributes']['shipping_assignments'][0]['shipping']['address']['telephone']

    json = {
        "phone": phone,
        "content": content
    }

    r = requests.post(url=url, headers=headers, json=json)

    return r.json()