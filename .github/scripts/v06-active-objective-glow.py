from pathlib import Path
import re

p=Path('v06-enhancements.js')
s=p.read_text(encoding='utf-8')

old="function objectiveText(){return (document.getElementById('storyObjectiveText')?.textContent||'').trim()}"
new="""function objectiveText(){return (document.getElementById('storyObjectiveText')?.textContent||'').trim()}
function activeObjectiveText(){
  if(hasGame()&&typeof STORY_OBJECTIVES!=='undefined'&&Array.isArray(STORY_OBJECTIVES)){
    const current=STORY_OBJECTIVES[Number(G.clues||0)];
    if(current?.text)return String(current.text).trim();
  }
  const el=document.getElementById('storyObjectiveText');
  const raw=(el?.innerText||el?.textContent||'').trim();
  const marker=raw.lastIndexOf('➡️');
  return marker>=0?raw.slice(marker+2).trim():raw;
}"""
if old in s:
    s=s.replace(old,new,1)
elif 'function activeObjectiveText()' not in s:
    raise SystemExit('objectiveText function not found')

s=s.replace("  const objective=objectiveText();\n  if(objective)return {text:`Follow the Story Objective: ${objective}`,kind:'story'};",
            "  const objective=activeObjectiveText();\n  if(objective)return {text:`Follow the Story Objective: ${objective}`,kind:'story'};",1)

pattern=r"function highlightObjective\(\)\{.*?\n\}"
replacement="""function highlightObjective(){
  document.querySelectorAll('.loc.v06-objective-target').forEach(el=>el.classList.remove('v06-objective-target'));
  const objective=activeObjectiveText().toLowerCase();
  if(!objective)return;
  let best=null,bestLen=0;
  document.querySelectorAll('.loc').forEach(card=>{
    const txt=(card.textContent||'').trim().toLowerCase();
    if(!txt)return;
    const title=(card.querySelector('b')?.textContent||'').trim().toLowerCase();
    const candidate=title||txt.split('\\n')[0];
    if(candidate.length>3&&objective.includes(candidate)&&candidate.length>bestLen){best=card;bestLen=candidate.length}
  });
  if(best)best.classList.add('v06-objective-target');
}"""
s,n=re.subn(pattern,lambda m:replacement,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('highlightObjective function not found')

if 'const objective=activeObjectiveText().toLowerCase();' not in s:
    raise SystemExit('glow is not using the active objective')
if "STORY_OBJECTIVES[Number(G.clues||0)]" not in s:
    raise SystemExit('active objective is not tied to story progression')

p.write_text(s,encoding='utf-8')
print('Objective glow now follows only the active story objective')
