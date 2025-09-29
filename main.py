import json
import requests
from urllib.parse import quote
from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.utils import showInfo, showCritical, tooltip
from anki.hooks import addHook
import re
import os
from .jisho_parser import parse_jisho_result


class JishoImporter:
    """Main class for Jisho.org API integration"""
    
    def __init__(self):
        self.jisho_api_url = "https://jisho.org/api/v1/search/words"
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Could not load config: {e}")
        
        # Default configuration
        return {
            "field_mappings": {
                "Japanese": "kanji",
                "Reading": "reading",
                "Meaning": "meanings", 
                "JLPT": "jlpt",
                "PartOfSpeech": "pos",
                "Common": "common"
            },
            "keyboard_shortcut": "Ctrl+J"
        }
        
    def search_word(self, word):
        """Search for a Japanese word using Jisho.org API"""
        try:
            # Clean the word input
            word = word.strip()
            if not word:
                return None
                
            # Make API request
            url = f"{self.jisho_api_url}?keyword={quote(word)}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('data'):
                return None
                
            # Get the first result (most relevant)
            result = data['data'][0]
            return parse_jisho_result(result)
            
        except requests.RequestException as e:
            showCritical(f"Network error: {str(e)}")
            return None
        except Exception as e:
            showCritical(f"Error searching word: {str(e)}")
            return None
    
    def get_audio_url(self, word):
        """Generate audio URL for Japanese word"""
        # Using Forvo or similar service would be ideal, but for now we'll use a simple approach
        # You might want to integrate with a TTS service or Forvo API
        return f"https://www.gstatic.com/hostedimg/382a91be5ab2a4e8_large"  # Placeholder


class JishoDialog(QDialog):
    """Dialog for searching and importing word data"""
    
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor
        self.importer = JishoImporter()
        self.setupUI()
        
    def setupUI(self):
        self.setWindowTitle("Jisho Import")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Search input
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Japanese Word:"))
        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self.search_and_fill)
        search_layout.addWidget(self.search_input)
        
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_and_fill)
        search_layout.addWidget(self.search_btn)
        
        layout.addLayout(search_layout)
        
        # Results area
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.import_btn = QPushButton("Import to Note")
        self.import_btn.clicked.connect(self.import_to_note)
        self.import_btn.setEnabled(False)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.current_data = None
    
    def search_and_fill(self):
        """Search for word and display results"""
        word = self.search_input.text().strip()
        if not word:
            return
            
        self.search_btn.setEnabled(False)
        self.search_btn.setText("Searching...")
        
        # Perform search
        data = self.importer.search_word(word)
        
        if data:
            self.current_data = data
            self.display_results(data)
            self.import_btn.setEnabled(True)
        else:
            self.result_area.setPlainText("No results found or error occurred.")
            self.import_btn.setEnabled(False)
            
        self.search_btn.setEnabled(True)
        self.search_btn.setText("Search")
    
    def display_results(self, data):
        """Display search results in the text area"""
        result_text = f"""Found result:

Kanji: {data.get('kanji', 'N/A')}
Reading: {data.get('reading', 'N/A')}
Meanings: {data.get('meanings', 'N/A')}
Parts of Speech: {data.get('pos', 'N/A')}
JLPT Level: {data.get('jlpt', 'N/A')}
Common: {data.get('common', 'N/A')}
"""
        self.result_area.setPlainText(result_text)
    
    def import_to_note(self):
        """Import the current data to the note being edited"""
        if not self.current_data or not self.editor:
            return
            
        # Get field mappings from config
        field_mappings = self.importer.config.get("field_mappings", {})
        
        imported_fields = []
        for field_name, data_key in field_mappings.items():
            value = self.current_data.get(data_key, '')
            if value and self.fill_field(field_name, value):
                imported_fields.append(field_name)
        
        if imported_fields:
            tooltip(f"Imported data to fields: {', '.join(imported_fields)}")
        else:
            showInfo("No matching fields found in your note type. Please check the README for required field names.")
        
        self.close()
    
    def fill_field(self, field_name, value):
        """Fill a specific field in the editor with fuzzy matching"""
        try:
            # Get all field names in the current note type
            field_names = list(self.editor.note.keys())
            
            # Try exact match first (case-insensitive)
            target_field = None
            for fname in field_names:
                if fname.lower() == field_name.lower():
                    target_field = fname
                    break
            
            # If no exact match, try fuzzy matching
            if not target_field:
                field_variations = {
                    'japanese': ['japanese', 'word', 'kanji', 'japanese_word'],
                    'reading': ['reading', 'kana', 'hiragana', 'pronunciation', 'furigana'],
                    'meaning': ['meaning', 'definition', 'english', 'translation', 'definitions'],
                    'jlpt': ['jlpt', 'jlpt_level', 'level', 'jlptlevel'],
                    'partofspeech': ['partofspeech', 'pos', 'grammar', 'type', 'part_of_speech'],
                    'common': ['common', 'frequency', 'popular', 'commonness']
                }
                
                field_key = field_name.lower().replace('_', '').replace(' ', '')
                if field_key in field_variations:
                    for variant in field_variations[field_key]:
                        for fname in field_names:
                            if variant in fname.lower().replace('_', '').replace(' ', ''):
                                target_field = fname
                                break
                        if target_field:
                            break
            
            if target_field:
                self.editor.note[target_field] = value
                self.editor.loadNote()
                return True
            else:
                print(f"Field '{field_name}' not found in note type. Available fields: {field_names}")
                return False
                
        except Exception as e:
            print(f"Error filling field {field_name}: {str(e)}")
            return False


