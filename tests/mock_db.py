"""
SQLite Database for Mock LCSC Server

Provides fast search and retrieval of products using SQLite instead of JSON.
Much faster for large datasets (10,000+ products).

Usage:
    from mock_db import MockDatabase
    
    db = MockDatabase('mock_products.db')
    db.import_from_json('mock_products_large.json')
    
    results = db.search_products(keyword='resistor 0603', page=1, page_size=10)
"""

import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path


class MockDatabase:
    """SQLite-based product database for fast searching."""
    
    def __init__(self, db_path: str = 'mock_products.db'):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self._create_tables()
        self._create_indexes()
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Main products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_code TEXT PRIMARY KEY,
                product_model TEXT,
                product_name TEXT,
                brand_name TEXT,
                package_type TEXT,
                product_unit TEXT,
                min_packet_unit TEXT,
                min_buy_number TEXT,
                stock_number TEXT,
                product_intro_en TEXT,
                parent_catalog_name TEXT,
                product_data JSON,
                search_text TEXT
            )
        """)
        
        # Price tiers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_tiers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_code TEXT,
                start_number INTEGER,
                product_price REAL,
                discount_rate TEXT,
                FOREIGN KEY (product_code) REFERENCES products(product_code)
            )
        """)
        
        # Parameters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_code TEXT,
                param_code TEXT,
                param_value TEXT,
                FOREIGN KEY (product_code) REFERENCES products(product_code)
            )
        """)
        
        self.conn.commit()
    
    def _create_indexes(self):
        """Create indexes for fast searching."""
        cursor = self.conn.cursor()
        
        # Create indexes on searchable fields
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_code ON products(product_code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_model ON products(product_model)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_brand_name ON products(brand_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_package_type ON products(package_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_text ON products(search_text)")
        
        # Full-text search index (SQLite FTS5)
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS products_fts USING fts5(
                product_code,
                product_model,
                product_name,
                brand_name,
                package_type,
                product_intro_en,
                parent_catalog_name,
                content=products
            )
        """)
        
        self.conn.commit()
    
    def import_from_json(self, json_path: str) -> int:
        """Import products from JSON file into database."""
        print(f"Importing products from {json_path}...")
        
        if not os.path.exists(json_path):
            print(f"Error: JSON file not found: {json_path}")
            return 0
        
        with open(json_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        # Clear existing data
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM products")
        cursor.execute("DELETE FROM price_tiers")
        cursor.execute("DELETE FROM parameters")
        cursor.execute("DELETE FROM products_fts")
        
        count = 0
        for product_code, product in products.items():
            # Create searchable text (all fields concatenated)
            search_text = ' '.join([
                str(product.get('productCode', '')),
                str(product.get('productModel', '')),
                str(product.get('productName', '')),
                str(product.get('brandName', '')),
                str(product.get('packageType', '')),
                str(product.get('productIntroEn', '')),
                str(product.get('parentCatalogName', '')),
            ]).lower()
            
            # Insert main product
            cursor.execute("""
                INSERT INTO products (
                    product_code, product_model, product_name, brand_name,
                    package_type, product_unit, min_packet_unit, min_buy_number,
                    stock_number, product_intro_en, parent_catalog_name,
                    product_data, search_text
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product_code,
                product.get('productModel', ''),
                product.get('productName', ''),
                product.get('brandName', ''),
                product.get('packageType', ''),
                product.get('productUnit', ''),
                product.get('minPacketUnit', ''),
                product.get('minBuyNumber', ''),
                product.get('stockNumber', ''),
                product.get('productIntroEn', ''),
                product.get('parentCatalogName', ''),
                json.dumps(product),
                search_text
            ))
            
            # Insert FTS entry
            cursor.execute("""
                INSERT INTO products_fts (
                    product_code, product_model, product_name, brand_name,
                    package_type, product_intro_en, parent_catalog_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                product_code,
                product.get('productModel', ''),
                product.get('productName', ''),
                product.get('brandName', ''),
                product.get('packageType', ''),
                product.get('productIntroEn', ''),
                product.get('parentCatalogName', '')
            ))
            
            # Insert price tiers
            for price in product.get('productPriceList', []):
                cursor.execute("""
                    INSERT INTO price_tiers (product_code, start_number, product_price, discount_rate)
                    VALUES (?, ?, ?, ?)
                """, (
                    product_code,
                    int(price.get('startNumber', 0)),
                    float(price.get('productPrice', 0)),
                    price.get('discountRate', '100')
                ))
            
            # Insert parameters
            for param in product.get('paramVOList', []):
                cursor.execute("""
                    INSERT INTO parameters (product_code, param_code, param_value)
                    VALUES (?, ?, ?)
                """, (
                    product_code,
                    param.get('paramCode', ''),
                    param.get('paramValue', '')
                ))
            
            count += 1
            if count % 1000 == 0:
                print(f"  Imported {count} products...")
        
        self.conn.commit()
        print(f"✓ Successfully imported {count} products")
        return count
    
    def search_products(self, keyword: str = '', page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Search products using SQL.
        
        Args:
            keyword: Search keyword(s)
            page: Page number (1-based)
            page_size: Results per page
        
        Returns:
            Dictionary with total, current_page, page_size, and productList
        """
        cursor = self.conn.cursor()
        
        if not keyword or keyword.strip() == '':
            # Return all products
            cursor.execute("SELECT COUNT(*) FROM products")
            total = cursor.fetchone()[0]
            
            offset = (page - 1) * page_size
            cursor.execute("""
                SELECT product_data, parent_catalog_name FROM products
                ORDER BY
                    -- Priority 1: Best price at highest price break (cheapest bulk price)
                    (
                        SELECT MIN(CAST(JSON_EXTRACT(price.value,
                                        '$.productPrice') AS REAL))
                        FROM JSON_EACH(product_data, '$.productPriceList') AS price
                        WHERE CAST(JSON_EXTRACT(price.value,
                                                '$.productPrice') AS REAL) > 0
                        ORDER BY CAST(JSON_EXTRACT(price.value, 
                                                   '$.endAmount') AS INTEGER) DESC
                        LIMIT 1
                    ) ASC,
                    -- Priority 2: Highest stock for tie-breaking
                    CAST(JSON_EXTRACT(product_data, '$.stockNumber') AS INTEGER) DESC,
                    -- Priority 3: Product code for consistency
                    product_code ASC
                LIMIT ? OFFSET ?
            """, (page_size, offset))
            
            results = []
            for row in cursor.fetchall():
                product = json.loads(row[0])
                # Inject the category from the database column
                if row[1]:
                    product['parentCatalogName'] = row[1]
                results.append(product)
        else:
            # Use LIKE search for reliability (FTS5 has issues with special chars like periods)
            # Split keywords and search for all of them
            keywords = keyword.strip().lower().split()
            
            if not keywords:
                return {
                    "total": 0,
                    "current_page": page,
                    "page_size": page_size,
                    "productList": []
                }
            
            # Build WHERE clause with LIKE for each keyword
            where_clauses = []
            params = []
            for kw in keywords:
                where_clauses.append("lower(product_data) LIKE ?")
                params.append(f'%{kw}%')
            
            where_sql = " AND ".join(where_clauses)
            
            # Get total count
            count_sql = f"SELECT COUNT(*) FROM products WHERE {where_sql}"
            cursor.execute(count_sql, params)
            total = cursor.fetchone()[0]
            
            # Get paginated results with smart sorting
            offset = (page - 1) * page_size
            select_sql = f"""
                SELECT product_data, parent_catalog_name
                FROM products
                WHERE {where_sql}
                ORDER BY
                    -- Priority 1: Best price at highest price break
                    (
                        SELECT MIN(CAST(JSON_EXTRACT(price.value,
                                        '$.productPrice') AS REAL))
                        FROM JSON_EACH(product_data, 
                                      '$.productPriceList') AS price
                        WHERE CAST(JSON_EXTRACT(price.value,
                                                '$.productPrice') AS REAL) > 0
                        ORDER BY CAST(JSON_EXTRACT(price.value,
                                                   '$.endAmount') AS INTEGER) DESC
                        LIMIT 1
                    ) ASC,
                    -- Priority 2: Highest stock for tie-breaking
                    CAST(JSON_EXTRACT(product_data, 
                                     '$.stockNumber') AS INTEGER) DESC,
                    -- Priority 3: Product code for consistency
                    product_code ASC
                LIMIT ? OFFSET ?
            """
            params.extend([page_size, offset])
            cursor.execute(select_sql, params)
            
            results = []
            for row in cursor.fetchall():
                product = json.loads(row[0])
                # Inject the category from the database column
                if row[1]:
                    product['parentCatalogName'] = row[1]
                results.append(product)
        
        return {
            "total": total,
            "current_page": page,
            "page_size": page_size,
            "productList": results
        }
    
    def get_product(self, product_code: str) -> Optional[Dict[str, Any]]:
        """Get a single product by code."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT product_data, parent_catalog_name FROM products WHERE product_code = ?", (product_code,))
        row = cursor.fetchone()
        
        if row:
            product = json.loads(row[0])
            # Inject the category from the database column
            if row[1]:
                product['parentCatalogName'] = row[1]
            return product
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT brand_name) FROM products")
        total_brands = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT package_type) FROM products")
        total_packages = cursor.fetchone()[0]
        
        return {
            "total_products": total_products,
            "total_brands": total_brands,
            "total_packages": total_packages
        }
    
    def close(self):
        """Close database connection."""
        self.conn.close()


def convert_json_to_db(json_path: str, db_path: str = 'mock_products.db'):
    """
    Convert JSON file to SQLite database.
    
    Usage:
        python mock_db.py
    """
    db = MockDatabase(db_path)
    count = db.import_from_json(json_path)
    stats = db.get_stats()
    
    print(f"\nDatabase Statistics:")
    print(f"  Total Products: {stats['total_products']:,}")
    print(f"  Total Brands: {stats['total_brands']:,}")
    print(f"  Total Packages: {stats['total_packages']:,}")
    
    db.close()
    print(f"\n✓ Database created: {db_path}")


if __name__ == '__main__':
    # Convert the large JSON file to database
    json_file = 'mock_products_large.json'
    db_file = 'mock_products.db'
    
    if os.path.exists(json_file):
        convert_json_to_db(json_file, db_file)
    else:
        print(f"Error: {json_file} not found")
        print("Please run this script from the tests/ directory")
