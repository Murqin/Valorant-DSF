import tls_client
import json
import getpass

def debug_login():
    print("=== Valorant DSF Auth Debugger ===")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    session = tls_client.Session(
        client_identifier="chrome_112",
        random_tls_extension_order=True
    )

    # 1. Initial Auth Request
    print("\n[1] Sending Initial Auth Request...")
    auth_url = "https://auth.riotgames.com/api/v1/authorization"
    auth_data = {
        "client_id": "play-valorant-web-prod",
        "nonce": "1",
        "redirect_uri": "https://playvalorant.com/opt_in",
        "response_type": "token id_token",
        "scope": "account openid"
    }
    
    resp1 = session.post(auth_url, json=auth_data)
    print(f"Status: {resp1.status_code}")

    # 2. Submit Credentials
    print("\n[2] Submitting Credentials...")
    login_data = {
        "type": "auth",
        "username": username,
        "password": password
    }
    resp2 = session.put(auth_url, json=login_data)
    
    print(f"Status: {resp2.status_code}")
    try:
        data = resp2.json()
        print("Response Body:")
        print(json.dumps(data, indent=2))
        
        if "error" in data:
            print(f"\n[!] Error Detected: {data['error']}")
        
        if "response" in data:
            print("\n[+] Auth Success! URI found.")
        else:
            print("\n[-] No 'response' object found. Check the JSON output above for details.")
            
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        print(resp2.text)

if __name__ == "__main__":
    debug_login()
