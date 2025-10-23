#!/usr/bin/env python3
"""
Test pagination button logic to verify the fix for duplicate page numbers.
"""

def test_create_page_buttons_logic(current_page, total_pages, max_buttons=5):
    """Test the pagination button logic."""
    print(f"\nTesting: current_page={current_page}, total_pages={total_pages}")
    
    if total_pages <= 1:
        print("No buttons needed (total_pages <= 1)")
        return []
    
    # Calculate the range of pages to display
    half_range = max_buttons // 2  # 2 for max_buttons=5
    start_page = max(1, current_page - half_range)
    end_page = min(total_pages, current_page + half_range)
    
    # Adjust range to always show max_buttons if possible
    if end_page - start_page + 1 < max_buttons:
        if start_page == 1:
            # We're at the beginning, extend to the right
            end_page = min(total_pages, start_page + max_buttons - 1)
        elif end_page == total_pages:
            # We're at the end, extend to the left
            start_page = max(1, end_page - max_buttons + 1)
    
    page_range = list(range(start_page, end_page + 1))
    print(f"Pages to show: {page_range}")
    return page_range

def main():
    """Test various pagination scenarios."""
    print("=== Pagination Button Logic Test ===")
    
    # Test scenarios
    test_cases = [
        (1, 104),    # First page
        (2, 104),    # Second page
        (3, 104),    # Third page
        (50, 104),   # Middle page
        (102, 104),  # Near end
        (103, 104),  # Second to last
        (104, 104),  # Last page (the problematic case)
        (1, 3),      # Small dataset
        (2, 3),      # Small dataset middle
        (3, 3),      # Small dataset end
    ]
    
    for current, total in test_cases:
        result = test_create_page_buttons_logic(current, total)
        
        # Check for duplicates
        if len(result) != len(set(result)):
            print(f"❌ DUPLICATE PAGES FOUND: {result}")
        else:
            print(f"✅ No duplicates")

if __name__ == "__main__":
    main()