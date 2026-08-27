# The Last Night

Browser-based horror survival/card game set in Blackwood.

## Current architecture

The original project was a single ~80 KB `index.html` containing markup, styles, game data, combat logic, story systems, inventory systems, and rendering code. The refactor branch separates those responsibilities without intentionally changing gameplay:

- `index.html` — page structure and game UI containers
- `styles.css` — all presentation and responsive styling
- `game.js` — existing gameplay/data/rendering logic, preserved for compatibility
- `docs/ARCHITECTURE.md` — next-stage modularization plan

## Refactor safety

This work lives on `refactor-clean-architecture`. The `main` branch remains unchanged until the refactor is tested.

## Next refactor stages

1. Remove inline `onclick` handlers and centralize DOM events.
2. Split static game data into dedicated files.
3. Split combat, story, inventory, save state, and UI rendering.
4. Add a single state-management layer and validation helpers.
5. Add smoke tests for game start, turn progression, combat, story progression, inventory, and night transitions.
