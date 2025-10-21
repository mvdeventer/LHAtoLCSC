"""
LCSC API Endpoints.

Defines all API endpoint paths.
"""


class LCSCEndpoints:
    """LCSC API endpoint paths."""
    
    # Base API path
    BASE_PATH = "/rest/wmsc2agent"
    
    # Product APIs
    CATEGORY = f"{BASE_PATH}/category"
    BRAND = f"{BASE_PATH}/brand"
    CATEGORY_PRODUCT = f"{BASE_PATH}/category/product/{{category_id}}"
    PRODUCT_INFO = f"{BASE_PATH}/product/info/{{product_number}}"
    SEARCH_PRODUCT = f"{BASE_PATH}/search/product"
    
    # Order APIs
    SUBMIT_ORDER = f"{BASE_PATH}/submit/order"
    SELECT_ORDER = f"{BASE_PATH}/select/order/page"
    
    # Shipment APIs
    GET_SHIPMENT = f"{BASE_PATH}/get/shipment"
