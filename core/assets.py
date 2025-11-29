import tls_client

class AssetManager:
    def __init__(self):
        self.skins = {}
        self.load_assets()

    def load_assets(self):
        session = tls_client.Session(client_identifier="chrome_112")
        
        try:
            resp = session.get("https://valorant-api.com/v1/weapons/skins?language=en-US")
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                for skin in data:
                    # Index by the main skin UUID
                    self.skins[skin["uuid"]] = {
                        "name": skin["displayName"],
                        "icon": skin["displayIcon"],
                        "tier": skin.get("contentTierUuid")
                    }
                    # Also index by each level UUID (Store returns Level UUIDs)
                    for level in skin.get("levels", []):
                        self.skins[level["uuid"]] = {
                            "name": skin["displayName"], # Or level["displayName"] if different
                            "icon": level["displayIcon"] or skin["displayIcon"], # Level icon preferred
                            "tier": skin.get("contentTierUuid")
                        }

        except Exception as e:
            print(f"Failed to load assets: {e}")

    def get_skin_data(self, uuid):
        return self.skins.get(uuid, {"name": "Unknown Skin", "icon": None})
