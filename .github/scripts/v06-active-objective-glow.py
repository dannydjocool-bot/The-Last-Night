from pathlib import Path
import re

p=Path('v06-enhancements.js')
s=p.read_text(encoding='utf-8')

objective_text="function objectiveText(){return (document.getElementById('storyObjectiveText')?.textContent||'').trim()}"
active_fn="""function activeObjectiveText(){
  if(hasGame()&&typeof STORY_OBJECTIVES!=='undefined'&&Array.isArray(STORY_OBJECTIVES)){
    const current=STORY_OBJECTIVES[Number(G.clues||0)];
    if(current?.text)return String(current.text).trim();
  }
  const el=document.getElementById('storyObjectiveText');
  const raw=(el?.innerText||el?.textContent||'').trim();
  const marker=raw.lastIndexOf('➡️');
  return marker>=0?raw.slice(marker+2).trim():raw;
}"""

# Keep exactly one activeObjectiveText helper. Earlier patch reruns could duplicate it.
s=re.sub(r"\nfunction activeObjectiveText\(\)\{.*?\n\}","",s,flags=re.S)
if objective_text not in s:
    raise SystemExit('objectiveText function not found')
s=s.replace(objective_text,objective_text+'\n'+active_fn,1)

s=s.replace("  const objective=objectiveText();\n  if(objective)return {text:`Follow the Story Objective: ${objective}`,kind:'story'};",
            "  const objective=activeObjectiveText();\n  if(objective)return {text:`Follow the Story Objective: ${objective}`,kind:'story'};",1)

# Replace prior target/glow helpers as one state-driven block.
s=re.sub(r"\nfunction objectiveTargetLocs\(\)\{.*?\n\}\nfunction highlightObjective\(\)\{.*?\n\}","",s,flags=re.S)
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
window.v06ObjectiveTargetLocs=objectiveTargetLocs;
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

anchor='function explainLocks(){'
if anchor not in s:
    raise SystemExit('explainLocks anchor not found')
s=s.replace(anchor,replacement+'\n'+anchor,1)

required=[
  'function objectiveTargetLocs()',
  'window.v06ObjectiveTargetLocs=objectiveTargetLocs;',
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
if s.count('function activeObjectiveText()')!=1:
    raise SystemExit('activeObjectiveText must exist exactly once')
if s.count('function objectiveTargetLocs()')!=1:
    raise SystemExit('objectiveTargetLocs must exist exactly once')

p.write_text(s,encoding='utf-8')
print('Objective glow resolver hardened through final escape')
