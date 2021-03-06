# Install:
# pip install woocommerce
# Put your API credentials in secretsEXAMPLE.py, and rename it to secrets.py
# Upload a .csv containing ONLY the order IDs you want to edit (see orders.csv as an example). Please ensure you don't have a header row.

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

def fix_country(old_country, bill_state, ship_state):
  def check_if_usa(val):
    us_states = ["Alaska",
                    "Alabama",
                    "Arkansas",
                    "American Samoa",
                    "Arizona",
                    "California",
                    "Colorado",
                    "Connecticut",
                    "District of Columbia",
                    "Delaware",
                    "Florida",
                    "Georgia",
                    "Guam",
                    "Hawaii",
                    "Iowa",
                    "Idaho",
                    "Illinois",
                    "Indiana",
                    "Kansas",
                    "Kentucky",
                    "Louisiana",
                    "Massachusetts",
                    "Maryland",
                    "Maine",
                    "Michigan",
                    "Minnesota",
                    "Missouri",
                    "Mississippi",
                    "Montana",
                    "North Carolina",
                    " North Dakota",
                    "Nebraska",
                    "New Hampshire",
                    "New Jersey",
                    "New Mexico",
                    "Nevada",
                    "New York",
                    "Ohio",
                    "Oklahoma",
                    "Oregon",
                    "Pennsylvania",
                    "Puerto Rico",
                    "Rhode Island",
                    "South Carolina",
                    "South Dakota",
                    "Tennessee",
                    "Texas",
                    "Utah",
                    "Virginia",
                    "Virgin Islands",
                    "Vermont",
                    "Washington",
                    "Wisconsin",
                    "West Virginia",
                    "Wyoming"] + [ "AK",
                      "AL",
                      "AR",
                      "AS",
                      "AZ",
                      "CA",
                      "CO",
                      "CT",
                      "DC",
                      "DE",
                      "FL",
                      "GA",
                      "GU",
                      "HI",
                      "IA",
                      "ID",
                      "IL",
                      "IN",
                      "KS",
                      "KY",
                      "LA",
                      "MA",
                      "MD",
                      "ME",
                      "MI",
                      "MN",
                      "MO",
                      "MS",
                      "MT",
                      "NC",
                      "ND",
                      "NE",
                      "NH",
                      "NJ",
                      "NM",
                      "NV",
                      "NY",
                      "OH",
                      "OK",
                      "OR",
                      "PA",
                      "PR",
                      "RI",
                      "SC",
                      "SD",
                      "TN",
                      "TX",
                      "UT",
                      "VA",
                      "VI",
                      "VT",
                      "WA",
                      "WI",
                      "WV",
                      "WY"]
    return val in us_states
  def check_if_can(val):
    can_provs = ['Alberta', 
      'British Columbia', 
      'Manitoba', 
      'New Brunswick', 'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon Territory'] + ['AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
    return val in can_provs
  def check_us_can_au(val):
    if check_if_usa(val):
      return 'United States'
    elif check_if_can(val):
      return 'Canada'
    elif val == 'Queensland' or 'Australia' in val:
      return 'Australia'
    else:
      print(f'Can\'t find the country for {val}')
      return None
  if old_country == 'CA':
    return 'Canada'
  elif old_country == 'US':
    return 'United States'
  elif bill_state:
    return check_us_can_au(bill_state)
  elif ship_state:
    return check_us_can_au(ship_state)
  else:
    print("There was no billing or shipping states...")
    return None

def fix_country_reqs():
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
    new_country = fix_country(billing['country'], billing['state'], shipping['state'])
    if not new_country == None:
      data = {
        "billing": {
          "country": new_country
        }
      }
      print(f"Editing order {num} of {num_orders}")
      print(wcapi.put(f"orders/{id}", data).json())

fix_country_reqs()