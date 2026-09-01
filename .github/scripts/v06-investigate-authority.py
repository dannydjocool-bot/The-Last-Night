from pathlib import Path
import re

# Core game: give the visible Investigate button one dedicated handler.
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Search is loot/events only; never story progression.
search_pattern=r"function search\(\)\{.*?\n\}"
m=re.search(search_pattern,s,re.S)
if not m:
    raise SystemExit('search function missing')
search_new='''function search(){

let p=G.ps[G.active];
let r=d6();

log(`${p.name} searches and rolls ${r}.`);

if(r===1){
encounter();
}
else if(r<=3){
log("Nothing useful.");
}
else{
gainItem();
}
}'''
s=s[:m.start()]+search_new+s[m.end():]

# Rename the core story action so no enhancement wrapper can shadow the button target.
s=s.replace('function investigate(){\n  const p=G.ps[G.active];','function performObjectiveInvestigate(){\n  const p=G.ps[G.active];',1)
if 'function performObjectiveInvestigate()' not in s:
    raise SystemExit('core Investigate function rename failed')

# Add compatibility alias for older code/saves/tests, but the UI will not use this alias.
needle='''  render();
  return true;
}
function flashlightSceneFor(loc){'''
replace='''  render();
  window.v06SyncGuidance?.();
  window.v06RefreshObjectiveGlow?.();
  return true;
}
window.performObjectiveInvestigate=performObjectiveInvestigate;
function investigate(){return performObjectiveInvestigate();}
function flashlightSceneFor(loc){'''
if needle in s:
    s=s.replace(needle,replace,1)
elif 'window.performObjectiveInvestigate=performObjectiveInvestigate;' not in s:
    raise SystemExit('could not expose dedicated Investigate handler')

# The rendered button must call the dedicated handler directly.
s,n=re.subn(r'onclick="investigate\(\)"', 'onclick="window.performObjectiveInvestigate()"', s, count=1)
if n!=1 and 'onclick="window.performObjectiveInvestigate()"' not in s:
    raise SystemExit('visible Investigate button was not rewired')

p.write_text(s,encoding='utf-8')

# V0.6 enhancement: Search may be wrapped for atmosphere; Investigate must not be replaced.
p=Path('v06-enhancements.js')
js=p.read_text(encoding='utf-8')

investigate_wrapper=r"if\(typeof investigate==='function'\)\{const o=investigate;window\.investigate=function\(\)\{.*?\n\}\}"
js,n=re.subn(investigate_wrapper,'',js,count=1,flags=re.S)
if n==0 and "window.investigate=function" in js:
    raise SystemExit('could not remove V0.6 Investigate wrapper')

# Expose an explicit glow refresh hook for the core objective action.
if 'window.v06RefreshObjectiveGlow=highlightObjective;' not in js:
    marker='function highlightObjective(){'
    idx=js.find(marker)
    if idx<0:
        raise SystemExit('highlightObjective function missing')
    # expose after the function body using the next known helper marker
    next_marker='function transformationGuidance'
    end=js.find(next_marker,idx)
    if end<0:
        next_marker='function visibleLockReason'
        end=js.find(next_marker,idx)
    if end<0:
        raise SystemExit('could not locate end of highlightObjective section')
    js=js[:end]+'window.v06RefreshObjectiveGlow=highlightObjective;\n'+js[end:]

p.write_text(js,encoding='utf-8')
print('Investigate button now calls dedicated objective progression handler directly')
