from pathlib import Path

# Core game: give the visible Investigate button one dedicated handler.
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old_search='''function search(){

let p=G.ps[G.active];
let r=d6();

log(`${p.name} searches and rolls ${r}.`);

if(r===1){
encounter();
}
else if(r<=3){
log("Nothing useful.");
}
else if(r===4){
gainItem();
}
else if(r===5){
gainClue();
}
else{
gainItem();
gainClue();
}
}'''
new_search='''function search(){

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
if old_search in s:
    s=s.replace(old_search,new_search,1)
elif new_search not in s:
    raise SystemExit('Search source did not match expected code')

old_head='''function investigate(){
  const p=G.ps[G.active];'''
new_head='''function performObjectiveInvestigate(){
  const p=G.ps[G.active];'''
if old_head in s:
    s=s.replace(old_head,new_head,1)
elif new_head not in s:
    raise SystemExit('Investigate source did not match expected code')

# Correct the player-facing objective transition. G.clues is the completed objective count,
# so the newly active objective is G.clues + 1.
s=s.replace('log(`📍 Objective advanced: ${before+1} → ${G.clues}.`,"good");','log(`📍 Objective advanced: ${before+1} → ${G.clues+1}.`,"good");')

old_tail='''  updateStoryObjective();
  log(`📍 Objective advanced: ${before+1} → ${G.clues+1}.`,"good");
  render();
  return true;
}
function flashlightSceneFor(loc){'''
new_tail='''  updateStoryObjective();
  log(`📍 Objective advanced: ${before+1} → ${G.clues+1}.`,"good");
  render();
  window.v06SyncGuidance?.();
  window.v06RefreshObjectiveGlow?.();
  return true;
}
window.performObjectiveInvestigate=performObjectiveInvestigate;
function investigate(){return performObjectiveInvestigate();}
function flashlightSceneFor(loc){'''
if old_tail in s:
    s=s.replace(old_tail,new_tail,1)
elif 'window.performObjectiveInvestigate=performObjectiveInvestigate;' not in s:
    raise SystemExit('Could not expose dedicated Investigate handler')

old_button='onclick="investigate()"'
new_button='onclick="window.performObjectiveInvestigate()"'
if old_button in s:
    s=s.replace(old_button,new_button,1)
elif new_button not in s:
    raise SystemExit('Visible Investigate button was not found')

if 'Objective advanced: ${before+1} → ${G.clues}.' in s:
    raise SystemExit('Old objective feedback is still present')
if 'Objective advanced: ${before+1} → ${G.clues+1}.' not in s:
    raise SystemExit('Corrected objective feedback is missing')

p.write_text(s,encoding='utf-8')

# V0.6: Search keeps atmosphere wrapper, Investigate must not be shadowed.
p=Path('v06-enhancements.js')
js=p.read_text(encoding='utf-8')
old_wrapper='''if(typeof investigate==='function'){const o=investigate;window.investigate=function(){
  const p0=hasGame()?G.ps[G.active]:null,obj0=objectiveText().trim().toLowerCase(),loc0=p0?.loc,clues0=Number(G?.clues||0);
  const r=o.apply(this,arguments);
  if(hasGame()&&Number(G?.clues||0)>clues0&&G.ps[G.active]?.loc===loc0){G.v06ClearedObjectiveTarget=null;window.v06SyncGuidance?.();highlightObjective();j(`Objective advanced after investigating ${LM?.[loc0]?.[1]||loc0}.`,'INVESTIGATION')}
  hallucinate();anomaly();return r
}}
'''
if old_wrapper in js:
    js=js.replace(old_wrapper,'',1)
elif 'window.investigate=function' in js:
    raise SystemExit('Unexpected V0.6 Investigate wrapper shape')

# Expose the existing objective glow function without altering its internals.
if 'window.v06RefreshObjectiveGlow=highlightObjective;' not in js:
    marker='function transformationGuidance'
    pos=js.find(marker)
    if pos<0:
        marker='function visibleLockReason'
        pos=js.find(marker)
    if pos<0:
        raise SystemExit('Could not locate guidance section after highlightObjective')
    js=js[:pos]+'window.v06RefreshObjectiveGlow=highlightObjective;\n'+js[pos:]

p.write_text(js,encoding='utf-8')
print('Investigate button now calls the core objective handler directly with correct objective feedback')
