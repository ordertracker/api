import requests, json
from flask import request
from flask import current_app as app
from flask_restful import reqparse
from flask_restplus import Namespace, Resource

from app.helpers.orders import get_all_orders, get_order, get_order_items, order_update, get_orders_by_status
from app.helpers.common import authorize, welfare, get_service_token, status_code_responses
from app.helpers.socket import socket_printer, socket_sms

_orders_parser = reqparse.RequestParser()
_orders_parser.add_argument(
    "entity_id",
    type=int,
    required=False,
)
_orders_parser.add_argument(
    "status",
    type=str,
    required=False,
)
_orders_parser.add_argument(
    "prep_time",
    type=str,
    required=False
)
_orders_parser.add_argument(
    "sms_content",
    type=str,
    required=False
)
_orders_parser.add_argument(
    "reason",
    type=str,
    required=False
)

api = Namespace('orders', path='/api', description='Magento orders')

@api.route('/orders')
@api.doc(responses=status_code_responses,
         security=['apitoken']
        )
class Orders(Resource):
    @authorize
    @welfare
    @api.doc(description='Get all Magento orders')
    def get(self):
        orders = get_all_orders(
            start=request.args.get('start', 1), 
            limit=request.args.get('limit', 10)
        )
        return orders, 200

@api.route('/order/<int:entity_id>')
@api.doc(response=status_code_responses,
         security=['apitoken']
        )
class Order(Resource):
    @authorize
    @welfare
    @api.doc(description='Get order by entity id')
    def get(self, entity_id):
        order = get_order(entity_id)
        if order:
            return order, 200
        else:
            return {
                "message": "Order not found!"
            }, 404

@api.route('/order_items/<int:entity_id>')
@api.doc(response=status_code_responses,
         security=['apitoken']
        )
class OrderItems(Resource):
    @authorize
    @welfare
    @api.doc(description='Get order items by entity id')
    def get(self, entity_id):
        order = get_order_items(entity_id)
        if order:
            return order, 200
        else:
            return {
                "message": "Order not found!"
            }, 404

@api.route('/get_orders_by_status/<string:status>')
@api.doc(response=status_code_responses,
         security=['apitoken']
        )
class OrdersByStatus(Resource):
    @authorize
    @welfare
    @api.doc(description='Get orders by status')
    def get(self, status):
        order = get_orders_by_status(
            status,
            start=request.args.get('start', 1),
            limit=request.args.get('limit', 10)
        )
        if order:
            return order, 200
        else:
            return {
                "message": "Request error"
            }, 404

@api.route('/order_update')
@api.doc(response=status_code_responses,
         security=['apitoken']
        )
class OrderUpdate(Resource):
    @authorize
    @welfare
    @api.doc(description='Updating order with specific status and sending data to WS')
    def post(self):

        response = {}
        data = _orders_parser.parse_args()
        order_statuses = ['processing', 'completed', 'canceled']

        if data['status'] not in order_statuses:
            return {
                "message": "Unknown order status",
                "response": "",
                "code": 400
            }

        order = get_order(data['entity_id'])
        if order['code'] != 200:
            return {
                "message": "Order not exist",
                "response": "",
                "code": 400
            }
        
        if data['status'] == 'processing':

            if data['prep_time'] == '':
                return {
                    "message": "Prepare time is required for processing orders",
                    "response": "",
                    "code": 400
                }

            sms_content = "Вашата нарачка ќе биде подготвена за " + data['prep_time'] + " минути. Ви благодариме!"

            printer = socket_printer(order, data['prep_time'])
            sms = socket_sms(order, sms_content)

            if printer['status'] != 'OK':
                return {
                    "message": "Receipt not successfully printed",
                    "response": {
                        "printer": printer['status']
                    },
                    "code": 400
                }
                
            if sms['status'] != 'OK':
                return {
                    "message": "Message not sent to customer",
                    "response": {
                        "sms": sms['status']
                    },
                    "code": 400
                }

            response.update(
                            {
                                "response": {
                                    "sms": sms,
                                    "printer": printer,
                                }
                            }
            )

        if data['status'] == 'canceled':
            sms_content = data['reason']
            sms = socket_sms(order, sms_content)

            if sms['status'] != 'OK':
                return {
                    "message": "Message not sent to customer",
                    "response": {
                        "sms": sms['status']
                    },
                    "code": 400
                }

            response.update(
                            {
                                "response": {
                                    "sms": sms
                                }
                            }
            )

        if data['status'] == 'completed':
            sms_content = "Вашата нарачка е успешно завршена."
            sms = socket_sms(order, sms_content)

            if sms['status'] != 'OK':
                return {
                    "message": "Message not sent to customer",
                    "response": {
                        "sms": sms['status']
                    },
                    "code": 400
                }

            response.update(
                            {
                                "response": {
                                    "sms": sms
                                }
                            }
            )

        order = order_update(data)
        if order != 'OK':
            return {
                "message": "Order not updated in Magento",
                "code": 400
            }

        response.update(
                        {
                            "message": "Order updated successfully",
                            "code": 200
                        }
        )

        return response