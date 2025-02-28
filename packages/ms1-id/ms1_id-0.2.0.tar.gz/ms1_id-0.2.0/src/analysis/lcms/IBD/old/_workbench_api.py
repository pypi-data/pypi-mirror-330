import requests
import json


def get_inchikey_from_refmet_name(refmet_name):
    base_url = "https://www.metabolomicsworkbench.org/rest/refmet/name/"
    url = f"{base_url}{refmet_name}/inchi_key"

    try:
        response = requests.get(url)
        data = json.loads(response.text)
        return data['inchi_key'] if data else None
    except:
        return None

# Example usage:
# inchikey = get_inchikey_from_refmet_name("Cholesterol")
# print(inchikey)


def get_refmet_name_from_inchikey(inchikey):
    base_url = "https://www.metabolomicsworkbench.org/rest/refmet/inchi_key/"
    url = f"{base_url}{inchikey}/name"

    try:
        response = requests.get(url)
        data = json.loads(response.text)
        return data['name'] if data else None
    except:
        return None

# Example usage:
# refmet_name = get_refmet_name_from_inchikey("HVYWMOMLDIMFJA-DPAQBDIFSA-N")
# print(refmet_name)


def get_all_info_from_inchikey(inchikey):
    base_url = "https://www.metabolomicsworkbench.org/rest/compound/inchi_key/"
    url = f"{base_url}{inchikey}/all"

    try:
        response = requests.get(url)
        data = json.loads(response.text)
        return data if data else None
    except:
        return None

# Example usage:
# all_info = get_all_info_from_inchikey("HVYWMOMLDIMFJA-DPAQBDIFSA-N")
# print(json.dumps(all_info, indent=2))