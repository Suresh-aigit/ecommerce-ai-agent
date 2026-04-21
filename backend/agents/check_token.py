from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('SHOPIFY_ACCESS_TOKEN')
store = os.getenv('SHOPIFY_STORE_URL')

print(f"Store: {store}")
print(f"Token: {token[:20]}..." if token else "No token found")
print(f"Length: {len(token) if token else 0}")
print(f"Starts with 'atkn_': {token.startswith('atkn_') if token else False}")