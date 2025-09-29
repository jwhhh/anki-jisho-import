# Sample Anki Note Template for Jisho Import Add-on

This file contains sample HTML templates for your Anki cards that work well with the Jisho Import add-on.

## Sample Card Templates

### Front Template (Question Side)
```html
<div class="card">
    <div class="japanese-word">{{Japanese}}</div>
    <div class="metadata">
        {{#JLPT}}<span class="jlpt">{{JLPT}}</span>{{/JLPT}}
        {{#Common}}<span class="common">Common: {{Common}}</span>{{/Common}}
    </div>
</div>
```

### Back Template (Answer Side)
```html
<div class="card">
    <div class="japanese-word">{{Japanese}}</div>
    
    {{#Reading}}
    <div class="reading">{{Reading}}</div>
    {{/Reading}}

    {{#Meaning}}
    <div class="meaning">{{Meaning}}</div>
    {{/Meaning}}
    
    {{#PartOfSpeech}}
    <div class="pos">{{PartOfSpeech}}</div>
    {{/PartOfSpeech}}
    
    <div class="metadata">
        {{#JLPT}}<span class="jlpt">{{JLPT}}</span>{{/JLPT}}
        {{#Common}}<span class="common">Common: {{Common}}</span>{{/Common}}
    </div>
</div>
```

### Styling (CSS)
```css
.card {
    font-family: "Hiragino Kaku Gothic Pro", "ヒラギノ角ゴ Pro W3", "Noto Sans CJK JP", "Yu Gothic", "游ゴシック", "メイリオ", Meiryo, sans-serif;
    text-align: center;
    color: #333;
    background: #f9f9f9;
    padding: 20px;
    border-radius: 10px;
    max-width: 500px;
    margin: 0 auto;
}

.japanese-word {
    font-size: 3em;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 10px;
    line-height: 1.2;
}

.reading {
    font-size: 1.5em;
    color: #e74c3c;
    margin-bottom: 15px;
    font-weight: 500;
}

.meaning {
    font-size: 1.2em;
    color: #27ae60;
    margin-bottom: 15px;
    line-height: 1.4;
    font-weight: 500;
}

.pos {
    font-size: 0.9em;
    color: #8e44ad;
    font-style: italic;
    margin-bottom: 15px;
}

.metadata {
    font-size: 0.8em;
    color: #7f8c8d;
    border-top: 1px solid #bdc3c7;
    padding-top: 10px;
}

.jlpt-badge, .jlpt {
    background: #3498db;
    color: white;
    padding: 3px 8px;
    border-radius: 15px;
    font-size: 0.8em;
    font-weight: bold;
    margin-right: 10px;
}

.common {
    background: #f39c12;
    color: white;
    padding: 3px 8px;
    border-radius: 15px;
    font-size: 0.8em;
}

/* Mobile responsive */
@media (max-width: 600px) {
    .card {
        padding: 15px;
    }
    
    .japanese-word {
        font-size: 2.5em;
    }
    
    .reading {
        font-size: 1.3em;
    }
    
    .meaning {
        font-size: 1.1em;
    }
}
```

## How to Apply These Templates

### Setting Up Multiple Card Types

#### Option 1: Single Note Type with Multiple Card Templates
1. **Open Anki** and go to **Browse**
2. **Select your note type** and click **Cards...** button (or press Ctrl+L)
3. **For the first card (Japanese → English)**:
   - Use the original Front and Back templates above
4. **Add a second card template**:
   - Click the **"+"** button to add a new card template
   - Name it "Reverse" or "English → Japanese"  
   - Use the Reverse Card templates above
5. **Copy and paste the CSS** (includes both regular and reverse styles)
6. **Click Close** to save

#### Option 2: Separate Note Types
Create two different note types if you want to control which cards get which template:

1. **"Japanese Vocabulary"** - Uses the regular template (Japanese → English)
2. **"Japanese Recall"** - Uses the reverse template (English → Japanese)

### Basic Setup (Single Card Type)
1. **Open Anki** and go to **Browse**
2. Click **Cards...** button (or press Ctrl+L)
3. **Copy and paste** the Front Template, Back Template, and Styling into the respective sections
4. **Click Close** to save

## Required Fields for Your Note Type

Make sure your note type includes these fields:
- `Japanese` - Main Japanese word
- `Reading` - Kana reading
- `Meaning` - English definitions
- `JLPT` - JLPT level (optional)
- `PartOfSpeech` - Grammar info (optional)
- `Common` - Frequency indicator (optional)

## Customization Tips

### Color Scheme
- **Japanese word**: Dark blue (`#2c3e50`)
- **Reading**: Red (`#e74c3c`)
- **Meaning**: Green (`#27ae60`)
- **Parts of speech**: Purple (`#8e44ad`)
- **JLPT badge**: Blue (`#3498db`)
- **Common badge**: Orange (`#f39c12`)

