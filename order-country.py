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

set_variables()
if check_environment():
  print("Authentication details are set.")
else:
  print("You must set up your authentication details.")

wcapi = make_api()
order_ids = get_order_ids()

for id in order_ids:
  print(id)
  print(wcapi.get("orders/{id}").json())
