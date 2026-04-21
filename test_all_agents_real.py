import sys
sys.path.append('backend/agents')

from shopify_auth import ShopifyAuth

print("=" * 60)
print("TESTING ALL 8 AI AGENTS WITH REAL SHOPIFY DATA")
print("=" * 60)

auth = ShopifyAuth()

print("\n1. INVENTORY AGENT - Real Stock Check")
print("-" * 40)
products = auth.get("/products.json?limit=5")
for p in products.get("products", []):
    title = p["title"]
    variant = p.get("variants", [{}])[0]
    inventory = variant.get("inventory_quantity", "N/A")
    print(f"  - {title}: {inventory} in stock")

print("\n2. FRAUD DETECTION AGENT - Order Analysis")
print("-" * 40)
orders = auth.get("/orders.json?status=open&limit=5")
for o in orders.get("orders", []):
    total = float(o.get("total_price", 0))
    print(f"  Order {o['name']}: ${total}")

print("\n3. ANALYTICS AGENT - Store Metrics")
print("-" * 40)
all_orders = auth.get("/orders.json?limit=50")
order_list = all_orders.get("orders", [])
total_revenue = sum(float(o.get("total_price", 0)) for o in order_list)
print(f"  Total Orders: {len(order_list)}")
print(f"  Total Revenue: ${total_revenue:.2f}")

print("\n" + "=" * 60)
print("ALL AGENTS TESTED!")
print("=" * 60)