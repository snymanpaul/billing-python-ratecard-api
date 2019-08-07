# Using this package which is a HTTP library
import requests
 
# Parameters needed for ratecard API
subscription = 'your subscription ID'                 # replace with your Azure subscription ID
#token = '<bearerToken>'                              # need to determine token at runtime, implementation below
offer = 'MS-AZR-0003p'                                # PAYG offer
currency = 'USD'
locale = 'en-US'
region = 'US'
rateCardUrl = "https://management.azure.com:443/subscriptions/{subscriptionId}/providers/Microsoft.Commerce/RateCard?api-version=2016-08-31-preview&$filter=OfferDurableId eq '{offerId}' and Currency eq '{currencyId}' and Locale eq '{localeId}' and RegionInfo eq '{regionId}'".format(subscriptionId = subscription, offerId = offer, currencyId = currency, localeId = locale, regionId = region)

# Parameters needed for Oauth2 API
grant_type = 'client_credentials'                     # static
client_id = 'your client ID'                          # replace with your client ID (App registration in AAD) 
client_secret = 'your client secret'                  # replace with your client secret (from the same App registration)
resource = 'https://management.azure.com/'            # static
oauthUrl1 = 'https://login.microsoftonline.com/'      # static
tenant_id = 'yourAADtenant.onmicrosoft.com'           # replace with your AD tenant ID
oauthUr2 = '/oauth2/token'                            # static

# Prepare paramters to be sent to api for Oauth2 token
URL = oauthUrl1 + tenant_id + '/oauth2/token'

PARAMS = {  'grant_type':    grant_type, 
            'client_id':     client_id,
            'client_secret': client_secret, 
            'resource':      resource}

# Request an OAuth2 bearer token, sending post request and saving response as response object 
r1 = requests.post(url = URL, data = PARAMS)

# Extract the Oauth2 token from the response
token = r1.json()['access_token']

# Don't allow redirects and call the RateCard API
response = requests.get(rateCardUrl, allow_redirects=False, headers = {'Authorization': 'Bearer %s' %token})

# Look at response headers to get the redirect URL
redirectUrl = response.headers['Location']

# Get the ratecard content by making another call to go the redirect URL
rateCard = requests.get(redirectUrl)

# Print the ratecard content
print(rateCard.content) 