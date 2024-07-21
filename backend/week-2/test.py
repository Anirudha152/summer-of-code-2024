import requests

url = 'http://localhost:5000'

def new_inventory_item():
    response = requests.post(url + '/inventory/add', json={
        'Item_SKU': 'SKU-0003',
        'Item_Name': 'Test Item',
        'Item_Description': 'Test Description',
        'Item_Price': 100.00,
        'Item_Qty': 100
    })
    print(response.json())

new_inventory_item()