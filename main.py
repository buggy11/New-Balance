import requests
import time
import lxml
from datetime import datetime
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed


atc_url = "https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/Cart-AddProduct"

shipping_scrape_url = "https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutShippingServices-UpdateShippingMethodsList"

shipping_submit_url = "https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutShippingServices-SubmitShipping"

payment_submit_url = "https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutServices-SubmitPayment"

place_order_url = "https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutServices-PlaceOrder?termsconditions=undefined"

headers_atc = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "content-length": "1085",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "referer": 'https://www.newbalance.com/pd/fresh-foam-roav-backpack/MROAVV1-33852.html',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",   
    "x-requested-with": "XMLHttpRequest"
}

headers_shipping = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "content-length": "1085",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.newbalance.com",
    "referer": "https://www.newbalance.com/checkout-begin/?stage=shipping",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",   
    "x-requested-with": "XMLHttpRequest"
}

headers_payment = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'content-length': '1443',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.newbalance.com',
    'referer': 'https://www.newbalance.com/checkout-begin/?stage=payment',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'x-dtpc': '3$331260293_794h21vHUNWQFRFFRARMNOCKBROKATVPUANTRAJ-0e15'
}

atc_data = {
    "pid": "193684933730", 
    "quantity": "1",
    "options": "[]",
}

shipping_scrape_data = {
    "firstName": "",
    "lastName": "",
    "address1": "",
    "address2": "",
    "city": "",
    "postalCode": "",
    "stateCode": "",
    "countryCode": "",
    "phone": "",
    "shipmentUUID": "",
}

place_order_params = {
    "termsconditions": "undefined",
}

