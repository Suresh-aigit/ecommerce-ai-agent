from shopify_auth import ShopifyAuth

class ShopifyInventoryAgent:
    def __init__(self, auth):
        self.auth = auth
    
    def get_all_products(self):
        result = self.auth.get("/products.json")
        products = result.get("products", [])
        return {
            "total": len(products),
            "products": [
                {
                    "id": p["id"],
                    "title": p["title"],
                    "sku": p.get("variants", [{}])[0].get("sku", "N/A"),
                    "stock": p.get("variants", [{}])[0].get("inventory_quantity", 0),
                    "price": p.get("variants", [{}])[0].get("price", 0)
                }
                for p in products
            ]
        }
    
    def check_low_stock(self, threshold=5):
        all_products = self.get_all_products()
        low_stock = [p for p in all_products["products"] if int(p["stock"]) <= threshold]
        return {
            "threshold": threshold,
            "low_stock_count": len(low_stock),
            "products": low_stock
        }
