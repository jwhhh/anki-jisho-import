# Anki Jisho Import Add-on

An Anki add-on that automatically fills Japanese word information using the Jisho.org API. Simply type a Japanese word and let the add-on fetch meanings, readings, JLPT levels, and other useful information.

## Demo

![Demo Video](demo.mov)

*The add-on in action: Type Japanese text → Press Ctrl+J → All fields automatically filled and corrected!*

## Features

- 🔍 **Automatic word lookup** using Jisho.org API
- 📚 **Multiple data fields**: Kanji, readings, English meanings, JLPT levels, parts of speech
- ⌨️ **Keyboard shortcuts**: Ctrl+J to open the search dialog
- 🎯 **Smart field mapping**: Automatically maps data to your note fields

## Installation

### Option 1: Install from Source
1. Clone or download this repository
2. Navigate to the project directory in your terminal
3. Create the add-on package:
   ```bash
   zip -r JishoImport.ankiaddon . -x "*.git*" "*.DS_Store*" "__pycache__/*" "*.pyc"
   ```
4. Open Anki
5. Go to **Tools** → **Add-ons** → **Install from file...**
6. Select the `JishoImport.ankiaddon` file you just created
7. Restart Anki

### Option 2: Manual Installation
1. Clone or download this repository
2. Copy the entire folder to your Anki add-ons directory:
   - **Windows**: `%APPDATA%\Anki2\addons21\`
   - **Mac**: `~/Library/Application Support/Anki2/addons21/`
   - **Linux**: `~/.local/share/Anki2/addons21/`
3. Restart Anki

## How to Use

### Method 1: Auto-fill from Japanese field (Recommended)
1. Open the Add/Edit note dialog
2. Type the Japanese word in your "Japanese" field (can be kanji, hiragana, katakana, or romaji)
3. Press **Ctrl+J**
4. The add-on will automatically search and fill/update all fields:
   - **Japanese field**: Updated with the accurate kanji/kana form from Jisho
   - **Other fields**: Filled with reading, meaning, JLPT level, etc.

### Method 2: Manual search dialog
1. Open the Add/Edit note dialog
2. Press **Ctrl+J** if the Japanese field is empty, or click the "Jisho" button
3. Type the Japanese word you want to look up
4. Click "Search" or press Enter
5. Review the results and click "Import to Note"

## Setting Up Your Note Type

For the add-on to work properly, your note type should have the following fields (field names are case-insensitive):

### Essential Fields
- **Japanese** - For the main Japanese word (kanji/kana)
- **Reading** - For the hiragana/katakana reading
- **Meaning** - For English definitions

### Optional Fields
- **JLPT** - For JLPT level information
- **PartOfSpeech** - For grammatical categories (noun, verb, etc.)
- **Common** - Indicates if the word is commonly used

### Creating Fields
1. Go to **Tools > Manage Note Types**
2. Select your note type and click **"Fields..."**
3. Add the required fields above
4. Restart Anki

## Examples

### Example 1: Auto-correction from hiragana
**Input**: Type `ねこ` in Japanese field → Press Ctrl+J
**Results**:
- **Japanese**: `猫` (corrected to kanji)
- **Reading**: `ねこ`
- **Meaning**: `cat (esp. the domestic cat, Felis catus); shamisen; geisha`
- **JLPT**: `jlpt-n5`
- **PartOfSpeech**: `Noun`
- **Common**: `Yes`

### Example 2: Looking up "食べる" (kanji input)
**Input**: Type `食べる` in Japanese field → Press Ctrl+J
**Results**:
- **Japanese**: `食べる` (unchanged - already correct)
- **Reading**: `たべる`
- **Meaning**: `to eat; to live on (e.g. a salary); to live off; to subsist on`
- **JLPT**: `jlpt-n5`
- **PartOfSpeech**: `Ichidan verb, Transitive verb`
- **Common**: `Yes`

### Example 3: Romaji input
**Input**: Type `arigatou` in Japanese field → Press Ctrl+J
**Results**:
- **Japanese**: `有り難う` (converted from romaji)
- **Reading**: `ありがとう`
- **Meaning**: `thank you; thanks`
- **JLPT**: `jlpt-n3`

## Configuration

You can customize the keyboard shortcut by editing the `config.json` file:

```json
{
    "keyboard_shortcut": "Ctrl+J"
}
```