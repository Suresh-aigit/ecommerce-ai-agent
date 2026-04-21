import sys
sys.path.append('backend/agents')

from shopify_auth import ShopifyAuth

print('=' * 60)
print('TESTING SHOPIFY CONNECTION')
print('=' * 60)

try:
    auth = ShopifyAuth()
    
    print('\nFetching products...')
    products = auth.get('/products.json?limit=5')
    items = products.get('products', [])
    print(f'Found {len(items)} products')
    
    for p in items[:3]:
        title = p['title']
        price = p.get('variants', [{}])[0].get('price', 'N/A')
        print(f'  - {title} ()')
    
    print('\nSUCCESS!')

except Exception as e:
    print(f'\nERROR: {e}')
