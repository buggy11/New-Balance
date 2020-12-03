import requests
import time
import lxml
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
                    

SESSION = requests.Session()

ATC_URL = "https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/Cart-AddProduct"

SHIPPING_SCRAPE_URL = "https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutShippingServices-UpdateShippingMethodsList"

SHIPPING_SUBMIT_URL = "https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutShippingServices-SubmitShipping"

PAYMENT_SUBMIT_URL = "https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutServices-SubmitPayment"

PLACE_ORDER_URL = "https://www.newbalance.com/on/demandware.store/Sites-NBUS-Site/en_US/CheckoutServices-PlaceOrder?termsconditions=undefined"

HEADERS_ATC = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "content-length": "1085",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "referer": "https://www.newbalance.com/checkout-begin/?stage=shipping",
    "referer": 'https://www.newbalance.com/pd/fresh-foam-roav-backpack/MROAVV1-33852.html',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",   
    "x-requested-with": "XMLHttpRequest"
}

HEADERS_SHIPPING = {
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

HEADERS_PAYMENT = {
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

ATC_DATA = {
    "pid": "739655529153", 
    "quantity": "1",
    "options": "[]",
}

SHIPPING_SCRAPE_DATA = {
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

PAYMENT_DATA = {
    "csrf_token":"",
    "localizedNewAddressTitle": "",
    "dwfrm_billing_paymentMethod": "",
    "dwfrm_billing_creditCardFields_cardNumber": "",
    "dwfrm_billing_creditCardFields_expirationMonth": "",
    "dwfrm_billing_creditCardFields_expirationYear": "",
    "dwfrm_billing_creditCardFields_securityCode": "",
    "dwfrm_billing_creditCardFields_cardType": "",
    "dwfrm_billing_realtimebanktransfer_iban": "",
    "dwfrm_billing_shippingAddressUseAsBillingAddress": "",
    "addressSelector": "",
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
    "dwfrm_billing_paymentMethod": "",
    "dwfrm_billing_creditCardFields_cardNumber": "",
    "dwfrm_billing_creditCardFields_expirationMonth": "",
    "dwfrm_billing_creditCardFields_expirationYear": "",
    "dwfrm_billing_creditCardFields_securityCode": "",
    "dwfrm_billing_creditCardFields_cardType": "",
    "dwfrm_billing_realtimebanktransfer_iban": "",
    "addressId": "",
    "saveBillingAddr": "false",
}

PLACE_ORDER_PARAMS = {
    "termsconditions": "undefined",
}




def task(num):
    ATC_RESPONSE = SESSION.post(url=ATC_URL, headers=HEADERS_ATC, data=ATC_DATA)
    ATC_CONTENT = ATC_RESPONSE.json()
    if ATC_CONTENT["message"] == "Product added to cart":
        print('added to cart')
    else:
        print('issue')


    SHIPMENT_SCRAPE_RESPONSE = SESSION.post(url=SHIPPING_SCRAPE_URL,headers=HEADERS_SHIPPING,data=SHIPPING_SCRAPE_DATA)
    SHIPMENT_SCRAPE_CONTENT = SHIPMENT_SCRAPE_RESPONSE.json()
    SHIPMENT_SCRAPE_UUID =  SHIPMENT_SCRAPE_CONTENT['order']['items']['items'][0]['shipmentUUID']

    SHIPPING_CRSF_RESPONSE = SESSION.get("https://www.newbalance.com/checkout-begin/?stage=shipping#shipping")

    INITIAL_SCRAPE = BeautifulSoup(SHIPPING_CRSF_RESPONSE.text, 'lxml')

    TOKEN = INITIAL_SCRAPE.find('input', {'name':'csrf_token'})['value']



    SHIPPING_DATA = {
    'originalShipmentUUID': SHIPMENT_SCRAPE_UUID,
    'shipmentUUID': SHIPMENT_SCRAPE_UUID,
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
    'csrf_token': TOKEN,
    'saveShippingAddr': 'false',
}
    
    try: 
        SHIPPING_RESPONSE = SESSION.post(url=SHIPPING_SUBMIT_URL,headers=HEADERS_SHIPPING,data=SHIPPING_DATA)
        SHIPPING_CONTENT = SHIPPING_RESPONSE.json()
        if SHIPPING_CONTENT["action"] == "CheckoutShippingServices-SubmitShipping":
            print('submitted shipping')
        else:
            print('issue')
    except:
        print('Failed to submit shipping.')

    PAYMENT_DATA = {
        "csrf_token":TOKEN,
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
        "dwfrm_billing_addressFields_country": "US",
        "dwfrm_billing_addressFields_firstName": "",
        "dwfrm_billing_addressFields_lastName": "",
        "dwfrm_billing_addressFields_address1": "",
        "dwfrm_billing_addressFields_address2": "",
        "dwfrm_billing_addressFields_city": "",
        "dwfrm_billing_addressFields_states_stateCode": "GA",
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
        PAYMENT_RESPONSE = SESSION.post(url=PAYMENT_SUBMIT_URL,headers=HEADERS_PAYMENT,data=PAYMENT_DATA)
        PAYMENT_CONTENT = PAYMENT_RESPONSE.json()
        if PAYMENT_CONTENT["action"] == "CheckoutServices-SubmitPayment":
            print('payment submitted')
        else:
            print('issue')
    except:
        print('issue')

    PLACE_ORDER_HEADERS = {
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
    
    PLACE_ORDER_RESPONSE = SESSION.post(url=PLACE_ORDER_URL,headers=PLACE_ORDER_HEADERS,params=PLACE_ORDER_PARAMS)
    PLACE_ORDER_CONTENT = PLACE_ORDER_RESPONSE.json()
    if PLACE_ORDER_CONTENT['error'] == False:
        print('payment success')
        WEBHOOK_ADDRESS_PARSE = SHIPPING_CONTENT["order"]["items"]["items"][0]["images"]["productDetail"][0]["src"]
        WEBHOOK_PRICE_PARSE = SHIPPING_CONTENT["order"]["items"]["items"][0]["price"]["sales"]["formatted"]
        WEBHOOK_NAME_PARSE = SHIPMENT_SCRAPE_CONTENT["order"]["items"]["items"][0]["productName"]
        WEBHOOK_URL = DiscordWebhook(url="https://discord.com/api/webhooks/781001274388250656/p_8bOP35K4lQJ5zm2M0Hxs5kdIijdSYSnKpJCXU4Ba3_Ppc19rFShEOGvYRmQfLlJQNp")
        embed = DiscordEmbed(title='Checked out!',color=000000)
        embed.set_footer(text='Cobra')
        embed.set_timestamp()
        embed.add_embed_field(name="Site: ", value="New Balance", inline=False)
        embed.add_embed_field(name="Product: ",value=WEBHOOK_NAME_PARSE, inline=False)
        embed.add_embed_field(name="Price: ",value=WEBHOOK_PRICE_PARSE)
        embed.add_embed_field(name="Mode: ",value="Fast")
        embed.set_thumbnail(url=WEBHOOK_ADDRESS_PARSE)
        WEBHOOK_URL.add_embed(embed)
        response = WEBHOOK_URL.execute()


    elif PLACE_ORDER_CONTENT['error'] == True:
        print('Payment declined')
        WEBHOOK_ADDRESS_PARSE = SHIPPING_CONTENT["order"]["items"]["items"][0]["images"]["productDetail"][0]["src"]
        WEBHOOK_PRICE_PARSE = SHIPPING_CONTENT["order"]["items"]["items"][0]["price"]["sales"]["formatted"]
        WEBHOOK_NAME_PARSE = SHIPMENT_SCRAPE_CONTENT["order"]["items"]["items"][0]["productName"]
        WEBHOOK_URL = DiscordWebhook(url="")
        embed = DiscordEmbed(title='Fix your info! / Declined.',color=000000)
        embed.set_footer(text='Your bot')
        embed.set_timestamp()
        embed.add_embed_field(name="Site: ", value="New Balance", inline=False)
        embed.add_embed_field(name="Product: ",value=WEBHOOK_NAME_PARSE, inline=False)
        embed.add_embed_field(name="Price: ",value=WEBHOOK_PRICE_PARSE)
        embed.add_embed_field(name="Mode: ",value="Fast")
        embed.set_thumbnail(url=WEBHOOK_ADDRESS_PARSE)
        WEBHOOK_URL.add_embed(embed)
        response = WEBHOOK_URL.execute()
    else:
        print('issue')
