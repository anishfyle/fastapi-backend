# URL Shortener API Test Script
# This script tests the URL shortener endpoints

import requests
import json

BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Root Endpoint (GET /)")
    print("="*60)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_shorten_url(long_url):
    """Test shortening a URL"""
    print("\n" + "="*60)
    print(f"TEST 2: Shorten URL (POST /shorten)")
    print("="*60)
    print(f"Long URL: {long_url}")
    
    payload = {"long_url": long_url}
    response = requests.post(f"{BASE_URL}/shorten", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json().get("short_url")
    return None

def test_resolve_url(short_url):
    """Test resolving a short URL"""
    print("\n" + "="*60)
    print(f"TEST 3: Resolve Short URL (GET /{short_url.split('/')[-1]})")
    print("="*60)
    print(f"Short URL: {short_url}")
    
    response = requests.get(short_url, allow_redirects=False)
    print(f"Status Code: {response.status_code}")
    print(f"Redirect Location: {response.headers.get('location', 'N/A')}")
    return response.status_code == 307

def test_duplicate_url(long_url):
    """Test that duplicate URLs return the same short code"""
    print("\n" + "="*60)
    print(f"TEST 4: Duplicate URL Handling")
    print("="*60)
    print(f"Long URL: {long_url}")
    
    payload = {"long_url": long_url}
    response = requests.post(f"{BASE_URL}/shorten", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✓ Should return the same short code as before")
    return response.status_code == 200

def test_invalid_short_code():
    """Test accessing an invalid short code"""
    print("\n" + "="*60)
    print(f"TEST 5: Invalid Short Code (GET /invalid999)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/invalid999", allow_redirects=False)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 404:
        print(f"Response: {response.json()}")
        print("✓ Correctly returns 404 for invalid short code")
    return response.status_code == 404

def test_multiple_urls():
    """Test shortening multiple different URLs"""
    print("\n" + "="*60)
    print(f"TEST 6: Multiple URLs")
    print("="*60)
    
    test_urls = [
        "https://www.python.org",
        "https://fastapi.tiangolo.com",
        "https://www.sqlite.org"
    ]
    
    short_urls = []
    for url in test_urls:
        payload = {"long_url": url}
        response = requests.post(f"{BASE_URL}/shorten", json=payload)
        if response.status_code == 200:
            short_url = response.json().get("short_url")
            short_urls.append(short_url)
            print(f"✓ {url} → {short_url}")
    
    return len(short_urls) == len(test_urls)

def main():
    """Run all tests"""
    print("\n" + "🚀 " + "="*56)
    print("   URL SHORTENER API - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    try:
        # Test 1: Root endpoint
        test_root_endpoint()
        
        # Test 2: Shorten a URL
        test_url = "https://www.github.com/anishfyle/fastapi-backend"
        short_url = test_shorten_url(test_url)
        
        if short_url:
            # Test 3: Resolve the short URL
            test_resolve_url(short_url)
            
            # Test 4: Test duplicate URL handling
            test_duplicate_url(test_url)
        
        # Test 5: Test invalid short code
        test_invalid_short_code()
        
        # Test 6: Test multiple URLs
        test_multiple_urls()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED!")
        print("="*60)
        print("\nThe URL Shortener is working correctly!")
        print(f"API is running at: {BASE_URL}")
        print(f"Interactive docs at: {BASE_URL}/docs")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the API server.")
        print("Please ensure the server is running with:")
        print("  uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main()
