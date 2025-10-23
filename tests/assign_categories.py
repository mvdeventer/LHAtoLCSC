"""Assign categories to products based on keywords in descriptions and names."""
import sqlite3
import re
from pathlib import Path

# Category mapping based on keywords
CATEGORY_MAPPINGS = {
    "Resistors": {
        "keywords": [
            r'\bresistor\b', r'\bohm\b', r'\bΩ\b', r'\bkohm\b', r'\bmohm\b',
            r'\b\d+[kKmM]?\s*[RΩ]\b',  # e.g., "10k", "100R", "1M"
            r'\bres\b', r'\bresistance\b'
        ],
        "subcategories": {
            "Chip Resistor - Surface Mount": [
                r'\bsmd\b', r'\bsmt\b', r'\bchip\b', r'\bsurface mount\b',
                r'\b0201\b', r'\b0402\b', r'\b0603\b', r'\b0805\b', r'\b1206\b',
                r'\b1210\b', r'\b2010\b', r'\b2512\b'
            ],
            "Through Hole Resistors": [
                r'\bthrough.?hole\b', r'\bthd\b', r'\baxial\b', r'\bradial\b',
                r'\bleaded\b', r'\bdip\b'
            ]
        }
    },
    "Capacitors": {
        "keywords": [
            r'\bcapacitor\b', r'\bcap\b', r'\bfarad\b', r'\bpf\b', r'\bnf\b', r'\buf\b',
            r'\b\d+[pnuµ]?[fF]\b',  # e.g., "10pF", "100nF", "1uF"
            r'\bmlcc\b', r'\bceramic\b', r'\belectrolytic\b', r'\btantalum\b'
        ],
        "subcategories": {
            "Multilayer Ceramic Capacitors MLCC - SMD/SMT": [
                r'\bmlcc\b', r'\bceramic\b', r'\bsmd\b', r'\bsmt\b', r'\bchip\b',
                r'\b0201\b', r'\b0402\b', r'\b0603\b', r'\b0805\b', r'\b1206\b'
            ],
            "Aluminum Electrolytic Capacitors": [
                r'\belectrolytic\b', r'\baluminum\b', r'\balu\b', r'\bpolarized\b',
                r'\bradial\b', r'\baxial\b'
            ]
        }
    },
    "Integrated Circuits (ICs)": {
        "keywords": [
            r'\bic\b', r'\bchip\b', r'\bmicrocontroller\b', r'\bmcu\b', r'\bmpu\b',
            r'\bprocessor\b', r'\bdriver\b', r'\bcontroller\b', r'\binterface\b',
            r'\bregulator\b', r'\bop.?amp\b', r'\bcomparator\b', r'\bconverter\b',
            r'\btransceiver\b', r'\breceiver\b', r'\btransmitter\b',
            r'\bstm32\b', r'\besp32\b', r'\batmega\b', r'\bpic\b', r'\barm\b'
        ],
        "subcategories": {
            "Microcontrollers - MCU": [
                r'\bmcu\b', r'\bmicrocontroller\b', r'\bstm32\b', r'\batmega\b',
                r'\besp32\b', r'\bpic\b', r'\barm\b', r'\bcortex\b'
            ],
            "Interface ICs": [
                r'\binterface\b', r'\buart\b', r'\bi2c\b', r'\bspi\b', r'\busb\b',
                r'\bcan\b', r'\brs232\b', r'\brs485\b', r'\btransceiver\b',
                r'\blevel.?shifter\b', r'\bbuffer\b'
            ]
        }
    }
}

def find_category(product_text):
    """
    Find the best matching category and subcategory for a product.
    
    Args:
        product_text: Combined text from product model, name, description
        
    Returns:
        Tuple of (category, subcategory) or (None, None) if no match
    """
    product_text_lower = product_text.lower()
    
    best_match = None
    best_score = 0
    
    for category, data in CATEGORY_MAPPINGS.items():
        # Check main category keywords
        category_score = 0
        for keyword in data["keywords"]:
            if re.search(keyword, product_text_lower, re.IGNORECASE):
                category_score += 1
        
        if category_score > 0:
            # Found a category match, now check subcategories
            subcategory_match = None
            subcategory_score = 0
            
            for subcategory, sub_keywords in data["subcategories"].items():
                sub_score = 0
                for keyword in sub_keywords:
                    if re.search(keyword, product_text_lower, re.IGNORECASE):
                        sub_score += 1
                
                if sub_score > subcategory_score:
                    subcategory_score = sub_score
                    subcategory_match = subcategory
            
            # Calculate total score (category matches count more)
            total_score = category_score * 10 + subcategory_score
            
            if total_score > best_score:
                best_score = total_score
                # If we found a subcategory, use it; otherwise use main category
                best_match = subcategory_match if subcategory_match else category
    
    return best_match

def assign_categories_to_database():
    """Update all products in the database with assigned categories."""
    db_path = Path("mock_products.db")
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all products
    print("📊 Loading products from database...")
    cursor.execute('''
        SELECT product_code, product_model, product_name, product_intro_en
        FROM products
    ''')
    products = cursor.fetchall()
    total = len(products)
    print(f"Found {total:,} products\n")
    
    # Process products in batches
    updates = []
    categorized = 0
    uncategorized = 0
    
    print("🔍 Analyzing products and assigning categories...")
    for i, (product_code, model, name, description) in enumerate(products, 1):
        # Combine all text fields for analysis
        combined_text = f"{model or ''} {name or ''} {description or ''}"
        
        # Find category
        category = find_category(combined_text)
        
        if category:
            updates.append((category, product_code))
            categorized += 1
        else:
            uncategorized += 1
        
        # Progress update every 10,000 products
        if i % 10000 == 0:
            print(f"  Processed {i:,}/{total:,} products...")
    
    print(f"\n✓ Analysis complete:")
    print(f"  - Categorized: {categorized:,} products")
    print(f"  - Uncategorized: {uncategorized:,} products")
    
    # Update database
    if updates:
        print(f"\n💾 Updating database with {len(updates):,} category assignments...")
        cursor.executemany('''
            UPDATE products 
            SET parent_catalog_name = ?
            WHERE product_code = ?
        ''', updates)
        conn.commit()
        print("✓ Database updated successfully")
    
    # Show category distribution
    print("\n📊 Category Distribution:")
    cursor.execute('''
        SELECT parent_catalog_name, COUNT(*) as count
        FROM products
        WHERE parent_catalog_name IS NOT NULL AND parent_catalog_name != ''
        GROUP BY parent_catalog_name
        ORDER BY count DESC
    ''')
    
    for category, count in cursor.fetchall():
        percentage = (count / total) * 100
        print(f"  {category}: {count:,} ({percentage:.1f}%)")
    
    # Show some examples
    print("\n📝 Sample categorized products:")
    cursor.execute('''
        SELECT product_code, product_model, parent_catalog_name
        FROM products
        WHERE parent_catalog_name IS NOT NULL AND parent_catalog_name != ''
        LIMIT 10
    ''')
    
    for code, model, category in cursor.fetchall():
        print(f"  {code} - {model}: {category}")
    
    conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Product Category Assignment Tool")
    print("=" * 60)
    print()
    
    assign_categories_to_database()
    
    print("\n✓ Category assignment complete!")
