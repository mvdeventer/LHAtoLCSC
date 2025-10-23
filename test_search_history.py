#!/usr/bin/env python3
"""
Test script for search history functionality.
"""

import sys
import os
import tempfile
import shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lhatolcsc.gui.search_history import SearchHistoryManager


def test_search_history():
    """Test search history functionality."""
    print("Testing Search History Manager...")
    
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create history manager with temp directory
        history_manager = SearchHistoryManager(config_dir=temp_dir, max_history=5)
        
        print("\n1. Testing adding search terms...")
        history_manager.add_search("resistor")
        history_manager.add_search("capacitor")
        history_manager.add_search("10k resistor")
        history_manager.add_search("led")
        
        history = history_manager.get_history()
        print(f"History after adding 4 terms: {history}")
        assert len(history) == 4
        assert history[0] == "led"  # Most recent first
        assert "resistor" in history
        
        print("\n2. Testing duplicate handling...")
        history_manager.add_search("resistor")  # Should move to top
        history = history_manager.get_history()
        print(f"History after duplicate 'resistor': {history}")
        assert history[0] == "resistor"
        assert len(history) == 4  # Should not increase
        
        print("\n3. Testing max history limit...")
        history_manager.add_search("diode")
        history_manager.add_search("mosfet")
        history_manager.add_search("crystal")
        history = history_manager.get_history()
        print(f"History after exceeding limit: {history}")
        assert len(history) == 5  # Should respect max_history
        assert history[0] == "crystal"
        
        print("\n4. Testing persistence...")
        # Create new manager with same config dir
        history_manager2 = SearchHistoryManager(config_dir=temp_dir, max_history=5)
        history2 = history_manager2.get_history()
        print(f"History from new manager instance: {history2}")
        assert history == history2  # Should be the same
        
        print("\n5. Testing filtered history...")
        filtered = history_manager.get_filtered_history("r")
        print(f"History filtered by 'r': {filtered}")
        expected_r_items = [item for item in history if item.lower().startswith("r")]
        assert filtered == expected_r_items
        
        print("\n6. Testing clear history...")
        history_manager.clear_history()
        history = history_manager.get_history()
        print(f"History after clear: {history}")
        assert len(history) == 0
        
        print("\n✅ All search history tests passed!")
        
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_edge_cases():
    """Test edge cases for search history."""
    print("\nTesting edge cases...")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        history_manager = SearchHistoryManager(config_dir=temp_dir, max_history=3)
        
        # Test empty/invalid searches
        history_manager.add_search("")
        history_manager.add_search("  ")
        history_manager.add_search("a")  # Too short
        
        history = history_manager.get_history()
        print(f"History after invalid searches: {history}")
        assert len(history) == 0
        
        # Test valid searches
        history_manager.add_search("resistor")
        history_manager.add_search("  capacitor  ")  # With whitespace
        
        history = history_manager.get_history()
        print(f"History after valid searches: {history}")
        assert len(history) == 2
        assert "capacitor" in history
        assert "  capacitor  " not in history  # Should be trimmed
        
        print("✅ Edge case tests passed!")
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    try:
        test_search_history()
        test_edge_cases()
        print("\n🎉 All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()