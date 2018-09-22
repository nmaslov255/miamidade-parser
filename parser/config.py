folio = '0821220330230'

url = 'https://www.miamidade.gov/PApublicServiceProxy/PaServicesProxy.ashx'

# without this header, the server will response json error: 
# 412 - Request is not coming from an authorized UI
headers = {
    'Referer':'https://www.miamidade.gov/propertysearch/',
}

params = {
    'Operation':'GetPropertySearchByFolio',
    'clientAppName': 'PropertySearch',
    'folioNumber': folio,
}