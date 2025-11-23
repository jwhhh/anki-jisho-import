#!/usr/bin/env python3
"""
Test script for Jisho.org API functionality with audio support
Run this script to test the API connection and data parsing
without needing to install the add-on in Anki first.
"""

import json
import requests
from urllib.parse import quote
from jisho_parser import parse_jisho_result

def test_jisho_audio(word, reading):
    """Test Jisho.org audio extraction"""
    print(f"🎵 Testing Jisho.org audio for: {word} ({reading})")
    
    try:
        # Request the Jisho.org search page
        url = f"https://jisho.org/search/{quote(word)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        html_content = response.text
        
        # Look for audio URLs in the HTML
        import re
        audio_pattern = r'//d1vjc5dkcd3yh2\.cloudfront\.net/audio/([a-f0-9]{32})\.mp3'
        matches = re.findall(audio_pattern, html_content)
        
        if matches:
            audio_hash = matches[0]
            audio_url = f"https://d1vjc5dkcd3yh2.cloudfront.net/audio/{audio_hash}.mp3"
            print(f"   ✅ Jisho.org: Found audio - {audio_url}")
            
            # Test if the audio URL is accessible
            audio_response = requests.head(audio_url, timeout=5)
            if audio_response.status_code == 200:
                print(f"   ✅ Audio file is accessible")
            else:
                print(f"   ⚠️  Audio file status: {audio_response.status_code}")
        else:
            print(f"   ❌ Jisho.org: No audio found for {word}")
            
    except Exception as e:
        print(f"   ❌ Jisho.org audio test failed: {e}")

def test_audio_sources(word, reading):
    """Test various audio sources for a Japanese word"""
    # Test the Jisho.org audio extraction
    test_jisho_audio(word, reading)

def test_jisho_api():
    """Test the Jisho.org API with sample words"""
    
    test_words = ["猫", "食べる", "美しい", "こんにちは", "arigatou", "付く"]
    
    print("🧪 Testing Jisho.org API Integration with Audio Support")
    print("=" * 60)
    
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
            # Print the formatted numbered meanings (one sense per line)
            print("   Meanings:")
            print(parsed.get('meanings', 'N/A'))
            # If parser exposes grouped and flat lists, show them for clarity
            if parsed.get('meanings_grouped') is not None:
                print(f"   Meanings (grouped list): {parsed.get('meanings_grouped')}")
            if parsed.get('meanings_list') is not None:
                print(f"   Meanings (flat list): {parsed.get('meanings_list')}")
            print(f"   JLPT: {parsed.get('jlpt', 'N/A')}")
            print(f"   Parts of Speech: {parsed.get('pos', 'N/A')}")
            print(f"   Common: {parsed.get('common', 'N/A')}")
            
            # Test audio sources for this word
            if parsed.get('kanji') and parsed.get('reading'):
                test_audio_sources(parsed.get('kanji'), parsed.get('reading'))
            
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
    