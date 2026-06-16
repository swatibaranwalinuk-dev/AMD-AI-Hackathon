from services.asset_service import load_assets

class DiscoveryAgent:

    def discover(self):

        assets = load_assets()

        return assets
