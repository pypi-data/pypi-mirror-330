import requests

def build(data):
    try:
        response = requests.get(f"https://evm-build.netlify.app/.netlify/functions/api/{data}")
        return response  # Return the response object instead of None for more utility
    except requests.RequestException as e:
        return None  # Return None if there's an error