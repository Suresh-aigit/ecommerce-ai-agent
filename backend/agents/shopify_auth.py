"""
Shopify Authentication Module
Handles API connections and requests to Shopify store
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()


class ShopifyAuth:
    """
    Shopify API Authentication and Request Handler
    """
    
    def __init__(self):
        """Initialize Shopify connection with credentials from .env"""
        self.shop_name = os.getenv('SHOPIFY_SHOP_NAME', 'ai-swarm-2')
        self.access_token = os.getenv('SHOPIFY_ACCESS_TOKEN', 'dummy-token')
        self.api_version = '2024-01'
        self.base_url = f"https://{self.shop_name}.myshopify.com/admin/api/{self.api_version}"
        
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
    
    def get(self, endpoint, params=None):
        """
        Make GET request to Shopify API
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(
                url, 
                headers=self.headers, 
                params=params, 
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Shopify API Error: {e}")
            return self._get_mock_data(endpoint)
    
    def post(self, endpoint, data=None):
        """
        Make POST request to Shopify API
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Shopify API POST Error: {e}")
            return {"error": str(e), "success": False}
    
    def _get_mock_data(self, endpoint):
        """
        Return realistic mock data for testing when API is unavailable
        """
        if "products" in endpoint:
            return {
                "products": [
                    {
                        "id": 1,
                        "title": "Premium Snowboard",
                        "product_type": "Snowboards",
                        "variants": [{
                            "id": 101,
                            "sku": "SB-001",
                            "price": "599.99",
                            "inventory_quantity": 15
                        }],
                        "created_at": "2024-01-10T10:00:00Z",
                        "updated_at": "2024-01-15T14:30:00Z"
                    },
                    {
                        "id": 2,
                        "title": "Winter Jacket Pro",
                        "product_type": "Clothing",
                        "variants": [{
                            "id": 102,
                            "sku": "WJ-002",
                            "price": "299.99",
                            "inventory_quantity": 8
                        }],
                        "created_at": "2024-01-12T09:00:00Z",
                        "updated_at": "2024-01-14T16:45:00Z"
                    },
                    {
                        "id": 3,
                        "title": "Ski Goggles HD",
                        "product_type": "Accessories",
                        "variants": [{
                            "id": 103,
                            "sku": "SG-003",
                            "price": "89.99",
                            "inventory_quantity": 0
                        }],
                        "created_at": "2024-01-08T11:20:00Z",
                        "updated_at": "2024-01-13T10:15:00Z"
                    },
                    {
                        "id": 4,
                        "title": "Thermal Gloves",
                        "product_type": "Accessories",
                        "variants": [{
                            "id": 104,
                            "sku": "TG-004",
                            "price": "49.99",
                            "inventory_quantity": 45
                        }],
                        "created_at": "2024-01-11T13:00:00Z",
                        "updated_at": "2024-01-14T09:30:00Z"
                    },
                    {
                        "id": 5,
                        "title": "Snow Boots",
                        "product_type": "Footwear",
                        "variants": [{
                            "id": 105,
                            "sku": "BT-005",
                            "price": "179.99",
                            "inventory_quantity": 12
                        }],
                        "created_at": "2024-01-09T15:30:00Z",
                        "updated_at": "2024-01-15T11:00:00Z"
                    }
                ]
            }
        
        elif "orders" in endpoint:
            return {
                "orders": [
                    {
                        "id": 1001,
                        "name": "#1001",
                        "total_price": "599.99",
                        "subtotal_price": "599.99",
                        "taxes_included": True,
                        "currency": "USD",
                        "financial_status": "paid",
                        "fulfillment_status": None,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:35:00Z",
                        "customer": {
                            "id": 2001,
                            "email": "john.smith@example.com",
                            "first_name": "John",
                            "last_name": "Smith",
                            "orders_count": 3
                        },
                        "line_items": [
                            {
                                "id": 3001,
                                "title": "Premium Snowboard",
                                "quantity": 1,
                                "price": "599.99",
                                "sku": "SB-001"
                            }
                        ],
                        "shipping_address": {
                            "city": "Denver",
                            "province": "Colorado",
                            "country": "USA"
                        }
                    },
                    {
                        "id": 1002,
                        "name": "#1002",
                        "total_price": "389.98",
                        "subtotal_price": "389.98",
                        "taxes_included": True,
                        "currency": "USD",
                        "financial_status": "paid",
                        "fulfillment_status": "fulfilled",
                        "created_at": "2024-01-15T09:15:00Z",
                        "updated_at": "2024-01-15T14:20:00Z",
                        "customer": {
                            "id": 2002,
                            "email": "jane.doe@example.com",
                            "first_name": "Jane",
                            "last_name": "Doe",
                            "orders_count": 1
                        },
                        "line_items": [
                            {
                                "id": 3002,
                                "title": "Winter Jacket Pro",
                                "quantity": 1,
                                "price": "299.99",
                                "sku": "WJ-002"
                            },
                            {
                                "id": 3003,
                                "title": "Thermal Gloves",
                                "quantity": 2,
                                "price": "49.99",
                                "sku": "TG-004"
                            }
                        ],
                        "shipping_address": {
                            "city": "Aspen",
                            "province": "Colorado",
                            "country": "USA"
                        }
                    },
                    {
                        "id": 1003,
                        "name": "#1003",
                        "total_price": "89.99",
                        "subtotal_price": "89.99",
                        "taxes_included": False,
                        "currency": "USD",
                        "financial_status": "pending",
                        "fulfillment_status": None,
                        "created_at": "2024-01-15T08:45:00Z",
                        "updated_at": "2024-01-15T08:45:00Z",
                        "customer": None,
                        "line_items": [
                            {
                                "id": 3004,
                                "title": "Ski Goggles HD",
                                "quantity": 1,
                                "price": "89.99",
                                "sku": "SG-003"
                            }
                        ],
                        "shipping_address": {
                            "city": "Boulder",
                            "province": "Colorado",
                            "country": "USA"
                        }
                    }
                ]
            }
        
        return {}