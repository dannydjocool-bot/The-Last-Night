# Architecture Refactor Plan

## Goal

Make The Last Night easier to expand without changing existing gameplay behavior.

## Current risks

The game has grown organically inside one global script. Systems reference the same global state directly, rendering and game rules are mixed together, boss outcomes repeat similar code, and inline HTML handlers make functions part of the public global API.

## Target layout

```
index.html
styles.css
js/
  data/
    locations.js
    survivors.js
    creatures.js
    items.js
    story.js
  core/
    state.js
    rules.js
    save.js
  systems/
    combat.js
    inventory.js
    encounters.js
    progression.js
    night.js
  ui/
    render.js
    events.js
    log.js
  main.js
```

## Migration order

**Stage 1 — complete in this branch:** extract CSS and JavaScript from the HTML while preserving behavior.

**Stage 2:** move static location, survivor, creature, item, rarity, and story definitions into data files. No rule changes.

**Stage 3:** isolate combat and boss-resolution code. Repeated boss reward/defeat handling should become one shared function.

**Stage 4:** isolate inventory, Extra Pockets, ammo, weapon durability, and item-use logic.

**Stage 5:** isolate story objectives, clues, location discovery, night progression, and endings.

**Stage 6:** replace inline `onclick` attributes with centralized event listeners and a small action dispatcher.

**Stage 7:** introduce save-versioning and automated smoke tests.

## Rules for the refactor

- Preserve current balancing and numbers unless a separate gameplay change is requested.
- Keep `main` untouched until the refactor build is tested.
- Make small commits so regressions can be isolated.
- Prefer named helper functions over duplicated boss/survivor logic.
- Keep UI rendering separate from state mutation wherever practical.
