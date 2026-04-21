import os
import sys
sys.path.append('backend/agents')

from dotenv import load_dotenv
from shopify_auth import ShopifyAuth
from shopify_inventory_agent import ShopifyInventoryAgent

load_dotenv()

store_url = os.getenv("SHOPIFY_STORE_URL")
token = os.getenv("SHOPIFY_ACCESS_TOKEN")

print("=" * 60)
print("TESTING SHOPIFY CONNECTION")
print("=" * 60)

# Check credentials
if not store_url or "your" in store_url:
    print("\n❌ ERROR: Missing SHOPIFY_STORE_URL in .env")
    exit()
if not token or len(token) < 20:
    print("\n❌ ERROR: Missing or invalid SHOPIFY_ACCESS_TOKEN")
    exit()

print(f"\nStore URL: {store_url}")
print(f"Token: {token[:10]}...")

try:
    auth = ShopifyAuth(store_url, token)
    agent = ShopifyInventoryAgent(auth)
    
    print("\n1. FETCHING PRODUCTS...")
    products = agent.get_all_products()
    print(f"   Total products: {products['total']}")
    
    if products['total'] > 0:
        for p in products["products"][:5]:
            print(f"   - {p['title'][:40]:<40} | Stock: {p['stock']:>3} | ₹{p['price']}")
    else:
        print("   No products found in store")
    
    print("\n2. CHECKING LOW STOCK...")
    low = agent.check_low_stock(threshold=5)
    print(f"   Products with ≤5 stock: {low['low_stock_count']}")
    for p in low["products"][:3]:
        print(f"   ⚠️  {p['title'][:35]:<35} | Only {p['stock']} left!")
    
    print("\n" + "=" * 60)
    print("✅ SHOPIFY CONNECTION SUCCESSFUL!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Check if store URL is correct")
    print("2. Check if access token is valid")
    print("3. Ensure app has permissions: read_products")