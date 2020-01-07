# Bulk Edit Woocommerce Orders

Some utilities for bulk editing WooCommerce orders using the Woo Rest API. These are utilities I've written for clients, open sourced. You may require modifications for your use case, however this is meant as a starting point for bulk editing many woocommerce order values at once. 

If you want help for your custom use case, please contact me at rachel@rachelgould.dev

## Order Country

Due to importing orders from another system, some orders in WooCommerce ended up with their billing/shipping country blank. This method normalizes country values, and reuploads the order with shipping country copied to billing.

## Copy Shipping Address to Billing Address

Again, from our data import some other orders have shipping address details but no billing address. If this is true, we want to copy shipping address details to billing. 

# Usage

1. `pip install woocommerce`
2. Put your API credentials in secretsEXAMPLE.py, and rename it to secrets.py
3. Upload a .csv containing ONLY the order IDs you want to edit (see orders.csv as an example). Please ensure you don't have a header row.
4. Depending on the functionality you want:
`python order-country.py` or `python shipping-address-copy-to-billing.py`

## Disclaimer

Please use these scripts at your own risk. They are specific to my use case and may need to be modified to suit yours. Feel free to fork this repo and make any edits necessary. 