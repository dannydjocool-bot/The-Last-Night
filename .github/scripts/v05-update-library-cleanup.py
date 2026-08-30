from pathlib import Path

path = Path('index.html')
text = path.read_text()

old = '''<div id="updateInfoOverlay" class="update-info-overlay" role="dialog" aria-modal="true" aria-labelledby="updateInfoTitle" onclick="closeUpdateInfo(event)">
  <section class="update-info-card" onclick="event.stopPropagation()">
    <div class="update-info-kicker">Latest Build</div>
    <h2 id="updateInfoTitle">V-0.4 Beta — New Update</h2>
    <p>This update focuses on improving the overall experience, especially on phones, while keeping the PC layout intact.</p>
    <ul class="update-info-list">
      <li>Improved mobile layout for the Main Pack / Extra Pockets panel.</li>
      <li>Fixed transforming survivor cards so flipped text no longer overlaps.</li>
      <li>Improved Obtainable Items Codex spacing and mobile item image fitting.</li>
      <li>Adjusted main-menu survivor portraits on phones so heads are less likely to be cropped.</li>
      <li>Added the clickable V-0.4 Beta development message.</li>
      <li>Additional mobile polish and readability fixes across menus.</li>
    </ul>
    <button class="update-info-close" type="button" onclick="closeUpdateInfo()">Close</button>
  </section>
</div>'''

new = '''<div id="updateInfoOverlay" class="update-info-overlay" role="dialog" aria-modal="true" aria-labelledby="updateInfoTitle" onclick="closeUpdateInfo(event)">
  <section class="update-info-card" onclick="event.stopPropagation()">
    <div class="update-info-kicker">Latest Build</div>
    <h2 id="updateInfoTitle">V-0.5 Beta — New Update</h2>
    <p>Blackwood grows more dangerous. V-0.5 expands survivor combat strategy, transformation rules, and the atmosphere stalking every night.</p>
    <ul class="update-info-list">
      <li>Low-health transformation requirements for The Moonbound and The Ashen Saint.</li>
      <li>Transformed forms can remain active for up to three Nights.</li>
      <li>Party members can rotate into combat after the active survivor runs out of Combat AP.</li>
      <li>Combat swaps carry a 30% chance for the creature to strike the retreating survivor.</li>
      <li>New quieter horror music and environmental ambience replaces the old bass-heavy test sound.</li>
      <li>Improved multi-survivor combat flow while preserving creature health and battle state.</li>
    </ul>
    <button class="update-info-close" type="button" onclick="closeUpdateInfo()">Close</button>
  </section>
</div>'''

if old not in text:
    raise SystemExit('Legacy V0.4 update modal not found')
text = text.replace(old, new, 1)
path.write_text(text)
print('Legacy update modal cleaned for V0.5.')
