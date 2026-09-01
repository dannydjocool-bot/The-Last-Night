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

# Replace the old text-matching glow with state-driven location targeting.
pattern=r"function highlightObjective\(\)\{.*?\n\}"
replacement="""function objectiveTargetLocs(){
  if(!hasGame())return [];
  if(typeof STORY_OBJECTIVES!=='undefined'&&Array.isArray(STORY_OBJECTIVES)){
    const clueTarget=STORY_OBJECTIVES[Number(G.clues||0)];
    if(clueTarget?.loc)return [String(clueTarget.loc)];
  }
  if(!G.wardenDefeated||!G.hollowDefeated){
    const out=[];
    if(!G.wardenDefeated)out.push('prison');
    if(!G.hollowDefeated)out.push('hollow');
    return out;
  }
  if(!G.bloodkeeperDefeated||!G.sentinelDefeated){
    const out=[];
    if(!G.bloodkeeperDefeated)out.push('slaughterhouse');
    if(!G.sentinelDefeated)out.push('asylum');
    return out;
  }
  if(!G.rootEntered)return ['root'];
  if(!G.rootGateUnlocked)return ['root'];
  if(!G.rootFusionDefeated)return ['root'];
  if(!G.rootDefeated)return ['root'];
  return ['gate'];
}
function highlightObjective(){
  document.querySelectorAll('.loc.v06-objective-target').forEach(el=>el.classList.remove('v06-objective-target'));
  const targets=objectiveTargetLocs();
  if(!targets.length)return;
  const fallbackNames={station:'Police Station',library:'Town Library',chapel:'The Chapel',huntercamp:"Hunter's Camp",hospital:'Abandoned Hospital',school:'Blackwood School',factory:'Abandoned Factory',massgrave:'Mass Grave',laboratory:'Underground Laboratory',ritual:'Ritual Chamber',prison:'Blackwood Prison',hollow:'The Hollow',slaughterhouse:'Slaughterhouse',asylum:'Asylum',root:'Root of Blackwood',gate:'Escape Gate'};
  for(const loc of targets){
    let expected='';
    try{if(typeof LM!=='undefined'&&LM?.[loc]?.[1])expected=String(LM[loc][1]).trim().toLowerCase()}catch{}
    if(!expected)expected=String(fallbackNames[loc]||loc).trim().toLowerCase();
    let best=null,bestLen=0;
    document.querySelectorAll('.loc').forEach(card=>{
      const txt=(card.textContent||'').trim().toLowerCase();
      const title=(card.querySelector('b')?.textContent||'').trim().toLowerCase();
      const candidate=title||txt.split('\\n')[0];
      const exact=candidate===expected;
      const loose=candidate.includes(expected)||expected.includes(candidate);
      if((exact||loose)&&candidate.length>bestLen){best=card;bestLen=candidate.length}
    });
    if(best)best.classList.add('v06-objective-target');
  }
}"""
s,n=re.subn(pattern,lambda m:replacement,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('highlightObjective function not found')

required=[
  'function objectiveTargetLocs()',
  "if(!G.wardenDefeated)out.push('prison')",
  "if(!G.hollowDefeated)out.push('hollow')",
  "if(!G.bloodkeeperDefeated)out.push('slaughterhouse')",
  "if(!G.sentinelDefeated)out.push('asylum')",
  "if(!G.rootEntered)return ['root']",
  "if(!G.rootDefeated)return ['root']",
  "return ['gate']",
  "const targets=objectiveTargetLocs()"
]
for marker in required:
    if marker not in s:
        raise SystemExit('missing objective glow marker: '+marker)

p.write_text(s,encoding='utf-8')
print('Objective glow now follows story progression through the Escape Gate')
