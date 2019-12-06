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
  with open('orders.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      line_count = line_count + 1
      ids.append(row[0])
    print(str(line_count) + " orders in list.")
  return ids

def address_complete(address):
  # Check that every mandatory field is filled out
  # all (k in address for k in('first_name', 'last_name', 'address_1', 'city', 'state', 'postcode', 'country'))
  #   print(k)
  # return address

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
    shipping = order['shipping']
    billing = order['billing']
    print(address_complete(shipping))
    print(address_complete(billing))

    # if address_complete(shipping) and not address_complete(billing):
    #   # data = {
    #   #   "billing": {
    #   #     "country": 
    #   #   }
    #   # }
    #   print(f"Editing order {num} of {num_orders}")
    #   print(wcapi.put(f"orders/{id}", data).json())

copy_shipping_to_billing()