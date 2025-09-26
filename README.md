# Duplicate Highlighter

A simple Python GUI application that automatically highlights duplicate words in text as you type. Built with Tkinter, this tool helps identify repetitive language and improve writing quality.

## Features

- **Real-time highlighting**: Duplicate words are highlighted instantly as you type
- **Stop word filtering**: Ignores common function words and punctuation marks to focus on meaningful duplicates
- **Case-insensitive matching**: Treats "Word" and "word" as the same for duplicate detection

## Use Cases

- **Writing improvement**: Identify repetitive language in essays, articles, or documents
- **Content editing**: Spot overused words in blog posts or marketing copy
- **Academic writing**: Ensure variety in research papers and reports
- **Creative writing**: Avoid repetitive vocabulary in stories and novels
- **General text analysis**: Quickly identify patterns in any written content

## Screenshots

The application features a clean text editor with duplicate words highlighted in light green (#8cf5b7).

## Installation

### Prerequisites

- Python 3.6 or higher
- Tkinter (usually included with Python)

### Running the Application

1. Clone or download this repository
2. Navigate to the project directory
3. Run the application:

```bash
python app.py
```

## How It Works

### Word Detection Algorithm

The application uses a regex pattern to identify words:

```python
r"[A-Za-z0-9_']+(?:[.,;:!?\-]+[A-Za-z0-9_']+)*|[.,;:!?\-]+"
```

This pattern:
- Recognizes words containing letters, numbers, underscores, and apostrophes
- Handles contractions like "didn't", "won't", "can't" as single words
- Supports words with embedded punctuation (e.g., "e.g.", "i.e.")
- Identifies standalone punctuation marks

### Stop Word Filtering

The application maintains a list of function words and punctuation that are ignored during duplicate detection:

- Articles: "the", "a", "an"
- Prepositions: "in", "on", "at", "by", "with", etc.
- Pronouns: "I", "you", "he", "she", "they", etc.
- Common verbs: "is", "are", "was", "were", "be", etc.
- Punctuation: ".", ",", "!", "?", ":", ";", "-"

### Highlighting Logic

1. Extract all words from the text using regex
2. Convert to lowercase and filter out stop words
3. For each unique word, count occurrences using overlapping substring matching
4. Highlight words that appear 2 or more times
5. Update highlights in real-time as text changes

## Technical Details

### Dependencies

- `tkinter`: GUI framework (included with Python)
- `re`: Regular expressions (included with Python)

### File Structure

```
duplicate-highlighter/
├── app.py          # Main application file
├── groceries.txt   # Sample text file
└── README.md       # This file
```

### Key Functions

- `highlight_duplicates()`: Core function that finds and highlights duplicate words
- `on_text_modified()`: Event handler for real-time text updates
- `show_context_menu()`: Manages right-click context menu functionality
- `main()`: Application initialization and GUI setup

## Customization

### Changing Highlight Color

Modify the highlight color by changing the background color in the tag configuration:

```python
text.tag_configure("dup_highlight", background="#your_color_here")
```

### Adjusting Font

Change the font family and size in the main function:

```python
chosen = "Your Font Name"
font_pt_size = 20  # Adjust size as needed
```

### Adding Stop Words

Add words to the `FUNCTION_WORDS` set to exclude them from duplicate detection:

```python
FUNCTION_WORDS = {
    "the", "a", "an", # ... existing words
    "your", "new", "stop", "words"  # Add your words here
}
```