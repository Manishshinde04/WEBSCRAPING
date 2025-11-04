import requests
import bs4
from datetime import datetime
import json
import os
import re
from urllib.parse import urlparse

# --- NEW: Import Flask ---
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# --- Configuration ---
DATA_FILE = 'product_data.json' 
PRODUCTS_FILE = 'products.txt' # Stores the URLs for a separate scheduler

# --- Browser Simulation Headers ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# --- NEW: Create the Flask App ---
app = Flask(__name__)
CORS(app)  # This enables Cross-Origin requests, allowing your HTML file to fetch data

# --- Helper Functions (renamed with _ to show they are internal) ---

def _load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"💾 Data saved to {DATA_FILE}")

def _add_url_to_products_file(url):
    """Ensures a URL is in products.txt for a separate scheduler."""
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'w') as f:
            f.write(url + '\n')
    else:
        with open(PRODUCTS_FILE, 'r+') as f:
            lines = f.read().splitlines()
            if url not in lines:
                f.write(url + '\n')

def _get_usd_to_inr_rate(fallback=83.5):
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
        response.raise_for_status()
        data = response.json()
        rate = data.get('rates', {}).get('INR')
        if rate:
            return float(rate)
    except requests.exceptions.RequestException:
        pass # Use fallback
    return fallback

def _extract_asin(url):
    match = re.search(r'/(dp|gp/product)/([A-Z0-9]{10})', url)
    if match:
        return match.group(2)
    return None

def _parse_price(price_text):
    if not price_text: return None
    cleaned_price = re.sub(r"[₹$,]", "", price_text).strip()
    try:
        return float(cleaned_price)
    except ValueError:
        return None

def _scrape_product(product_url, exchange_rate):
    """
    Scrapes a single product and returns structured data.
    This is the same robust function from our last message.
    """
    asin = _extract_asin(product_url)
    if not asin:
        raise ValueError("Could not extract ASIN from URL.")

    try:
        response = SESSION.get(product_url, timeout=10)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        
        title_tag = soup.select_one('#productTitle')
        image_tag = soup.select_one('#imgTagWrapperId img')
        
        price_selectors = ['span.a-price-whole', 'span.a-offscreen', '#corePrice_feature_div .a-offscreen']
        price_text, currency_symbol = None, None
        
        for selector in price_selectors:
            price_tag = soup.select_one(selector)
            if price_tag:
                price_text = price_tag.get_text(strip=True)
                if price_text.startswith('₹'): currency_symbol = 'INR'
                elif price_text.startswith('$'): currency_symbol = 'USD'
                if currency_symbol: break
        
        if not price_text or not title_tag or not currency_symbol:
            raise ValueError("Failed to find price, title, or currency.")

        price_float = _parse_price(price_text)
        if price_float is None:
            raise ValueError("Failed to parse price.")
            
        price_inr = price_float
        if currency_symbol == 'USD':
            price_inr = round(price_float * exchange_rate, 2)
            print(f"✔️ Success for {asin}: Found ${price_float} -> ₹{price_inr}")
        else:
            print(f"✔️ Success for {asin}: Found ₹{price_float}")

        title = title_tag.get_text(strip=True)
        image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else f"https://placehold.co/200x200/ffffff/111827?text={asin}"
        timestamp = datetime.now().isoformat()
        
        return asin, {
            "name": title,
            "imageUrl": image_url,
            "url": product_url,
            "lastPriceINR": price_inr,
            "priceHistory": [{'timestamp': timestamp, 'price_inr': price_inr}]
        }

    except Exception as e:
        print(f"❌ Error scraping {asin}: {e}")
        raise

# --- API ENDPOINT 1: Get all saved products ---
@app.route('/api/all-products', methods=['GET'])
def get_all_products():
    """
    This endpoint is called when the page loads.
    It reads product_data.json and sends it to the frontend.
    """
    print("Request received for /api/all-products")
    data = _load_data()
    return jsonify(data)

# --- API ENDPOINT 2: Track a new product ---
@app.route('/api/track-product', methods=['POST'])
def track_new_product():
    """
    This endpoint is called when you click the "Track Product" button.
    It scrapes the new URL, saves it, and returns the new product's data.
    """
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required."}), 400
    
    print(f"Request received to track: {url}")
    
    try:
        exchange_rate = _get_usd_to_inr_rate()
        asin, new_product_data = _scrape_product(url, exchange_rate)
        
        # Save the new product
        all_data = _load_data()
        
        if asin in all_data:
            # It already exists, just add the new price to its history
            all_data[asin]['priceHistory'].append(new_product_data['priceHistory'][0])
            all_data[asin]['lastPriceINR'] = new_product_data['lastPriceINR']
        else:
            # It's a brand new product
            all_data[asin] = new_product_data
        
        _save_data(all_data)
        _add_url_to_products_file(url) # Save URL for your scheduled script
        
        # Send just the new/updated product data back to the frontend
        return jsonify(all_data[asin])
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Main entry point to run the server ---
if __name__ == "__main__":
    print("🚀 PricePulse API Server starting on http://127.0.0.1:5000")
    print("   (Your old scheduled tracker.py is not running. This server is for the UI.)")
    app.run(debug=True, port=5000)