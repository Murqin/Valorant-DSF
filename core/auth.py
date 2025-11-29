import tls_client
import re
import urllib.parse

class RiotAuth:
    def __init__(self):
        self.session = tls_client.Session(
            client_identifier="chrome_112",
            random_tls_extension_order=True
        )
        self.access_token = None
        self.id_token = None
        self.entitlements_token = None
        self.puuid = None
        self.region = "eu" # Default to EU
        self.client_version = "release-07.08-shipping-20-998585" # Default client version

    def extract_tokens_from_url(self, url_string):
        """
        Extracts access_token and id_token from the provided URL string.
        Then fetches entitlements and userinfo.
        """
        # Handle cases where user might paste just the fragment or full URL
        # We look for access_token=... and id_token=...
        
        # Decode URL just in case, though regex usually handles it
        decoded_url = urllib.parse.unquote(url_string)

        # Security Check: Validate Domain
        if not re.match(r"^https://(auth\.riotgames\.com|playvalorant\.com)", decoded_url):
            return False, "Invalid URL domain. Must be from Riot Games."

        access_token_match = re.search(r"access_token=([^&]*)", decoded_url)
        id_token_match = re.search(r"id_token=([^&]*)", decoded_url)

        if not access_token_match or not id_token_match:
            return False, "Could not find tokens in the provided URL."

        self.access_token = access_token_match.group(1)
        self.id_token = id_token_match.group(1)

        # Now get entitlements and PUUID
        if not self._fetch_entitlements_and_userinfo():
            return False, "Failed to fetch entitlements or user info."

        # Detect Region
        if not self._fetch_region():

            self.region = "eu"

        # Fetch Client Version
        self._fetch_client_version()
        

        return True, "Success"

    def _fetch_entitlements_and_userinfo(self):
        try:
            # 1. Get Entitlements
            ent_url = "https://entitlements.auth.riotgames.com/api/token/v1"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            ent_resp = self.session.post(ent_url, headers=headers, json={})
            
            if ent_resp.status_code != 200:

                return False
            
            self.entitlements_token = ent_resp.json().get("entitlements_token")

            # 2. Get User Info (PUUID)
            userinfo_url = "https://auth.riotgames.com/userinfo"
            user_resp = self.session.get(userinfo_url, headers=headers)
            
            if user_resp.status_code != 200:

                return False
                
            self.puuid = user_resp.json().get("sub")
            return True
            
        except Exception as e:

            return False

    def _fetch_region(self):
        try:
            url = "https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            resp = self.session.put(url, headers=headers, json={"id_token": self.id_token})
            
            if resp.status_code != 200:

                return False
            
            data = resp.json()
            # Response example: {'token': '...', 'affinities': {'live': 'eu'}}
            self.region = data.get("affinities", {}).get("live", "eu")
            return True
        except Exception as e:

            return False

    def _fetch_client_version(self):
        try:
            resp = self.session.get("https://valorant-api.com/v1/version")
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                self.client_version = data.get("riotClientVersion", "release-07.08-shipping-20-998585")
            else:
                self.client_version = "release-07.08-shipping-20-998585"
        except:
            self.client_version = "release-07.08-shipping-20-998585"

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "X-Riot-Entitlements-JWT": self.entitlements_token,
            "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
            "X-Riot-ClientVersion": getattr(self, 'client_version', "release-07.08-shipping-20-998585")
        }
