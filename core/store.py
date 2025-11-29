class ValorantStore:
    def __init__(self, auth_client):
        self.auth = auth_client
        self.region = auth_client.region

    def get_storefront(self):
        url = f"https://pd.{self.region}.a.pvp.net/store/v2/storefront/{self.auth.puuid}"
        headers = self.auth.get_headers()
        
        # Try v2 Storefront
        resp = self.auth.session.get(url, headers=headers)
        
        if resp.status_code == 404:
            url_v3 = f"https://pd.{self.region}.a.pvp.net/store/v3/storefront/{self.auth.puuid}"
            # v3 usually requires POST
            resp = self.auth.session.post(url_v3, headers=headers, json={})

        return resp.json()
