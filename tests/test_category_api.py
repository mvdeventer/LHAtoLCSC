"""
Test the LCSC Category API endpoint
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lhatolcsc.api.client import LCSCClient
import json

# Test category endpoint
print("="*60)
print("Testing LCSC Category API")
print("="*60)

try:
    # Create API client (will use mock server)
    client = LCSCClient(
        api_key="test_api_key_12345",
        api_secret="test_api_secret_67890",
        base_url="http://localhost:5000"
    )
    
    # Get categories
    categories = client.get_categories()
    
    print(f"\n✓ Found {len(categories)} top-level categories\n")
    
    # Display category tree
    for cat in categories:
        print(f"📁 {cat['categoryName']} (ID: {cat['categoryId']})")
        
        # Show subcategories
        children = cat.get('children', [])
        for child in children:
            print(f"   └─ {child['categoryName']} (ID: {child['categoryId']})")
        print()
    
    # Save to file for reference
    with open('category_tree.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    print("💾 Category tree saved to: category_tree.json")
    
except ConnectionRefusedError:
    print("❌ Error: Cannot connect to mock server")
    print("   Please make sure the server is running on http://localhost:5000")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
