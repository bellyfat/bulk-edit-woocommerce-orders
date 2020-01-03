# THIS FILE IS A WORK IN PROGRESS - NOT COMPLETE!

# Install:
# pip install woocommerce
# Put your API credentials in secretsEXAMPLE.py, and rename it to secrets.py
# Upload a .csv containing ONLY the order IDs you want to edit (see orders.csv as an example)

# Billing and shipping addresses have this format:
# {'first_name': 'First', 'last_name': 'Last', 'company': '', 'address_1': '213 Street Rd', 'address_2': '#101', 'city': 'Cityname', 'state': 'CA', 'postcode': '90210', 'country': 'US'}

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

def check_address_complete(address):
  return bool(address['first_name']) and bool(address['last_name']) and bool(address['address_1']) and bool(address['city']) and bool(address['state']) and bool(address['postcode']) and bool(address['country'])

def convert_state(state):
  states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming',
    'AB': 'Alberta',
    'BC': 'British Columbia',
    'MB': 'Manitoba',
    'NB': 'New Brunswick',
    'NL': 'Newfoundland And Labrador',
    'NT': 'Northwest Territories',
    'NS': 'Nova Scotia',
    'NU': 'Nunavut',
    'ON': 'Ontario',
    'PE': 'Prince Edward Island',
    'QC': 'Quebec',
    'SK': 'Saskatchewan',
    'YT': 'Yukon'
  }
  if len(state) <= 2:
    return state
  else:
    case_matched = state.title()
    for k, v in states.items():
      if v == case_matched:
        return k
  return state

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
        data = {
          "billing": {
            # Country is handled in order-country.py
            "first_name"  : shipping['first_name'],
            "last_name"   : shipping['last_name'],
            "company"     : shipping['company'],
            "address_1"   : shipping['address_1'],
            "address_2"   : shipping['address_2'],
            "city"        : shipping['city'],
            "state"       : convert_state(shipping['state']),
          }
        }
        print(f"Sending this data to the Woo API: {data}")
        print(wcapi.put(f"orders/{id}", data).json())

copy_shipping_to_billing()