from pathlib import Path

path = Path('index.html')
text = path.read_text()

def replace(old, new, count=None):
    global text
    found = text.count(old)
    if count is not None and found != count:
        raise SystemExit(f'Expected {count} matches, found {found}: {old[:120]!r}')
    if found == 0:
        raise SystemExit(f'Pattern not found: {old[:120]!r}')
    text = text.replace(old, new)

# Persist transformation for the night it is activated plus the next two nights.
replace(
'''function revertTransformationState(p,announce=false){
  if(!p||!p.transformed)return;
  p.transformed=false;''',
'''function revertTransformationState(p,announce=false){
  if(!p||!p.transformed)return;
  p.transformed=false;
  p.transformedThroughNight=null;''',
1)

# Combat ending should no longer force transformed survivors back to normal.
replace(
'''function resetCombatTransformations(){
  if(!G)return;
  G.ps.forEach(p=>{
    revertTransformationState(p,false);
    p.transformationUsedThisCombat=false;
  });
}''',
'''function resetCombatTransformations(){
  if(!G)return;
  G.ps.forEach(p=>{
    p.transformationUsedThisCombat=false;
  });
}''',
1)

# Set three-night duration at the moment transformation activates.
replace(
'''    p.transformationUsedThisCombat=true;
    p.transformed=true;
    p.name=t.name;''',
'''    p.transformationUsedThisCombat=true;
    p.transformed=true;
    p.transformedThroughNight=G.night+2;
    p.name=t.name;''',
1)

replace(
'''    log(`✨ ${p.originalName} transforms into ${p.name} at critical health!`,"good");''',
'''    log(`✨ ${p.originalName} transforms into ${p.name} at critical health! The transformation can remain active through Night ${p.transformedThroughNight}.`,"good");''',
1)

# Expire transformations after a total of three nights. The activation night counts as Night 1.
replace(
'''  G.night++;

  // Reset every living Survivor for the new Night
  G.ps.forEach(p=>{

    if(p.dead)return;

    p.actions=nightActionCount(p);''',
'''  G.night++;

  // Reset every living Survivor for the new Night
  G.ps.forEach(p=>{

    if(p.dead)return;

    // V0.5: transformations last for three total Nights, including the activation Night.
    if(p.transformed){
      if(!Number.isFinite(p.transformedThroughNight))p.transformedThroughNight=G.night+1;
      if(G.night>p.transformedThroughNight){
        const transformedName=p.name;
        revertTransformationState(p,false);
        log(`🌘 ${transformedName}'s three-Night transformation has expired. ${p.originalName} returns to normal.`,"good");
      }
    }

    p.actions=nightActionCount(p);''',
1)

# Update player-facing guidance where the exact text exists, without making the patch depend on it.
text = text.replace(
'The Moonbound and The Ashen Saint transform only during combat after reaching their health threshold, and each transformation can activate once per encounter.',
'The Moonbound and The Ashen Saint transform only during combat after reaching their health threshold. Once activated, the transformed form can remain active for three total Nights, including the activation Night.'
)
text = text.replace('Transformation active</div>', 'Transformation active · lasts up to 3 Nights</div>')

path.write_text(text)
print('V0.5 three-night transformation duration patch applied.')
