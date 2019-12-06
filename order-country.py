# Install:
# pip install woocommerce
# Put your API credentials in secretsEXAMPLE.py, and rename it to secrets.py

# Setup:
from woocommerce import API
from secrets import set_variables
import os

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

set_variables()
if check_environment():
  print("Authentication details are set.")
else:
  print("You must set up your authentication details.")

wcapi = make_api()

print(wcapi.get("orders/727").json())
