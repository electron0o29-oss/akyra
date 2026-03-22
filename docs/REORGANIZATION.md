# AKYRA Website Reorganization

Successfully reorganized the AKYRA website from a single 3489-line HTML file into a modular structure.

## New Structure

```
/Users/tgds.2/akyra/
├── index.html              # Clean HTML structure (64KB)
├── css/
│   ├── variables.css       # CSS variables and design tokens (853B)
│   ├── reset.css           # Reset styles, scrollbar, base styles (1.9KB)
│   ├── components.css      # Reusable components (.dlg, .btn, .label, etc.) (5.9KB)
│   └── sections.css        # Section-specific styles (25KB)
└── js/
    ├── neural-network.js   # Neural network canvas in hero (5.1KB)
    ├── society-map.js      # Blockchain network map visualization (16KB)
    ├── live-feed.js        # Live feed ticker (4.2KB)
    ├── terminal.js         # Terminal simulation (3.7KB)
    └── main.js             # Stats counters, scroll animations, globe (19KB)
```

## CSS Files

### 1. css/variables.css
- CSS custom properties (design tokens)
- Color palette (Aegean/Greek deep blue)
- Typography variables
- All `:root` definitions

### 2. css/reset.css
- Global resets (`*, *::before, *::after`)
- HTML and body base styles
- Scrollbar customization
- Grid background pattern
- Base element styling (a, strong, hr)

### 3. css/components.css
All reusable UI components:
- `.wrap` - Layout wrapper
- `.label`, `.gk`, `.gk-lg` - Typography utilities
- `.dlg` - Pixel dialog (RPG-style message boxes)
- `.btn` - Button styles (solid, ghost, sizes)
- `.redacted` - Redacted text style
- Animations (`@keyframes fadeUp`, `pulse`, `ticker`, `type`)
- `.sec-intro`, `.sec-h2` - Section headers
- `.greek-rule` - Decorative Greek divider

### 4. css/sections.css
Section-specific styles for all major sections:
- Live Stats Bar
- Navigation
- Hero section
- What is AKYRA
- Journal/Timeline
- Features Grid
- Why Now
- Whitelist Urgency
- Presale
- Token
- Angel of Death
- The Dead
- Factions
- Agents
- Society Snapshot
- CTA
- Footer

## JavaScript Files

### 1. js/neural-network.js
- Neural network particle canvas animation
- Hero background visualization
- 52 nodes, 110 floating particles
- Signal pulses traveling along edges
- Canvas resizing and animation loop

### 2. js/society-map.js
- Force-directed graph visualization
- 23 agent nodes (leaders, members, dead)
- Relationship links (alliance, conflict, transfer, judge, death)
- Interactive tooltips
- Animated pulses on alliance links
- Monochrome cream/blue design aesthetic

### 3. js/live-feed.js
- Live transaction feed simulator
- 6 transaction types (TRANSFER, ALLIANCE, GOVERN, DEPLOY, EVOLVE, BUILD)
- Automatic event generation every 2.4s
- Transaction counter
- Agent count tracking
- Clock display (UTC time)

### 4. js/terminal.js
- Terminal command simulation
- Three commands: `deploy`, `status`, `help`
- Animated text output with delays
- Auto-runs 'deploy' on first view
- Intersection Observer for viewport detection

### 5. js/main.js
- Live stats bar counters
- Why Now section scroll animations
- Timeline drag-to-scroll
- Waitlist counter animation
- Navigation scroll effects
- Scroll fade-up animations
- Angel of Death bar animations
- **Three.js Globe visualization**:
  - 12 agent locations worldwide
  - Alliance arcs between agents
  - Interactive labels and tooltips
  - Drag to rotate
  - Auto-rotation with inertia
  - Agent status indicators

## Key Features Preserved

✓ All functionality intact
✓ Same class names and structure
✓ All animations preserved
✓ Interactive elements working
✓ Three.js globe visualization
✓ Canvas animations (neural network, society map)
✓ Live feed and counters
✓ Terminal simulation
✓ Scroll effects and observers

## HTML Structure

The `index.html` file now:
- Contains only HTML markup
- Links to 4 external CSS files
- Links to 5 external JavaScript files
- Includes Three.js CDN for globe visualization
- Maintains all original content and structure
- Keeps inline styles only where semantically necessary (inline color values, etc.)

## Benefits of This Structure

1. **Maintainability**: Each file has a clear, single purpose
2. **Readability**: Styles and scripts are organized logically
3. **Performance**: Browsers can cache CSS/JS files separately
4. **Debugging**: Easier to locate and fix issues
5. **Collaboration**: Multiple developers can work on different files
6. **Reusability**: Components can be easily reused or modified
7. **Documentation**: Clear comments in each file explain purpose

## Usage

Simply open `/Users/tgds.2/akyra/index.html` in a browser. All CSS and JavaScript will load from their respective files. The website will function identically to the original single-file version.

## Original File

The original `/Users/tgds.2/akyra/akyra-final.html` (144KB) has been preserved and remains unchanged.
