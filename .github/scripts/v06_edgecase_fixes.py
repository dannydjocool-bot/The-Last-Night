from pathlib import Path

p=Path('v06-enhancements.js')
s=p.read_text()

old="function newNightMod(){if(!hasGame())return;G.v06NightModifier={...pick(MODS)};"
new="function newNightMod(){if(!hasGame()||document.body.classList.contains('menu-mode'))return;G.v06NightModifier={...pick(MODS)};"
assert old in s, 'night modifier guard marker missing'
s=s.replace(old,new,1)

old="function bossIntro(c,id){c.v06Introduced=true;show(`"
assert old in s, 'bossIntro marker missing'
# Replace only the boss button handler tail.
old_tail="document.getElementById('v06FaceBoss').onclick=()=>{close();if(typeof horrorTone==='function'){horrorTone('warning');setTimeout(()=>horrorTone('enemy'),250)}window.__v06StartCombat(String(id))};j(`${c.name} revealed itself.`,'BOSS')}"
new_tail="document.getElementById('v06FaceBoss').onclick=()=>{close();if(typeof horrorTone==='function'){horrorTone('warning');setTimeout(()=>horrorTone('enemy'),250)}window.__v06StartCombat(String(id));const p=hasGame()?G.ps[G.active]:null;if(p&&bestBond(p)>=3&&currentCombat()){p.combatActions=(p.combatActions||0)+1;lg(`🤝 TRUST BONUS: ${p.name} gains +1 Combat Action.`,'good')}};j(`${c.name} revealed itself.`,'BOSS')}"
assert old_tail in s, 'boss intro handler marker missing'
s=s.replace(old_tail,new_tail,1)

old="  if(document.querySelector('.loc.locked'))return '🔒 Some locations are story-locked. Advance the Story Objective to open them.';\n"
new=""
assert old in s, 'generic locked-location warning marker missing'
s=s.replace(old,new,1)

p.write_text(s)

# Validation
out=p.read_text()
assert "document.body.classList.contains('menu-mode')" in out
assert "window.__v06StartCombat(String(id));const p=hasGame()?G.ps[G.active]:null" in out
assert "Some locations are story-locked" not in out
print('V0.6 edge-case fixes validated')