### Font Customization
The template uses Japanese-friendly fonts:
- **Hiragino Kaku Gothic Pro** (macOS)
- **Noto Sans CJK JP** (Cross-platform)
- **Yu Gothic** (Windows)
- **Meiryo** (Windows fallback)

### Adding Audio Support
If you want to add audio in the future, add this to your template:
```html
{{#Audio}}
<div class="audio">{{Audio}}</div>
{{/Audio}}
```

### Adding Example Sentences
If you want to add example sentences later:
```html
{{#Example}}
<div class="example">{{Example}}</div>
{{/Example}}
```

## Alternative Layouts

### Reverse Card Template (English → Japanese)
Perfect for testing recall from meaning to Japanese word and reading.

#### Front Template (Question Side)
```html
<div class="card reverse">
    {{#Meaning}}
    <div class="meaning-prompt">{{Meaning}}</div>
    {{/Meaning}}
    
    {{#PartOfSpeech}}
    <div class="pos-hint">{{PartOfSpeech}}</div>
    {{/PartOfSpeech}}
    
    <div class="metadata">
        {{#JLPT}}<span class="jlpt">{{JLPT}}</span>{{/JLPT}}
        {{#Common}}<span class="common">Common: {{Common}}</span>{{/Common}}
    </div>
</div>
```

#### Back Template (Answer Side)
```html
<div class="card reverse">
    {{#Meaning}}
    <div class="meaning-prompt">{{Meaning}}</div>
    {{/Meaning}}
    
    <div class="answer-section">
        <div class="japanese-word">{{Japanese}}</div>
        
        {{#Reading}}
        <div class="reading">{{Reading}}</div>
        {{/Reading}}
    </div>
    
    {{#PartOfSpeech}}
    <div class="pos">{{PartOfSpeech}}</div>
    {{/PartOfSpeech}}
    
    <div class="metadata">
        {{#JLPT}}<span class="jlpt">{{JLPT}}</span>{{/JLPT}}
        {{#Common}}<span class="common">Common: {{Common}}</span>{{/Common}}
    </div>
</div>
```

#### Additional CSS for Reverse Cards
Add this CSS to your existing styling:

```css
/* Reverse card specific styling */
.card.reverse {
    background: #f0f8ff;
    border: 2px solid #3498db;
}

.meaning-prompt {
    font-size: 1.4em;
    color: #27ae60;
    font-weight: 600;
    margin-bottom: 20px;
    line-height: 1.4;
    background: white;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #27ae60;
}

.pos-hint {
    font-size: 0.95em;
    color: #8e44ad;
    font-style: italic;
    margin-bottom: 15px;
    opacity: 0.8;
}

.instruction {
    font-size: 0.9em;
    color: #7f8c8d;
    font-style: italic;
    margin-top: 15px;
    padding: 8px;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 4px;
}

.answer-section {
    margin: 20px 0;
    padding: 15px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}

.answer-section .japanese-word {
    font-size: 2.8em;
    margin-bottom: 8px;
}

.answer-section .reading {
    font-size: 1.4em;
    margin-bottom: 0;
}
```

### Minimalist Layout
For a cleaner look, use this simpler front template:
```html
<div class="minimal-card">
    {{Japanese}}
</div>
```

With this CSS:
```css
.minimal-card {
    font-family: "Noto Sans CJK JP", sans-serif;
    font-size: 4em;
    text-align: center;
    color: #2c3e50;
    background: white;
    padding: 40px 20px;
    border: 2px solid #ecf0f1;
    border-radius: 8px;
}
```

### Detailed Study Layout
For comprehensive study sessions:
```html
<!-- Front: Shows everything except meaning -->
<div class="study-card">
    <div class="word">{{Japanese}}</div>
    <div class="reading">{{Reading}}</div>
    {{#JLPT}}<div class="level">{{JLPT}}</div>{{/JLPT}}
    {{#PartOfSpeech}}<div class="grammar">{{PartOfSpeech}}</div>{{/PartOfSpeech}}
</div>

<!-- Back: Shows meaning -->
<div class="study-card">
    <div class="word">{{Japanese}}</div>
    <div class="reading">{{Reading}}</div>
    <div class="meaning">{{Meaning}}</div>
    <div class="metadata">
        {{#JLPT}}{{JLPT}}{{/JLPT}}
        {{#PartOfSpeech}} • {{PartOfSpeech}}{{/PartOfSpeech}}
        {{#Common}} • {{Common}}{{/Common}}
    </div>
</div>
```

Choose the layout that best fits your study style! 📚✨