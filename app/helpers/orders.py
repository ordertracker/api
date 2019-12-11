import requests
from requests_oauthlib import OAuth1
from flask import current_app as app
from app.helpers.common import welfare

'''
Private method for keeping the Magento URL
'''
def _url():
    return app.config.get("MAGENTO_URL")

'''
OAuth Authentication
'''
def _auth():
    auth = OAuth1(
                app.config.get("CONSUMER_KEY"),
                app.config.get("CONSUMER_SECRET"),
                app.config.get("ACCESS_TOKEN"),
                app.config.get("ACCESS_TOKEN_SECRET")
            )
    return auth

'''
Genereting header for all requests
'''
def generate_headers():
    return {
        'Content-Type': 'application/json'
    }

'''
Counting all orders
'''
def _orders_count():

    path = '/rest/V1/orders?searchCriteria=all'
    url = _url() + path
    headers = generate_headers()

    r = requests.get(url=url, auth=_auth(), headers=headers)
    orders = r.json()

    return orders

'''
Counting orders by status
'''
def _orders_count_by_status(status):

    path = ("/rest/V1/orders?"
            "&searchCriteria[filter_groups][0][filters][0][field]=status"
            "&searchCriteria[filter_groups][0][filters][0][value]=%s"
            "&searchCriteria[filter_groups][0][filters][0][condition_type]=eq"
            "&searchCriteria[sortOrders][0][field]=created_at&searchCriteria[sortOrders][0][direction]=DESC") % (status)
    url = _url() + path
    headers = generate_headers()

    r = requests.get(url=url, auth=_auth(), headers=headers)
    orders = r.json()

    return orders

'''
Get all Magento orders
'''
def get_all_orders(start, limit):

    start = int(start)
    limit = int(limit)

    orders = _orders_count()
    count = len(orders["items"])
    
    path = ("/rest/V1/orders?"
            "fields=items[entity_id,increment_id,created_at,customer_email,customer_firstname,customer_lastname,status,subtotal_incl_tax,items[name,price_incl_tax,qty_ordered]]"
            "&searchCriteria[filter_groups][0][filters][0][field]=created_at"
            "&searchCriteria[filter_groups][0][filters][0][value]=2019-05-16T04:00:00.0000000Z"
            "&searchCriteria[filter_groups][0][filters][0][condition_type]=from"
            "&searchCriteria[filter_groups][1][filters][0][field]=created_at"
            "&searchCriteria[filter_groups][1][filters][0][value]=2019-07-11T04:00:00.0000000Z"
            "&searchCriteria[filter_groups][1][filters][0][condition_type]=to"
            "&searchCriteria[sortOrders][0][field]=created_at&searchCriteria[sortOrders][0][direction]=DESC"
            "&searchCriteria[current_page]=%d"
            "&searchCriteria[page_size]=%d") % (start, limit)
    url = _url() + path
    headers = generate_headers()

    r = requests.get(url=url, auth=_auth(), headers=headers)
    orders = r.json()

    endpoint = '/api/orders'

    if limit < 0:
        return {
            "message": "Pagination error"
        }, 404

    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count

    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = start - 1
        obj['previous'] = endpoint + '?start=%d&limit=%d' % (start_copy, limit)

    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + 1
        obj['next'] = endpoint + '?start=%d&limit=%d' % (start_copy, limit)

    obj['results'] = orders["items"][(start - 1):(start - 1 + limit)]

    return obj
    
'''
Get orders by status
'''
def get_orders_by_status(status, start, limit):

    start = int(start)
    limit = int(limit)

    orders = _orders_count_by_status(status)
    count = len(orders["items"])
    
    path = ("/rest/V1/orders?"
            "fields=items[entity_id,increment_id,created_at,extension_attributes[delivery_date],customer_email,customer_firstname,customer_lastname,status,subtotal_incl_tax,items[name,price_incl_tax,qty_ordered]]"
            "&searchCriteria[filter_groups][0][filters][0][field]=status"
            "&searchCriteria[filter_groups][0][filters][0][value]=%s"
            "&searchCriteria[filter_groups][0][filters][0][condition_type]=eq"
            "&searchCriteria[sortOrders][0][field]=created_at&searchCriteria[sortOrders][0][direction]=DESC") % (status)
    url = _url() + path
    headers = generate_headers()

    r = requests.get(url=url, auth=_auth(), headers=headers)
    orders = r.json()

    endpoint = '/api/orders'

    if limit < 0:
        return {
            "message": "Pagination error"
        }, 404

    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count

    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = start - 1
        obj['previous'] = endpoint + '?start=%d&limit=%d' % (start_copy, limit)

    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + 1
        obj['next'] = endpoint + '?start=%d&limit=%d' % (start_copy, limit)

    obj['results'] = orders["items"][(start - 1):(start - 1 + limit)]

    response = {
        "message": r.reason,
        "response": obj,
        "code": r.status_code
    }

    return response

'''
Get Magent Order by Entity ID including the order items
'''
def get_order(entity_id):

    path = '/rest/V1/orders/' + str(entity_id) + "?fields=entity_id,increment_id,created_at,customer_email,customer_firstname,customer_lastname,state,status,subtotal_incl_tax,payment[additional_information],extension_attributes[delivery_date,shipping_assignments[shipping[address,method]]]"
    url = _url() + path
    headers = generate_headers()

    r = requests.get(url=url, auth=_auth(), headers=headers)
    r_order = r.json()
    r_items = get_order_items(entity_id)
    r_order.update(r_items)

    response = {
        "message": r.reason,
        "response": r_order,
        "code": r.status_code
    }

    return response

'''
Get Magent Order Items by Entity ID
'''
def get_order_items(entity_id):

    path = ("/rest/V1/orders/items?"
            "fields=items"
            "&searchCriteria[filter_groups][0][filters][0][field]=order_id"
            "&searchCriteria[filter_groups][0][filters][0][value]=%s"
            "&searchCriteria[filter_groups][0][filters][0][condition_type]=eq") % (entity_id)
    url = _url() + path
    headers = generate_headers()

    r = requests.get(url=url, auth=_auth(), headers=headers)

    return r.json()

'''
Updating specific order with new status
'''
def order_update(data):

    json = { 
        "entity":{
                "entity_id":data['entity_id'],
                "state":data['status'],
                "status":data['status']
        }
    }

    path = '/rest/V1/orders'
    url = _url() + path
    headers = generate_headers()

    r = requests.post(url=url, auth=_auth(), headers=headers, json=json)

    return r.reason