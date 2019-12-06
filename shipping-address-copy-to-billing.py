# THIS FILE IS A WORK IN PROGRESS - NOT COMPLETE!

# Install:
# pip install woocommerce
# Put your API credentials in secretsEXAMPLE.py, and rename it to secrets.py
# Upload a .csv containing ONLY the order IDs you want to edit (see orders.csv as an example)

# Setup:
from woocommerce import API
from secrets import set_variables
import os
import csv

def check_environment():
  return all (k in os.environ for k in('STORE_URL', 'CONSUMER_KEY', 'CONSUMER_SECRET'))

def make_api():
  return API(
      url= os.environ['STORE_URL'],
      consumer_key= os.environ['CONSUMER_KEY'],
      consumer_secret= os.environ['CONSUMER_SECRET'],
      wp_api=True,
      version="wc/v3"
  )

def get_order_ids():
  ids = list()
  with open('orders2.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      line_count = line_count + 1
      ids.append(row[0])
    print(str(line_count) + " orders in list.")
  return ids

def check_address_complete(address):
  return bool(address['first_name']) and bool(address['last_name']) and bool(address['address_1']) and bool(address['city']) and bool(address['state']) and bool(address['postcode']) and bool(address['country'])

def copy_shipping_to_billing():
  set_variables()
  if check_environment():
    print("Authentication details are set.")
  else:
    print("You must set up your authentication details.")

  wcapi = make_api()
  order_ids = get_order_ids()
  num_orders = len(order_ids)

  for num, id in enumerate(order_ids):
    order = wcapi.get(f"orders/{id}").json()
    if 'shipping' in order:
      shipping = order['shipping']
      billing = order['billing']
      print(f"Processing order {num} of {num_orders}")
      if check_address_complete(shipping) and not check_address_complete(billing):
        print(f"going to copy this shipping address {shipping} into billing address {billing}")
        # data = {
        #   "billing": {
        #     "country": 
        #   }
        # }
        # print(wcapi.put(f"orders/{id}", data).json())

copy_shipping_to_billing()