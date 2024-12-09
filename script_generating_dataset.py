import csv
import random
import string
from faker import Faker
from datetime import datetime
import json  # For handling complex fields like reviews

# Initialize Faker for generating random data
fake = Faker()

# Define categories and other constants
CATEGORIES = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Camera", "Television", "Tablet", "Speaker", "Monitor", "Keyboard"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Dress", "Sweater", "Skirt", "Shoes", "Hat", "Scarf", "Socks"],
    "Home & Kitchen": ["Blender", "Microwave", "Vacuum Cleaner", "Toaster", "Cookware Set", "Knife Set", "Dish Rack", "Coffee Maker", "Pressure Cooker", "Air Purifier"],
    "Books": ["Mystery Novel", "Self-Help Guide", "Science Fiction", "Romance Novel", "History Book", "Biography", "Fantasy Novel", "Children's Book", "Cookbook", "Thriller"],
    "Toys": ["Action Figure", "Board Game", "Doll", "Puzzle", "Remote Control Car", "Lego Set", "Plush Toy", "Science Kit", "Play-Doh", "Yo-Yo"],
    "Health & Personal Care": ["Shampoo", "Conditioner", "Toothbrush", "Toothpaste", "Hand Soap", "Face Cream", "Body Lotion", "Sunscreen", "First Aid Kit", "Thermometer"]
}
MAX_PRODUCTS = 500000
CSV_FILE_NAME = "Amazon_Product.csv"

# Pools for sellers, companies, and manufacturers
SELLER_POOL = [fake.name() for _ in range(20)]
COMPANY_POOL = [fake.company() for _ in range(20)]
MANUFACTURER_POOL = [fake.company() for _ in range(20)]

# Generate random reviews
def generate_reviews():
    reviews = []
    num_reviews = random.randint(1, 20)
    for _ in range(num_reviews):
        reviews.append({
            "reviewer": fake.name(),
            "rating": round(random.uniform(1, 5), 2),
            "bought_past_month": random.randint(0, 500),
            "comment": fake.sentence()
        })
    return reviews

# Generate ISO 8601 date without trailing zeros
def generate_iso_date():
    return datetime.strftime(fake.date_time_this_decade(), "%Y-%m-%dT%H:%M:%SZ")

# Function to generate a random product
def generate_product():
    category = random.choice(list(CATEGORIES.keys()))
    product_name = random.choice(CATEGORIES[category])
    initial_price = round(random.uniform(20, 1000), 2)
    max_discounted_price = initial_price * 0.4  # Ensure at least 40% of the original price
    final_price = round(random.uniform(max_discounted_price, initial_price), 2)
    image_urls = [fake.image_url() for _ in range(random.randint(1, 5))]  # Define image_urls here
    
    return {
        "title": product_name or "Untitled Product",
        "description": fake.paragraph(nb_sentences=2) or "No description available",
        "initial_price": initial_price,
        "final_price": final_price,
        "currency": "USD",
        "bought_past_month": random.randint(0, 100),
        "delivery": random.choice(["2-day", "Standard", "Overnight"]),
        "availability": random.choice(["In Stock", "Out of Stock", "Preorder"]),
        "reviews_count": random.randint(1, 20),
        "categories": category,
        "asin": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        "root_bs_rank": random.randint(1, 10000),
        "domain": fake.domain_name() or "example.com",
        "images_count": len(image_urls),
        "url": fake.url() or "https://example.com",
        "image_url": image_urls,
        "item_weight": round(random.uniform(0.1, 5.0), 2),
        "rating": round(random.uniform(1, 5), 2),
        "product_dimensions": f"{round(random.uniform(5, 50), 1)} x {round(random.uniform(5, 50), 1)} x {round(random.uniform(5, 50), 1)} cm",
        "date_first_available": generate_iso_date(),
        "discount": round((initial_price - final_price) / initial_price * 100, 2),
        "model_number": fake.ean(length=13),
        "manufacturer": random.choice(MANUFACTURER_POOL),
        "department": random.choice(["Men", "Women", "Kids", "Unisex"]),
        "badge": random.choice(["Amazon's Choice", "Best Seller", None]),
        "climate_pledge_friendly": random.choice([True, False]),
        "reviews": generate_reviews(),
        "seller": {
            "name": random.choice(SELLER_POOL),
            "company": random.choice(COMPANY_POOL),
            "seller_url": fake.url() or "https://example.com/seller"
        }
    }

# Generate the CSV file
def generate_csv():
    with open(CSV_FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
        # Update the fieldnames list to include 'climate_pledge_friendly'
        writer = csv.DictWriter(file, fieldnames=[
            "title", "description", "initial_price", "final_price", "currency", "bought_past_month", "delivery", "availability", "reviews_count", "categories", "asin", 
            "root_bs_rank", "domain", "images_count", "url", "image_url", "item_weight", "rating", 
            "product_dimensions", "date_first_available", "discount", "model_number", "manufacturer", "department", 
            "badge", "reviews", "seller", "climate_pledge_friendly"  
        ])
        # Write the header
        writer.writeheader()

        print(f"Starting product generation for {MAX_PRODUCTS} products...")
        for i in range(MAX_PRODUCTS):
            product = generate_product()
            # Convert reviews to JSON string
            product["reviews"] = json.dumps(product["reviews"]) 
            writer.writerow(product)

            if (i + 1) % 1000 == 0:
                print(f"Generated {i + 1} products so far...")

        print(f"Finished generating {MAX_PRODUCTS} products. Saved to {CSV_FILE_NAME}")

# Run the script
if __name__ == "__main__":
    generate_csv()
