"""Test if component images are accessible."""
import requests
from PIL import Image
from io import BytesIO

# Test resistor image URL
url = "https://wmsc.lcsc.com/szlcsc/2304140030_UNI-ROYAL-Uniroyal-Elec-0402WGF1000TCE_C25744.jpg"

print(f"Testing image URL:")
print(f"  {url}")
print()

# Add proper headers (LCSC blocks requests without headers)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.lcsc.com/',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
}

try:
    print("Downloading image with proper headers...")
    response = requests.get(url, timeout=5, headers=headers)
    response.raise_for_status()
    
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Content-Type: {response.headers.get('Content-Type')}")
    print(f"✓ Size: {len(response.content):,} bytes")
    
    # Try to open as image
    print("\nOpening image with PIL...")
    img = Image.open(BytesIO(response.content))
    print(f"✓ Format: {img.format}")
    print(f"✓ Size: {img.size}")
    print(f"✓ Mode: {img.mode}")
    
    print("\n✅ Image is valid and accessible!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"   Type: {type(e).__name__}")
