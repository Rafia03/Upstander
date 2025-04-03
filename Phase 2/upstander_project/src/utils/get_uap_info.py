

#import pandas as pd
##TODO



# Load UAP data
#uap_data = pd.read_csv("uap_locations.csv")

def get_uap_info(uap_number):
    info = uap_data[uap_data['UAP Number'] == uap_number]
    if not info.empty:
        return info.to_dict('records')[0]
    return None

def get_uap_info(uap_number):
    # This function retrieves information about UAP locations based on the provided UAP number.
    # For demonstration purposes, let's assume we have a predefined dictionary of UAP information.
    
    uap_data = {
        102: {"Location": "Location A"},
        105: {"Location": "Location B"},
        106: {"Location": "Location C"},
        107: {"Location": "Location D"},
        201: {"Location": "Location E"},
        202: {"Location": "Location F"},
        203: {"Location": "Location G"},
        204: {"Location": "Location H"},
        205: {"Location": "Location I"},
    }
    
    return uap_data.get(uap_number, None)