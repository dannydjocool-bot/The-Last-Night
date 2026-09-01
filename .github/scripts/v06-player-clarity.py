from pathlib import Path

p=Path('v06-enhancements.js')
s=p.read_text(encoding='utf-8')

repls={
"if(Math.random()<.55&&typeof gainItem==='function'){gainItem();lg(`🎒 ${p.name}'s deeper search uncovers an additional item.`,'good')}":"if(!currentCombat()&&Math.random()<.55&&typeof gainItem==='function'){gainItem();lg(`🎒 ${p.name}'s deeper search uncovers an additional item.`,'good')}",
"if(Math.random()<.5)lg(`👂 ${p.name} hears movement before it reaches the room.`,'good')":"if(!currentCombat()&&Math.random()<.5)lg(`👂 ${p.name} hears movement before it reaches the room.`,'good')",
"lg(`🌫️ Heavy Fog closes around ${p.name}. +1 Fear.`,'bad')":"lg(`🌫️ Heavy Fog closes around ${p.name}. +1 Fear.`,'bad');G.v06LastEffect='Heavy Fog: +1 Fear';G.v06LastEffectAt=Date.now();window.v06SyncGuidance?.()",
"lg(`🔇 Dead Silence presses against ${p.name}. -1 Sanity.`,'bad');validateMind(p)":"lg(`🔇 Dead Silence presses against ${p.name}. -1 Sanity.`,'bad');G.v06LastEffect='Dead Silence: -1 Sanity';G.v06LastEffectAt=Date.now();window.v06SyncGuidance?.();validateMind(p)",
"lg('⛈️ The Blackwood Storm steals 1 extra Night AP.','bad')":"lg('⛈️ The Blackwood Storm steals 1 extra Night AP.','bad');G.v06LastEffect='Blackwood Storm: -1 Night AP';G.v06LastEffectAt=Date.now();window.v06SyncGuidance?.()",
"lg(`☠️ Restless Dead follow the party into ${LM[p.loc][1]}.`,'bad')":"lg(`☠️ Restless Dead follow the party into ${LM[p.loc][1]}.`,'bad');G.v06LastEffect='Restless Dead: another creature was attracted';G.v06LastEffectAt=Date.now();window.v06SyncGuidance?.()",
"const body='<div class=\"v06-help-grid\"><div><b>Night AP</b><span>Used for travel, investigation, resting, and exploration.</span></div><div><b>Combat AP</b><span>Used only during fights. It is separate from Night AP.</span></div><div><b>Fear & Sanity</b><span>High Fear and low Sanity make the night more dangerous.</span></div><div><b>Story Objective</b><span>Follow the objective and the glowing map target when one is available.</span></div><div><b>Transformations</b><span>Transforming survivors unlock their form only at low health during combat.</span></div><div><b>Blocked?</b><span>If a creature is alive at your location, defeat it before traveling or ending the Night.</span></div></div>';":"const body='<div class=\"v06-help-grid\"><div><b>Night AP</b><span>Used for travel, investigation, resting, and exploration.</span></div><div><b>Combat AP</b><span>Used only during fights. It is separate from Night AP.</span></div><div><b>Fear & Sanity</b><span>High Fear and low Sanity make the night more dangerous.</span></div><div><b>Story Objective</b><span>Follow the objective and the glowing map target when one is available.</span></div><div><b>Transformations</b><span>Transforming survivors unlock their form only at low health during combat.</span></div><div><b>Blocked?</b><span>If a creature is alive at your location, defeat it before traveling or ending the Night.</span></div></div><button type=\"button\" class=\"v06-show-tips\" onclick=\"v06ResetTips()\">Show Tips Again</button>';",
"if(G.v06NightModifier)meta.push(`${G.v06NightModifier.icon||'🌙'} ${G.v06NightModifier.name}`);":"if(G.v06NightModifier)meta.push(`${G.v06NightModifier.icon||'🌙'} ${G.v06NightModifier.name}`);\n  const trust=trustStatus(p);if(trust)meta.push(trust);\n  const root=rootProgress();if(root)meta.push(root);\n  if(G.v06LastEffect&&Date.now()-Number(G.v06LastEffectAt||0)<10000)meta.push(`⚠️ ${G.v06LastEffect}`);",
"ensureGuidanceUi();\nsetInterval(syncGuidance,700);":"window.v06SyncGuidance=syncGuidance;\nwindow.v06ResetTips=()=>{localStorage.removeItem(TIP_KEY);const c=document.getElementById('v06Coach');if(c)c.hidden=true;if(typeof v06CloseOverlay==='function')v06CloseOverlay();syncGuidance();};\nensureGuidanceUi();\nsetInterval(syncGuidance,700);"
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit(f'missing expected snippet: {old[:90]}')
    s=s.replace(old,new,1)

anchor="function coach(key,title,text){"
insert="""function trustStatus(p){
  if(!p||!hasGame())return '';
  const names=[p.originalName||p.name,p.name].filter(Boolean),b=G.v06Bonds||{};let best=0;
  for(const [key,val] of Object.entries(b)){if(names.some(n=>key.split('::').includes(n)))best=Math.max(best,Number(val)||0)}
  return `🤝 Trust: ${Math.min(3,best)}/3`;
}
function rootProgress(){
  if(!hasGame())return '';
  const obj=objectiveText().toLowerCase(),n=Math.min(3,Array.isArray(G.rootGateMinionsDefeated)?G.rootGateMinionsDefeated.length:0);
  const relevant=n>0||G.rootFusionTriggered||G.rootFusionPending||G.rootFusionDefeated||G.rootGateUnlocked||obj.includes('root')||obj.includes('guardian')||obj.includes('triune');
  if(!relevant)return '';
  const triune=G.rootFusionDefeated?'✅':(G.rootFusionTriggered||G.rootFusionPending||n>=3?'⚔️':'🔒');
  const root=G.rootGateUnlocked?'⚔️':'🔒';
  return `🗝️ Guardians ${n}/3 · Triune ${triune} · Root ${root}`;
}
function resetNewRunTips(){
  if(!hasGame()||Number(G.night||1)!==1||G.v06GuidanceRunStarted)return;
  G.v06GuidanceRunStarted=true;
  const seen=getSeen();['start','ap','modifier','transform'].forEach(k=>seen.delete(k));localStorage.setItem(TIP_KEY,JSON.stringify([...seen]));
}
"""
if anchor not in s: raise SystemExit('coach anchor missing')
s=s.replace(anchor,insert+anchor,1)

old="  ensureGuidanceUi();syncDock();\n  const box=document.getElementById('v06Guidance');"
new="  ensureGuidanceUi();syncDock();resetNewRunTips();\n  const box=document.getElementById('v06Guidance');"
if old not in s: raise SystemExit('sync guidance anchor missing')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('patched v06-enhancements.js')