def show_jisho_dialog(editor):
    """Show the Jisho import dialog or auto-search if Japanese field has content"""
    # Try to get content from Japanese field first
    japanese_word = get_japanese_field_content(editor)
    
    if japanese_word:
        # Auto-search and fill if Japanese field has content
        auto_search_and_fill(editor, japanese_word)
    else:
        # Show dialog if no content in Japanese field
        dialog = JishoDialog(editor.parentWindow, editor)
        dialog.exec()


def get_japanese_field_content(editor):
    """Get content from the Japanese field if it exists"""
    try:
        if not editor or not editor.note:
            return None
            
        # Get field mappings from config
        config = load_config()
        field_mappings = config.get("field_mappings", {})
        japanese_data_key = field_mappings.get("Japanese", "kanji")
        
        # Get all field names in the current note type
        field_names = list(editor.note.keys())
        
        # Try to find the Japanese field using the same fuzzy matching logic
        target_field = find_matching_field("Japanese", field_names)
        
        if target_field:
            content = editor.note[target_field]
            return content.strip() if content else None
            
    except Exception as e:
        print(f"Error getting Japanese field content: {e}")
    
    return None


def auto_search_and_fill(editor, word):
    """Automatically search for word and fill fields"""
    try:
        # Show a brief loading message
        tooltip("Searching Jisho.org...")
        
        # Create importer and search
        importer = JishoImporter()
        data = importer.search_word(word)
        
        if data:
            # Get field mappings from config
            field_mappings = importer.config.get("field_mappings", {})
            
            imported_fields = []
            
            # Fill ALL fields including Japanese (to replace with slug)
            for field_name, data_key in field_mappings.items():
                value = data.get(data_key, '')
                if value and fill_field_direct(editor, field_name, value):
                    imported_fields.append(field_name)
            
            if imported_fields:
                tooltip(f"✅ Updated: {', '.join(imported_fields)}", period=3000)
            else:
                tooltip("⚠️ No matching fields found for import", period=2000)
        else:
            tooltip("❌ No results found on Jisho.org", period=2000)
            
    except Exception as e:
        print(f"Error in auto search and fill: {e}")
        tooltip(f"❌ Error: {str(e)}", period=2000)


def find_matching_field(field_name, available_fields):
    """Find matching field using fuzzy matching - extracted from JishoDialog"""
    # Try exact match first (case-insensitive)
    for fname in available_fields:
        if fname.lower() == field_name.lower():
            return fname
    
    # If no exact match, try fuzzy matching
    field_variations = {
        'japanese': ['japanese', 'word', 'kanji', 'japanese_word'],
        'reading': ['reading', 'kana', 'hiragana', 'pronunciation', 'furigana'],
        'meaning': ['meaning', 'definition', 'english', 'translation', 'definitions'],
        'jlpt': ['jlpt', 'jlpt_level', 'level', 'jlptlevel'],
        'partofspeech': ['partofspeech', 'pos', 'grammar', 'type', 'part_of_speech'],
        'common': ['common', 'frequency', 'popular', 'commonness']
    }
    
    field_key = field_name.lower().replace('_', '').replace(' ', '')
    if field_key in field_variations:
        for variant in field_variations[field_key]:
            for fname in available_fields:
                if variant in fname.lower().replace('_', '').replace(' ', ''):
                    return fname
    
    return None


def fill_field_direct(editor, field_name, value):
    """Fill a specific field in the editor - extracted and simplified from JishoDialog"""
    try:
        # Get all field names in the current note type
        field_names = list(editor.note.keys())
        
        # Find matching field
        target_field = find_matching_field(field_name, field_names)
        
        if target_field:
            editor.note[target_field] = value
            editor.loadNote()
            return True
        else:
            print(f"Field '{field_name}' not found in note type. Available fields: {field_names}")
            return False
            
    except Exception as e:
        print(f"Error filling field {field_name}: {str(e)}")
        return False


def load_config():
    """Load configuration - extracted for reuse"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Could not load config: {e}")
    
    # Default configuration
    return {
        "field_mappings": {
            "Japanese": "kanji",
            "Reading": "reading",
            "Meaning": "meanings", 
            "JLPT": "jlpt",
            "PartOfSpeech": "pos",
            "Common": "common"
        },
        "keyboard_shortcut": "Ctrl+J"
    }


def add_jisho_button(buttons, editor):
    """Add Jisho import button to the editor"""
    btn = editor.addButton(
        icon=None,
        cmd="jisho",
        func=lambda e=editor: show_jisho_dialog(e),
        tip="Import from Jisho.org",
        label="Jisho"
    )
    buttons.append(btn)
    return buttons


def setup_shortcuts(editor):
    """Setup keyboard shortcuts"""
    # Get shortcut from config
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                shortcut_key = config.get('keyboard_shortcut', 'Ctrl+J')
        else:
            shortcut_key = 'Ctrl+J'
    except:
        shortcut_key = 'Ctrl+J'
    
    shortcut = QShortcut(QKeySequence(shortcut_key), editor.parentWindow)
    shortcut.activated.connect(lambda: show_jisho_dialog(editor))


# Hook into Anki's editor
gui_hooks.editor_did_init_buttons.append(add_jisho_button)
gui_hooks.editor_did_init.append(setup_shortcuts)


# Initialize the add-on
jisho_importer = JishoImporter()