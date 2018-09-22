import requests

url = 'https://www.miamidade.gov/PApublicServiceProxy/PaServicesProxy.ashx'

# without this header, the server will response json error: 
# 412 - Request is not coming from an authorized UI
HEADERS = {
    'Referer':'https://www.miamidade.gov/propertysearch/',
}

PARAMS = {
    'Operation':'GetPropertySearchByFolio',
    'clientAppName': 'PropertySearch',
}

def get_properties_by_folio(folio):
    """wallpaper for http requests, return json dict with contact properties
    
    Arguments:
        folio {int} -- folio number
    
    Returns:
        dict -- json properties of contact
    """
    params = {**PARAMS, **{'folioNumber': folio}}
    print(folio)
    response = requests.get(url, params=params, headers=HEADERS)
    
    if response.status_code != 200:
        response.raise_for_status()
    return response.json()

def replace_dash(folio):
    return int(folio.replace('-', ''))
