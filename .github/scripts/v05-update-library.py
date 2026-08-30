from pathlib import Path
import re

path = Path('index.html')
text = path.read_text()

# Main-menu version badge and beta info title.
text = text.replace('>V-0.4 Beta</button>', '>V-0.5 Beta</button>', 1)
text = text.replace('<h2 id="betaInfoTitle">V-0.4 Beta — Early Development</h2>', '<h2 id="betaInfoTitle">V-0.5 Beta — Early Development</h2>', 1)

# Library update badges: current update plus previous update archive.
old_badge = '<div class="library-art" role="img" aria-label="The Root of Blackwood creature artwork"><a class="library-update-badge library-update-link" href="#updateDetailsPanel" aria-label="View V-0.4 Beta update details">New Update</a></div>'
new_badge = '<div class="library-art" role="img" aria-label="The Root of Blackwood creature artwork"><a class="library-update-badge library-update-link" href="#updateDetailsPanel" aria-label="View V-0.5 Beta update details">New Update</a><a class="library-update-badge library-update-link library-previous-update-badge" href="#previousUpdatePanel" aria-label="View V-0.4 Beta previous update details">Previous Update</a></div>'
if old_badge not in text:
    raise SystemExit('Library update badge markup not found')
text = text.replace(old_badge, new_badge, 1)

# Add visual treatment for Previous Update and allow both update panels to use the same overlay behavior.
text = text.replace(
    '.library-update-badge:hover{border-color:#f08a94;background:rgba(141,36,48,.94)}',
    '.library-update-badge:hover{border-color:#f08a94;background:rgba(141,36,48,.94)}.library-previous-update-badge{top:108px;border-color:rgba(176,181,187,.5);background:rgba(25,28,31,.82);color:#d7dade;box-shadow:0 0 18px rgba(0,0,0,.3)}.library-previous-update-badge:hover{border-color:#c7cbd0;background:rgba(43,47,51,.95)}',
    1
)
text = text.replace(
    '#updateDetailsPanel{position:fixed;inset:0;z-index:26000;display:none;place-items:center;padding:20px;background:rgba(0,0,0,.9);backdrop-filter:blur(9px);pointer-events:auto}\n#updateDetailsPanel:target{display:grid}',
    '#updateDetailsPanel,#previousUpdatePanel{position:fixed;inset:0;z-index:26000;display:none;place-items:center;padding:20px;background:rgba(0,0,0,.9);backdrop-filter:blur(9px);pointer-events:auto}\n#updateDetailsPanel:target,#previousUpdatePanel:target{display:grid}',
    1
)
text = text.replace(
    '@media(max-width:600px){.update-details-card{padding:21px}.library-update-badge.library-update-link{right:14px;top:58px;font-size:9px}}',
    '@media(max-width:600px){.update-details-card{padding:21px}.library-update-badge.library-update-link{right:14px;top:58px;font-size:9px}.library-update-badge.library-update-link.library-previous-update-badge{top:98px}}',
    1
)

# Replace the old V0.4 "New Update" panel with the V0.5 current update and a V0.4 archive.
pattern = re.compile(r'<section id="updateDetailsPanel" aria-labelledby="updateDetailsTitle">.*?</section>', re.S)
match = pattern.search(text)
if not match:
    raise SystemExit('Current update details panel not found')

replacement = '''<section id="updateDetailsPanel" aria-labelledby="updateDetailsTitle">
  <div class="update-details-card">
    <div class="update-details-kicker">Latest Build</div>
    <h2 id="updateDetailsTitle">V-0.5 Beta — New Update</h2>
    <p>Blackwood grows more dangerous. V-0.5 expands survivor combat strategy, transformation rules, and the atmosphere stalking every night.</p>
    <ul class="update-details-list">
      <li><strong>Transformation Thresholds:</strong> The Moonbound and The Ashen Saint can no longer transform freely. Their transformed forms now unlock only after reaching their low-health combat requirements.</li>
      <li><strong>Three-Night Transformations:</strong> Once a transformation is activated, that survivor can remain in the transformed form for up to three Nights before automatically returning to normal.</li>
      <li><strong>Party Combat Switching:</strong> When the active survivor runs out of Combat AP, another living party member with Combat AP can step in and continue the same fight.</li>
      <li><strong>Dangerous Retreats:</strong> Combat swaps carry a 30% chance for the creature to strike the survivor attempting to fall back, making every switch a risk.</li>
      <li><strong>Horror Audio Overhaul:</strong> The old bass-heavy test sound has been replaced with quieter atmospheric horror music, eerie tones, wind, and environmental ambience designed to sit beneath gameplay.</li>
      <li><strong>Combat Flow Improvements:</strong> Multi-survivor encounters now preserve creature health and battle state while the party rotates fighters, giving larger teams a more tactical role.</li>
    </ul>
    <a class="update-details-back" href="#gameLibrary">← Back to Library</a>
  </div>
</section>

<section id="previousUpdatePanel" aria-labelledby="previousUpdateTitle">
  <div class="update-details-card">
    <div class="update-details-kicker">Previous Build</div>
    <h2 id="previousUpdateTitle">V-0.4 Beta — Previous Update</h2>
    <p>V-0.4 expanded the survivor roster, protected save progress, and improved mobile presentation throughout Blackwood.</p>
    <ul class="update-details-list">
      <li><strong>2 New G.O.A.T Survivors:</strong> Two powerful new G.O.A.T survivors can transform during a run, giving each form its own dramatic identity and combat presence.</li>
      <li><strong>7 Flashlight-Exclusive Survivors:</strong> Seven new survivors can only be discovered through flashlight exploration events, rewarding players who take the risk to search deeper.</li>
      <li><strong>Save Progress Protection:</strong> Existing save progress is preserved across future game updates, with automatic compatibility recovery and a backup copy for each save slot.</li>
      <li><strong>Item Images:</strong> Fixed Obtainable Items artwork overlapping or appearing heavily cropped on phones.</li>
      <li><strong>Transforming Survivor Cards:</strong> Fixed inverted card text stacking and overlapping.</li>
      <li><strong>Main Pack / Extra Pockets:</strong> Improved the phone layout so it no longer crowds the top of the game.</li>
      <li><strong>Main-Menu Portraits:</strong> Improved mobile framing so survivor heads are less likely to be cropped.</li>
      <li><strong>Mobile Polish:</strong> Additional spacing, readability, and presentation improvements.</li>
    </ul>
    <a class="update-details-back" href="#gameLibrary">← Back to Library</a>
  </div>
</section>'''

text = text[:match.start()] + replacement + text[match.end():]

path.write_text(text)
print('V0.5 library/version update patch applied.')
