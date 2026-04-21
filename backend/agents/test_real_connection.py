import sys
sys.path.append('backend/agents')

from shopify_auth import ShopifyAuth

try:
    print("Connecting to Shopify...")
    auth = ShopifyAuth()
    
    print("\nFetching your real products...")
    products = auth.get("/products.json?limit=5")
    
    print(f"SUCCESS! Found {len(products.get('products', []))} products")
    
    for p in products.get("products", [])[:3]:
        title = p['title']
        price = p.get('variants', [{}])[0].get('price', 'N/A')
        print(f"  - {title} (Price: ${price})")
        
    print("\nFetching orders...")
    orders = auth.get("/orders.json?status=open&limit=5")
    print(f"Found {len(orders.get('orders', []))} open orders")
    
    for o in orders.get("orders", [])[:2]:
        print(f"  - Order {o['name']}: ${o['total_price']}")
        
except Exception as e:
    print(f"\nERROR: {e}")
    print("\nCheck your .env file has real credentials")