from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# New Update popup: player-facing, immersive, current V0.6 only.
popup_pattern=r'(<h2 id="updateInfoTitle">).*?(</ul>)'
popup_replacement='''<h2 id="updateInfoTitle">V-0.6 Beta — Blackwood Feels Alive</h2>
    <p>Blackwood feels less like a map and more like a place watching you. Nights change the county, locations react, survivors remember what happened, and the investigation now pulls you deeper into the story.</p>
    <ul class="update-info-list">
      <li>Night Modifiers, location-specific horror events, strange anomalies, and Fear/Sanity hallucinations make each night feel different.</li>
      <li>Story locations now guide the investigation more clearly: Investigate to uncover the next clue, while Search is focused on scavenging and risk.</li>
      <li>The Blackwood Journal follows each save separately, recording discoveries, warnings, relationships, and unsettling moments from that run.</li>
      <li>Survivors can build Trust by surviving together, creating stronger bonds and useful party benefits.</li>
      <li>High-rarity creatures arrive with more dramatic reveals, while wounded enemies can become more dangerous as fights drag on.</li>
      <li>A darker cinematic soundtrack, stronger phone audio, and cleaner mobile controls make Blackwood feel more present wherever you play.</li>
    </ul>'''
s,n=re.subn(popup_pattern,lambda m: popup_replacement,s,count=1,flags=re.S)
if n!=1: raise SystemExit('New Update popup block not found')

# Library update details: same player-facing story, no internal QA/bug terminology.
details_pattern=r'(<section id="updateDetailsPanel".*?<h2 id="updateDetailsTitle">).*?(</ul>)'
details_replacement='''<section id="updateDetailsPanel" aria-labelledby="updateDetailsTitle">
  <div class="update-details-card">
    <div class="update-details-kicker">Latest Build</div>
    <h2 id="updateDetailsTitle">V-0.6 Beta — Blackwood Feels Alive</h2>
    <p>Blackwood County now reacts to the night around you. The investigation is easier to follow without losing its mystery, while the world, creatures, survivors, and soundscape become more unpredictable.</p>
    <ul class="update-details-list">
      <li><strong>Blackwood Feels Alive:</strong> Night Modifiers, location-specific disturbances, rare anomalies, and psychological events make familiar places feel different from one night to the next.</li>
      <li><strong>Investigation &amp; Scavenging:</strong> Investigate is now the action that pushes the case forward at the current story location. Search remains your way to hunt for supplies, trigger exploration choices, and take risks for extra rewards.</li>
      <li><strong>Follow the Case:</strong> The current story destination can glow on the map, and the NEXT STEP guidance helps point you toward what matters without revealing the mystery ahead.</li>
      <li><strong>Blackwood Journal &amp; Trust:</strong> Each save keeps its own Journal of discoveries and warnings, while survivors build Trust by enduring Blackwood together.</li>
      <li><strong>Escalating Encounters:</strong> Dangerous creatures can reveal themselves more dramatically and grow more threatening as they are wounded.</li>
      <li><strong>Horror Soundscape:</strong> The soundtrack has been rebuilt around darker music, distant tones, heartbeat-like pressure, and more space between sounds so the county can breathe.</li>
      <li><strong>Better on Phones:</strong> Journal, Game Log, and Main Pack controls are easier to reach, with stronger music presence and cleaner mobile spacing.</li>
    </ul>'''
s,n=re.subn(details_pattern,lambda m: details_replacement,s,count=1,flags=re.S)
if n!=1: raise SystemExit('Update details panel not found')

# Tips: explain the actual player action model clearly.
follow_pattern=r'<article class="guide-card"><h3>Follow the Investigation</h3><ul>.*?</ul></article>'
follow_replacement='''<article class="guide-card"><h3>Follow the Investigation</h3><ul><li>The Story Objective shows the next place the case is pulling you toward.</li><li>When you reach the objective location, use Investigate to uncover the story clue and move the case forward.</li><li>Search does not advance story clues; use it to scavenge for supplies and face exploration risks.</li><li>Story locations may glow when the current objective points there, then shift as the investigation moves on.</li><li>Collect all ten clues in order, defeat the relic guardians, break through the Root Gate, destroy the Root of Blackwood, and reach the Escape Gate.</li></ul></article>'''
s,n=re.subn(follow_pattern,follow_replacement,s,count=1,flags=re.S)
if n!=1: raise SystemExit('Follow the Investigation guide card not found')

# Save descriptions should include the Journal because it is now part of each run.
s=s.replace("Each local slot stores its own party, night, inventory, discoveries, combat state, and story progress in this browser.","Each local slot stores its own party, night, inventory, discoveries, Blackwood Journal, combat state, and story progress in this browser.",1)

# Remove stale V0.5-style phrases from the V0.6 popup/details if they survived.
stale=[
  'Low-health transformation requirements for The Moonbound and The Ashen Saint.',
  'Combat swaps carry a 30% chance for the creature to strike the retreating survivor.',
  'Endgame Reliability:'
]
for text in stale:
    if text in s: raise SystemExit('stale player-facing V0.6 copy remains: '+text)

required=[
  'V-0.6 Beta — Blackwood Feels Alive',
  'Investigate is now the action that pushes the case forward',
  'Search does not advance story clues',
  'Each save keeps its own Journal',
  'stronger music presence'
]
for text in required:
    if text not in s: raise SystemExit('required release copy missing: '+text)

p.write_text(s,encoding='utf-8')
print('V0.6 player-facing update copy refreshed around immersion and current gameplay')
