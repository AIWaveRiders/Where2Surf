import requests
import getpass
import json

def get_surfline_token(email: str, password: str) -> str:
    url = "https://services.surfline.com/trusted/token"
    payload = {
        "username": email,
        "password": password,
        "grant_type": "password"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    
    token = response.json().get("access_token")
    if not token:
        raise Exception("No access token found in response.")

    return token

if __name__ == "__main__":
    email = input("Enter your Surfline email: ")
    password = getpass.getpass("Enter your Surfline password: ")

    try:
        token = get_surfline_token(email, password)
        print("\n✅ Access token:")
        print(token)
    except Exception as e:
        print(f"❌ Error getting token: {e}")
