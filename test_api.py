#!/usr/bin/env python3
"""
Test script for Jisho.org API functionality
Run this script to test the API connection and data parsing
without needing to install the add-on in Anki first.
"""

import json
import requests
from urllib.parse import quote
from jisho_parser import parse_jisho_result

def test_jisho_api():
    """Test the Jisho.org API with sample words"""
    
    test_words = ["猫", "食べる", "美しい", "こんにちは", "arigatou"]
    
    print("🧪 Testing Jisho.org API Integration")
    print("=" * 50)
    
    for word in test_words:
        print(f"\n🔍 Testing word: {word}")
        print("-" * 30)
        
        try:
            # Make API request
            url = f"https://jisho.org/api/v1/search/words?keyword={quote(word)}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('data'):
                print("❌ No results found")
                continue
            
            # Parse first result
            result = data['data'][0]
            parsed = parse_jisho_result(result)
            
            # Display results
            print(f"✅ Found result:")
            print(f"   Kanji: {parsed.get('kanji', 'N/A')}")
            print(f"   Reading: {parsed.get('reading', 'N/A')}")
            print(f"   Meanings: {parsed.get('meanings', 'N/A')}")
            print(f"   JLPT: {parsed.get('jlpt', 'N/A')}")
            print(f"   Parts of Speech: {parsed.get('pos', 'N/A')}")
            print(f"   Common: {parsed.get('common', 'N/A')}")
            
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API test completed!")



def test_field_mapping():
    """Test the field mapping logic"""
    print("\n🧪 Testing Field Mapping Logic")
    print("=" * 50)
    
    # Simulate different field name scenarios
    test_cases = [
        {
            'available_fields': ['Japanese', 'Reading', 'Meaning', 'JLPT'],
            'target_field': 'Japanese',
            'expected': 'Japanese'
        },
        {
            'available_fields': ['Word', 'Kana', 'Definition', 'Level'], 
            'target_field': 'Japanese',
            'expected': 'Word'
        },
        {
            'available_fields': ['Front', 'Back', 'Extra'],
            'target_field': 'Japanese', 
            'expected': None
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}:")
        print(f"   Available fields: {case['available_fields']}")
        print(f"   Looking for: {case['target_field']}")
        
        result = find_matching_field(case['target_field'], case['available_fields'])
        print(f"   Found: {result}")
        print(f"   Expected: {case['expected']}")
        
        if result == case['expected']:
            print("   ✅ PASS")
        else:
            print("   ❌ FAIL")

def find_matching_field(target_field, available_fields):
    """Simulate the field matching logic from the add-on"""
    # Try exact match first (case-insensitive)
    for field_name in available_fields:
        if field_name.lower() == target_field.lower():
            return field_name
    
    # Try fuzzy matching
    field_variations = {
        'japanese': ['japanese', 'word', 'kanji', 'japanese_word'],
        'reading': ['reading', 'kana', 'hiragana', 'pronunciation', 'furigana'],
        'meaning': ['meaning', 'definition', 'english', 'translation', 'definitions'],
        'jlpt': ['jlpt', 'jlpt_level', 'level', 'jlptlevel'],
        'partofspeech': ['partofspeech', 'pos', 'grammar', 'type', 'part_of_speech'],
        'common': ['common', 'frequency', 'popular', 'commonness']
    }
    
    field_key = target_field.lower().replace('_', '').replace(' ', '')
    if field_key in field_variations:
        for variant in field_variations[field_key]:
            for field_name in available_fields:
                if variant in field_name.lower().replace('_', '').replace(' ', ''):
                    return field_name
    
    return None

if __name__ == "__main__":
    # Test API functionality
    try:
        test_jisho_api()
        test_field_mapping()
        
        print("\n✨ All tests completed!")
        print("If you see successful API responses above, the add-on should work correctly in Anki.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your internet connection and try again.")
    