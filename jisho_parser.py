"""
Jisho.org API parsing utilities
Centralized parsing logic for both the main add-on and testing
"""

def parse_jisho_result(result):
    """Parse Jisho.org API result into structured data"""
    parsed = {}
    
    # Japanese text - use slug as primary, fallback to japanese[0].word
    parsed['kanji'] = result.get('slug', '')
    if not parsed['kanji']:
        japanese = result.get('japanese', [{}])[0]
        parsed['kanji'] = japanese.get('word', '')
    
    # Reading - from japanese[0].reading
    japanese = result.get('japanese', [{}])[0]
    parsed['reading'] = japanese.get('reading', '')
    
    # English meanings
    senses = result.get('senses', [])
    if senses:
        # Get all English definitions (exclude Wikipedia definitions)
        definitions = []
        for sense in senses:
            # Skip Wikipedia definitions
            parts_of_speech = sense.get('parts_of_speech', [])
            if 'Wikipedia definition' in parts_of_speech:
                continue
            
            english_definitions = sense.get('english_definitions', [])
            if english_definitions:
                definitions.extend(english_definitions)
        
        parsed['meanings'] = '; '.join(definitions[:5])  # Limit to first 5 meanings
        
        # Get parts of speech (exclude Wikipedia)
        parts_of_speech = []
        for sense in senses:
            pos_list = sense.get('parts_of_speech', [])
            if 'Wikipedia definition' not in pos_list:
                parts_of_speech.extend(pos_list)
        
        # Remove duplicates and limit
        unique_pos = list(dict.fromkeys(parts_of_speech))  # Preserve order while removing dupes
        parsed['pos'] = ', '.join(unique_pos[:3])  # Limit to first 3 unique POS
    else:
        parsed['meanings'] = ''
        parsed['pos'] = ''
    
    # JLPT level - it's a list, take the first one
    jlpt_list = result.get('jlpt', [])
    parsed['jlpt'] = jlpt_list[0] if jlpt_list else ''
    
    # Common/frequency info
    parsed['common'] = 'Yes' if result.get('is_common', False) else 'No'
    
    return parsed