# Bulk Edit Woocommerce Orders

Some utilities for bulk editing WooCommerce orders using the Woo Rest API. These are utilities I've written for clients, open sourced. You may require modifications for your use case, however this is meant as a starting point for bulk editing many woocommerce order values at once. 

If you want help for your custom use case, please contact me at rachel@rachelgould.dev

## Order Country

Due to importing orders from another system, some orders in WooCommerce ended up with their billing/shipping country blank. This method normalizes country values, and reuploads the order with shipping country copied to billing.

## Copy Shipping Address to Billing Address

Again, from our data import some other orders have shipping address details but no billing address. If this is true, we want to copy shipping address details to billing. 
