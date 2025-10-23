"""
Test search performance with SQLite database
"""
import requests
import time
import json

BASE_URL = "http://localhost:5000"

def test_search(query, description):
    """Test search and measure time"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    
    start = time.time()
    
    response = requests.post(
        f"{BASE_URL}/rest/wmsc2agent/search/product",
        json={
            "searchContent": query,
            "currentPage": 1,
            "pageSize": 10
        }
    )
    
    elapsed = time.time() - start
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            result = data.get("result", {})
            total = result.get("total", 0)
            products = result.get("productRecordList", [])
            
            print(f"\n✓ Search completed in {elapsed:.3f} seconds")
            print(f"  Total results: {total:,}")
            print(f"  Returned: {len(products)} products")
            
            if products:
                print(f"\n  Top results:")
                for i, p in enumerate(products[:5], 1):
                    print(f"    {i}. {p['productCode']} - {p['productModel']}")
                    print(f"       {p['brandNameEn']} | {p.get('encapStandard', 'N/A')}")
        else:
            print(f"❌ API Error: {data.get('message')}")
    else:
        print(f"❌ HTTP Error {response.status_code}")
    
    return elapsed

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SQLite Database Search Performance Test")
    print("="*60)
    
    # Test various searches
    tests = [
        ("3.3k 0603 resistor", "Specific resistor search"),
        ("resistor", "Generic resistor search"),
        ("stm32", "Microcontroller search"),
        ("capacitor 10uf", "Capacitor search"),
        ("led", "LED search"),
    ]
    
    times = []
    for query, desc in tests:
        elapsed = test_search(query, desc)
        times.append(elapsed)
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "="*60)
    print("Performance Summary")
    print("="*60)
    print(f"Average search time: {sum(times)/len(times):.3f} seconds")
    print(f"Fastest search: {min(times):.3f} seconds")
    print(f"Slowest search: {max(times):.3f} seconds")
    print("\nCompare this to previous JSON-based search (5-30 seconds)!")
    print("="*60)
