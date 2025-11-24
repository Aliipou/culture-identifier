# Screenshots Guide

## How to Add Screenshots

To capture and add screenshots to this project:

### 1. Take Screenshots

Run the application and capture these views:

**Main Interface** (`main-interface.png`)
- Navigate to http://localhost:5000
- Show the clean interface with the text input area
- Include the header and "Share Your Thoughts" section
- Capture at ~1920x1080 resolution

**Analysis Results** (`analysis-results.png`)
- Enter sample text and click "Analyze My Writing"
- Wait for results to appear
- Capture the full results section showing:
  - Top 3 matches with scores
  - Cultural figure cards with explanations
  - Book recommendations
- Show at least 2 complete match cards

**Cultural Landscape** (`cultural-landscape.png`)
- Scroll to the "Cultural Landscape" section
- Capture the 2D scatter plot visualization
- Ensure the "You" point is clearly visible
- Include the surrounding cultural figures

**Writing Analysis** (`writing-analysis.png`)
- Scroll to "Your Writing Analysis" section
- Capture the full dashboard showing:
  - Word count, sentence count
  - Average sentence length
  - Question density, complex words
  - Detected themes

### 2. Optimize Screenshots

```bash
# Install imagemagick (optional)
# Resize images to consistent width
magick convert main-interface.png -resize 1200 main-interface.png

# Or use any image editor to:
# - Resize to reasonable width (1000-1400px)
# - Optimize file size
# - Save as PNG for quality
```

### 3. Add to Repository

Place screenshots in this directory:
```
screenshots/
├── main-interface.png
├── analysis-results.png
├── cultural-landscape.png
└── writing-analysis.png
```

### 4. Reference in README

The main README.md already includes the screenshot references. Just make sure the filenames match exactly.

## Sample Text for Screenshots

Use this text for consistent screenshots:

```
Life is a continuous dance between ambition and doubt, between the desire to create
something meaningful and the suspicion that meaning itself is a moving target.

What fascinates me is how people cling to illusions just to stay functional. We invent
routines, values, even identities, hoping they'll hold still long enough to guide us.
Yet every time I push deeper — through study, work, or observation — I'm reminded how
unstable the foundations really are. Maybe that's not a problem. Maybe clarity comes
from accepting that the ground is always shifting.

I keep returning to the same question: if certainty is a myth, then what actually deserves
commitment? For me, it's the pursuit of mastery, the refusal to settle for comfortable
narratives. There's something compelling about testing ideas against reality, watching
them evolve or break apart entirely.
```

This should generate matches with existential philosophers like Albert Camus or Jean-Paul Sartre.

## Tips for Quality Screenshots

1. **Clear Window**: Close unnecessary browser tabs and windows
2. **Full Screen**: Use F11 or maximize window for clean captures
3. **Dark/Light Mode**: Capture in the mode that matches your documentation
4. **Zoom Level**: Use 100% browser zoom for crisp screenshots
5. **Scroll Position**: Center the content you're capturing
6. **No Personal Data**: Don't include personal text in public screenshots

## Screenshot Tools

### Windows
- **Snipping Tool**: Win + Shift + S
- **Game Bar**: Win + G, then screenshot
- **ShareX**: Free, powerful screenshot tool

### Mac
- **Command + Shift + 4**: Select area
- **Command + Shift + 3**: Full screen

### Linux
- **Flameshot**: Powerful annotation tool
- **GNOME Screenshot**: Built-in tool

## Updating Screenshots

When updating the UI or features:
1. Retake affected screenshots
2. Keep naming consistent
3. Update README if adding new screenshots
4. Commit with message: "docs: update screenshots"
