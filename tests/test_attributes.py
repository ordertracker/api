import json

def test_products_attribute_add_not_authorized(client):
    res = client.post(
        '/api/products/attribute/add',
        data=json.dumps(
            {
                "product_id": "123",
                "attribute_id": "123",
                "attribute_key": "test_attr_key",
                "attribute_value": "test_attr_value"
            }
        ),
        content_type='application/json'
    )
    assert res.status_code == 401

def test_products_attribute_add_success(client):
    res = client.post(
        '/api/products/attribute/add',
        headers={
            "API-TOKEN": "test_apitoken_test_apitoken"  
        },
        data=json.dumps(
            {
                "product_id": "123",
                "attribute_id": "123",
                "attribute_key": "test_attr_key",
                "attribute_value": "test_attr_value"
            }
        ),
        content_type='application/json'
    )
    assert res.status_code == 200   