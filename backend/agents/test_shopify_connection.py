import sys
sys.path.append('backend/agents')

from shopify_auth import ShopifyAuth

try:
    print("=" * 60)
    print("TESTING SHOPIFY CONNECTION")
    print("=" * 60)
    
    # Connect to Shopify
    auth = ShopifyAuth()
    
    # Test 1: Get Products
    print("\n📦 Fetching products...")
    products = auth.get("/products.json?limit=5")
    product_list = products.get("products", [])
    print(f"✅ Found {len(product_list)} products")
    
    for p in product_list[:3]:
        title = p["title"]
        price = p.get("variants", [{}])[0].get("price", "N/A")
        inventory = p.get("variants", [{}])[0].get("inventory_quantity", "N/A")
        print(f"  - {title} (${price}) - Stock: {inventory}")
    
    # Test 2: Get Orders
    print("\n📋 Fetching open orders...")
    orders = auth.get("/orders.json?status=open&limit=5")
    order_list = orders.get("orders", [])
    print(f"✅ Found {len(order_list)} open orders")
    
    for o in order_list[:3]:
        print(f"  - Order {o['name']}: ${o['total_price']} ({o['financial_status']})")
    
    # Test 3: Get Inventory
    print("\n📊 Checking inventory levels...")
    for p in product_list[:2]:
        variant_id = p.get("variants", [{}])[0].get("id")
        if variant_id:
            inventory = auth.get(f"/inventory_levels.json?inventory_item_ids={variant_id}")
            print(f"  - {p['title']}: {inventory.get('inventory_levels', [])}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Check .env file has correct SHOPIFY_ACCESS_TOKEN")
    print("2. Verify token has 'read_products' and 'read_orders' permissions")
    print("3. Ensure shop name is correct (sureshchouhanm)")