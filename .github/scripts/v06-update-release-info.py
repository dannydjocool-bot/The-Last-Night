from pathlib import Path
import re

path = Path('index.html')
text = path.read_text()

# Keep main-menu version labels consistent.
text = text.replace('>V-0.5 Beta</button>', '>V-0.6 Beta</button>')
text = text.replace('V-0.5 Beta — Early Development', 'V-0.6 Beta — Early Development')

# Update library badge accessibility labels.
text = text.replace('aria-label="View V-0.5 Beta update details">New Update</a>', 'aria-label="View V-0.6 Beta update details">New Update</a>')
text = text.replace('aria-label="View V-0.4 Beta previous update details">Previous Update</a>', 'aria-label="View V-0.5 Beta previous update details">Previous Update</a>')

current = '''<section id="updateDetailsPanel" aria-labelledby="updateDetailsTitle">
  <div class="update-details-card">
    <div class="update-details-kicker">Latest Build</div>
    <h2 id="updateDetailsTitle">V-0.6 Beta — New Update</h2>
    <p>Blackwood feels more alive and unpredictable. V-0.6 focuses on deeper horror atmosphere, more reactive nights, and stronger endgame reliability.</p>
    <ul class="update-details-list">
      <li><strong>Blackwood Feels Alive:</strong> Added Night Modifiers, location-specific horror events, rare anomalies, Fear/Sanity hallucinations, and more reactive exploration moments.</li>
      <li><strong>Blackwood Journal:</strong> Important discoveries, warnings, boss encounters, relationship moments, and strange events can now be recorded during a run.</li>
      <li><strong>Survivor Relationships:</strong> Survivors can build Trust by surviving battles together, creating meaningful party bonuses over time.</li>
      <li><strong>Expanded Encounters:</strong> Added exploration choices, dramatic high-rarity creature introductions, and escalating creature phases as enemies become wounded.</li>
      <li><strong>Horror Soundtrack Overhaul:</strong> Replaced the engine-like ambience with a darker cinematic horror score using sparse music, distant tones, heartbeat-like impacts, and atmospheric movement.</li>
      <li><strong>Root Gate Reliability:</strong> Fixed Special Ability kills so Root Gate Guardians and The Triune Maw correctly advance the story, respect Triune Armor, and unlock the final Root encounter.</li>
      <li><strong>UI &amp; Mobile Polish:</strong> Improved V-0.6 overlay placement and prevented the Blackwood Journal from covering important game controls.</li>
    </ul>
    <a class="update-details-back" href="#gameLibrary">← Back to Library</a>
  </div>
</section>'''

previous = '''<section id="previousUpdatePanel" aria-labelledby="previousUpdateTitle">
  <div class="update-details-card">
    <div class="update-details-kicker">Previous Build</div>
    <h2 id="previousUpdateTitle">V-0.5 Beta — Previous Update</h2>
    <p>V-0.5 expanded transformation strategy and rebuilt the Root Gate endgame into a larger multi-stage encounter.</p>
    <ul class="update-details-list">
      <li><strong>Transformation Rules:</strong> The Moonbound and The Ashen Saint gained low-health transformation requirements, with transformed forms lasting up to three Nights.</li>
      <li><strong>Party Combat Switching:</strong> Living party members can rotate into an ongoing fight when the active survivor runs out of Combat AP, while creature health and battle state remain intact.</li>
      <li><strong>Dangerous Retreats:</strong> Switching survivors during combat can trigger a creature attack against the retreating survivor.</li>
      <li><strong>Root Gate Guardians:</strong> Added The Thornbound, The Veinmaw, and The Ash Wraith as three new Legendary guardians protecting the Root.</li>
      <li><strong>The Triune Maw:</strong> Defeating all three guardians triggers a transformation sequence that creates the Abyssal fusion boss before the final Root battle.</li>
      <li><strong>Root Gate Story &amp; Artwork:</strong> Added guardian artwork, the multi-scene fusion cutscene, final fusion artwork, and a transformation preview from the menu.</li>
      <li><strong>Endgame Combat Improvements:</strong> Improved Triune Maw damage/Armor behavior, Rootstorm effects, fusion save recovery, and final boss progression.</li>
      <li><strong>Horror Audio:</strong> Replaced the original bass-heavy test audio with a quieter tonal horror soundtrack and ambience.</li>
    </ul>
    <a class="update-details-back" href="#gameLibrary">← Back to Library</a>
  </div>
</section>'''

for panel_id, replacement in [('updateDetailsPanel', current), ('previousUpdatePanel', previous)]:
    pattern = re.compile(r'<section id="' + panel_id + r'"[^>]*>.*?</section>', re.S)
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f'{panel_id} not found exactly once')

path.write_text(text)
print('V0.6 menu/library release information updated.')
