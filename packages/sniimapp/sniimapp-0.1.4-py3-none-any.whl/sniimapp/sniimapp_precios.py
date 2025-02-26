import requests

class sniimapp_precios:
    def __init__(self, base_url, db_name, username, password):
        self.base_url = base_url
        self.db_name = db_name
        self.username = username
        self.password = password
        self.session = requests.Session()
        self._authenticate()

    def _authenticate(self):
        login_url = f"{self.base_url}/web/session/authenticate"
        login_data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "db": self.db_name,
                "login": self.username,
                "password": self.password,
            },
        }
        response = self.session.post(login_url, json=login_data)
        response.raise_for_status()

    def get_sniim_productos(self, product_key):
        api_url = f"{self.base_url}/api/get_sniim_productos"
        params = {"clave_producto": product_key} if clave_producto else {}
        response = self.session.get(api_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_sniim_precios(self, product_key, date_start, date_end, limit=50, offset=0):
        product_name = get_sniim_producto(product_key)['products'][0]['nombre_producto']
        product_type = get_sniim_producto(product_key)['products'][0]['tipo_producto']
        api_url = f"{self.base_url}/api/get_sniim_precios"
        params = {
            "product": product_name,
            "product_type": product_type,
            "date_start": date_start,
            "date_end": date_end,
            "limit": limit,
            "offset": offset,
        }
        response = self.session.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