def task():
        
    session = requests.Session()

    atc_response = session.post(url=atc_url, headers=headers_atc, data=atc_data)
    atc_content = atc_response.json()
    if atc_content["message"] == "Product added to cart":
        print('added to cart')
    else:
        logging.debug('issue')


    shipment_scrape_response = session.post(url=shipping_scrape_url,headers=headers_shipping,data=shipping_scrape_data)
    shipment_scrape_content = shipment_scrape_response.json()
    shipment_scrape_uuid =  shipment_scrape_content['order']['items']['items'][0]['shipmentUUID']

    shipping_csrf_response = session.get("https://www.newbalance.com/checkout-begin/?stage=shipping#shipping")

    initial_scrape = BeautifulSoup(shipping_csrf_response.text, 'lxml')

    token = initial_scrape.find('input', {'name':'csrf_token'})['value']



    shipping_data = {
    'originalShipmentUUID': shipment_scrape_uuid,
    'shipmentUUID': shipment_scrape_uuid,
    'zipCodeErrorMsg': 'Please enter a valid Zip/Postal code',
    "shipmentSelector": "new",
    'dwfrm_shipping_shippingAddress_addressFields_country': '',
    'dwfrm_shipping_shippingAddress_addressFields_firstName': '',
    'dwfrm_shipping_shippingAddress_addressFields_lastName': '',
    'dwfrm_shipping_shippingAddress_addressFields_address1': '',
    'dwfrm_shipping_shippingAddress_addressFields_address2': '',
    'dwfrm_shipping_shippingAddress_addressFields_city': '',
    'dwfrm_shipping_shippingAddress_addressFields_states_stateCode': '',
    'dwfrm_shipping_shippingAddress_addressFields_postalCode': '',
    'dwfrm_shipping_shippingAddress_addressFields_phone': '',
    'dwfrm_shipping_shippingAddress_addressFields_email': '',
    'dwfrm_shipping_shippingAddress_addressFields_addtoemaillist': '',
    'csrf_token': token,
    'saveShippingAddr': 'false',
}
    
    try: 
        shipping_response = session.post(url=shipping_submit_url,headers=headers_shipping,data=shipping_data)
        shipping_content = shipping_response.json()
        if shipping_content["action"] == "CheckoutShippingServices-SubmitShipping":
            print('submitted shipping')
        else:
            print('issue')
    except:
        print('Failed to submit shipping.')

    payment_data = {
        "csrf_token":token,
        "localizedNewAddressTitle": "New Address",
        "dwfrm_billing_paymentMethod": "CREDIT_CARD",
        "dwfrm_billing_creditCardFields_cardNumber": "",
        "dwfrm_billing_creditCardFields_expirationMonth": "",
        "dwfrm_billing_creditCardFields_expirationYear": "",
        "dwfrm_billing_creditCardFields_securityCode": "",
        "dwfrm_billing_creditCardFields_cardType": "",
        "dwfrm_billing_realtimebanktransfer_iban": "",
        "dwfrm_billing_shippingAddressUseAsBillingAddress": "true",
        "addressSelector": "21867dd2bbe4cf8d84b4e429c3",
        "select": "on",
        "dwfrm_billing_addressFields_country": "",
        "dwfrm_billing_addressFields_firstName": "",
        "dwfrm_billing_addressFields_lastName": "",
        "dwfrm_billing_addressFields_address1": "",
        "dwfrm_billing_addressFields_address2": "",
        "dwfrm_billing_addressFields_city": "",
        "dwfrm_billing_addressFields_states_stateCode": "",
        "dwfrm_billing_addressFields_postalCode": "",
        "dwfrm_billing_addressFields_phone": "",
        "dwfrm_billing_paymentMethod": "CREDIT_CARD",
        "dwfrm_billing_creditCardFields_cardNumber": "",
        "dwfrm_billing_creditCardFields_expirationMonth": "",
        "dwfrm_billing_creditCardFields_expirationYear": "",
        "dwfrm_billing_creditCardFields_securityCode": "",
        "dwfrm_billing_creditCardFields_cardType": "",
        "dwfrm_billing_realtimebanktransfer_iban": "",
        "addressId": "new",
        "saveBillingAddr": "false",
}
    try:
        payment_response = session.post(url=payment_submit_url,headers=headers_payment,data=payment_data)
        payment_content = payment_response.json()
        if payment_content["action"] == "CheckoutServices-SubmitPayment":
            print('payment submitted')
        else:
            print('issue')
    except:
            print('issue')

    place_order_headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.newbalance.com',
        'referer': 'https://www.newbalance.com/checkout-begin/?stage=placeOrder',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'x-dtpc': '3$331260293_794h28vHUNWQFRFFRARMNOCKBROKATVPUANTRAJ-0e17'
    }
    
    place_order_response = session.post(url=place_order_url,headers=place_order_headers,params=place_order_params)
    place_order_content = place_order_response.json()
    if place_order_content['error'] == False:
        print('Checkout success.')
        webhook_image_parse = shipping_content["order"]["items"]["items"][0]["images"]["productDetail"][0]["src"]
        webhook_price_parse = shipping_content["order"]["items"]["items"][0]["price"]["sales"]["formatted"]
        webhook_product_parse = shipment_scrape_content["order"]["items"]["items"][0]["productName"]
        webhook_url = DiscordWebhook(url="https://discord.com/api/webhooks/784942912768311296/mTLRXlZKIGsP5nQTvNujG2yA_bR59LYBTAa8ZHI-qdbM8OHlbuE2Yi2SWReTvsZroWEk")
        embed = DiscordEmbed(title='Checked out!',color=000000)
        embed.set_footer(text='Cobra')
        embed.set_timestamp()
        embed.add_embed_field(name="Site: ", value="New Balance", inline=False)
        embed.add_embed_field(name="Product: ",value=webhook_product_parse, inline=False)
        embed.add_embed_field(name="Price: ",value=webhook_price_parse)
        embed.add_embed_field(name="Mode: ",value="Fast")
        embed.set_thumbnail(url=webhook_image_parse)
        webhook_url.add_embed(embed)
        response = webhook_url.execute()
        
    elif place_order_content['error'] == True:
        print('Payment declined')
        webhook_image_parse = shipping_content["order"]["items"]["items"][0]["images"]["productDetail"][0]["src"]
        webhook_price_parse = shipping_content["order"]["items"]["items"][0]["price"]["sales"]["formatted"]
        webhook_product_parse = shipment_scrape_content["order"]["items"]["items"][0]["productName"]
        webhook_url = DiscordWebhook(url="https://discord.com/api/webhooks/784942912768311296/mTLRXlZKIGsP5nQTvNujG2yA_bR59LYBTAa8ZHI-qdbM8OHlbuE2Yi2SWReTvsZroWEk")
        embed = DiscordEmbed(title='Payment declined.',color=000000)
        embed.set_footer(text='Cobra')
        embed.set_timestamp()
        embed.add_embed_field(name="Site: ", value="New Balance", inline=False)
        embed.add_embed_field(name="Product: ",value=webhook_product_parse, inline=False)
        embed.add_embed_field(name="Price: ",value=webhook_price_parse)
        embed.add_embed_field(name="Mode: ",value="Fast")
        embed.set_thumbnail(url=webhook_image_parse)
        webhook_url.add_embed(embed)
        response = webhook_url.execute()
      
    else:
        print('issue')
task()
