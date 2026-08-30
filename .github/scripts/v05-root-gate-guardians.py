from pathlib import Path

path=Path('index.html')
text=path.read_text()

def rep(old,new,count=1,label='pattern'):
    global text
    found=text.count(old)
    if found < count:
        raise SystemExit(f'{label}: expected at least {count}, found {found}')
    text=text.replace(old,new,count)

# ---------- UI / RESPONSIVE SHOWCASE ----------
rep(
'.new-survivor-showcase{margin-bottom:18px;padding:18px;border:1px solid #385664;border-radius:16px;background:radial-gradient(circle at 50% 0,rgba(63,128,150,.14),transparent 55%),#0d0f11}',
'.new-survivor-showcase{margin-bottom:18px;padding:18px;border:1px solid #385664;border-radius:16px;background:radial-gradient(circle at 50% 0,rgba(63,128,150,.14),transparent 55%),#0d0f11}.new-gate-showcase{margin-bottom:18px;padding:18px;border:1px solid #704047;border-radius:16px;background:radial-gradient(circle at 50% 0,rgba(157,38,49,.18),transparent 55%),#0d0f11;min-width:0}.new-gate-showcase h2{margin:0 0 5px;text-align:center;font-family:Georgia,serif;letter-spacing:2px}.new-gate-showcase>p{text-align:center;color:#b8adb0;font-size:11px}.gate-guardian-stage{display:grid;grid-template-columns:44px minmax(0,1fr) 44px;gap:10px;align-items:center}.gate-guardian-nav{width:44px;height:54px;padding:0;margin:0;border-color:#704047;background:#171113;font-size:22px}.gate-guardian-card{position:relative;display:grid;grid-template-columns:minmax(135px,42%) 1fr;gap:14px;overflow:hidden;border:1px solid #824b54;border-radius:13px;background:#101113;padding:0;text-align:left;min-height:225px}.gate-guardian-card img{width:100%;height:225px;object-fit:cover}.gate-guardian-info{padding:17px 15px 14px 0;align-self:center}.gate-guardian-info b{display:block;font-family:Georgia,serif;font-size:22px;margin:4px 0 7px}.gate-guardian-info small{display:block;color:#e1b1b6;line-height:1.45}.gate-guardian-info p{font-size:12px;line-height:1.5;color:#c6c9cc;margin:10px 0 0}.gate-guardian-dots{display:flex;justify-content:center;gap:7px;margin-top:10px}.gate-guardian-dot{width:8px;height:8px;border-radius:50%;background:#484b50;border:0;padding:0;margin:0}.gate-guardian-dot.active{background:#e36b75;box-shadow:0 0 10px rgba(227,107,117,.7)}',
1,'showcase CSS')

rep(
'  .recruit-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.flashlight-choices{grid-template-columns:1fr}.recruit-detail{grid-template-columns:1fr}.map{grid-template-columns:repeat(2,minmax(120px,1fr))}',
'  .recruit-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.flashlight-choices{grid-template-columns:1fr}.recruit-detail{grid-template-columns:1fr}.map{grid-template-columns:repeat(2,minmax(120px,1fr))}.gate-guardian-card{grid-template-columns:1fr;min-height:0}.gate-guardian-card img{height:auto;aspect-ratio:16/10;object-position:center 28%}.gate-guardian-info{padding:12px 14px 15px}.gate-guardian-info b{font-size:19px}',
1,'tablet guardian CSS')

rep(
'@media(max-width:600px){\n  #logButton{',
'@media(max-width:600px){\n  .new-gate-showcase{padding:13px}.gate-guardian-stage{grid-template-columns:34px minmax(0,1fr) 34px;gap:6px}.gate-guardian-nav{width:34px;height:48px;font-size:18px}.gate-guardian-card img{aspect-ratio:4/3}.gate-guardian-info{padding:11px 12px 13px}.gate-guardian-info b{font-size:17px}.gate-guardian-info p{font-size:11px}\n  #logButton{',
1,'phone guardian CSS')

rep(
'    <section id="newSurvivorShowcase" class="new-survivor-showcase" aria-label="Seven new recruit-only survivors"></section>\n    <section id="menuArtStrip"',
'    <section id="newSurvivorShowcase" class="new-survivor-showcase" aria-label="Seven new recruit-only survivors"></section>\n    <section id="newGateGuardianShowcase" class="new-gate-showcase" aria-label="Three new Root Gate guardian creatures"></section>\n    <section id="menuArtStrip"',
1,'showcase HTML')

rep(
'  renderNewGoatShowcase();\n  renderNewSurvivorShowcase();',
'  renderNewGoatShowcase();\n  renderNewSurvivorShowcase();\n  renderRootGateGuardianShowcase();',
1,'showcase render hook')

# ---------- CREATURE DEFINITIONS ----------
root_obj='''  {\n  name:"The Root of Blackwood",\nhp:55,\natk:11,\n  rarity:"Abyssal",'''
guardians='''{\nname:"The Thornbound",\nhp:34,\natk:7,\nrarity:"Legendary",\nweight:0,\nimage:"bonecollector.png",\nability:"Barkbound Bulwark — The first successful strike against it each combat deals 50% less damage.",\nbossZone:"root",gateGuardian:true,isNew:true,gateOrder:1,\nlore:"A corpse-shaped wall of black roots, grown across the entrance so nothing reaches the heart beneath Blackwood."\n},\n{\nname:"The Veinmaw",\nhp:30,\natk:8,\nrarity:"Legendary",\nweight:0,\nimage:"wendigo.png",\nability:"Crimson Hunger — Below 50% HP its attacks gain +3 damage, with a chance to feed and restore 2 HP.",\nbossZone:"root",gateGuardian:true,isNew:true,gateOrder:2,\nlore:"A starving root-beast fed by the same red veins that pulse through the final chamber."\n},\n{\nname:"The Ash Wraith",\nhp:27,\natk:8,\nrarity:"Legendary",\nweight:0,\nimage:"palebride.png",\nability:"Ashen Whisper — Its attacks have a 35% chance to drain 2 Sanity from the survivor it strikes.",\nbossZone:"root",gateGuardian:true,isNew:true,gateOrder:3,\nlore:"The last voice at the threshold: a drifting spirit made from ash, memory, and the names Blackwood refuses to forget."\n},\n  {\n  name:"The Root of Blackwood",\nhp:55,\natk:11,\n  rarity:"Abyssal",'''
rep(root_obj,guardians,1,'guardian definitions')

# ---------- SHOWCASE FUNCTIONS ----------
anchor='''function openRecruitDetail(index){\n  const s=S.filter(x=>x.recruitOnly)[index];'''
insert='''let rootGuardianShowcaseIndex=0;\nfunction rootGateGuardians(){return CRE.filter(c=>c.gateGuardian).sort((a,b)=>(a.gateOrder||0)-(b.gateOrder||0));}\nfunction renderRootGateGuardianShowcase(){\n  const showcase=document.getElementById("newGateGuardianShowcase");\n  if(!showcase)return;\n  const guardians=rootGateGuardians();\n  if(!guardians.length){showcase.innerHTML="";return;}\n  rootGuardianShowcaseIndex=(rootGuardianShowcaseIndex+guardians.length)%guardians.length;\n  const c=guardians[rootGuardianShowcaseIndex];\n  showcase.innerHTML=`<h2>NEW ROOT GATE GUARDIANS</h2><p>Three creatures seal the entrance to the final chamber. Defeat all three before The Root of Blackwood can awaken.</p><div class="gate-guardian-stage"><button class="gate-guardian-nav" onclick="nextRootGateGuardian(-1)" aria-label="Previous Root Gate guardian">‹</button><button class="gate-guardian-card" onclick="openRootGuardianDetail(${rootGuardianShowcaseIndex})"><img src="${c.image}" alt="${c.name}"><span class="new-badge">NEW</span><span class="gate-guardian-info"><small>ROOT GATE GUARDIAN ${c.gateOrder}/3 · ${c.rarity}</small><b>${c.name}</b><small>❤️ ${c.hp} · ⚔️ ${c.atk}</small><p>${c.ability}</p></span></button><button class="gate-guardian-nav" onclick="nextRootGateGuardian(1)" aria-label="Next Root Gate guardian">›</button></div><div class="gate-guardian-dots">${guardians.map((_,i)=>`<button class="gate-guardian-dot ${i===rootGuardianShowcaseIndex?'active':''}" onclick="showRootGateGuardian(${i})" aria-label="Show guardian ${i+1}"></button>`).join("")}</div>`;\n}\nfunction nextRootGateGuardian(direction){rootGuardianShowcaseIndex+=direction;renderRootGateGuardianShowcase();}\nfunction showRootGateGuardian(index){rootGuardianShowcaseIndex=index;renderRootGateGuardianShowcase();}\nfunction openRootGuardianDetail(index){\n  const c=rootGateGuardians()[index];if(!c)return;\n  document.getElementById("menuDialogTitle").textContent=c.name;\n  document.getElementById("menuDialogContent").innerHTML=`<div class="recruit-detail"><img src="${c.image}" alt="${c.name}"><div><span class="recruit-only-badge">NEW · ROOT GATE GUARDIAN</span><h2>${c.name}</h2><div class="codex-stats"><span>${c.rarity}</span><span>❤️ ${c.hp}</span><span>⚔️ ${c.atk}</span></div><p><b>Creature Ability:</b> ${c.ability}</p><p>${c.lore}</p><p class="muted">Story Encounter: Root of Blackwood entrance. All three Gate Guardians must be defeated before the final boss can awaken.</p></div></div>`;\n  document.getElementById("menuOverlay").classList.add("open");document.body.style.overflow="hidden";\n}\n\nfunction openRecruitDetail(index){\n  const s=S.filter(x=>x.recruitOnly)[index];'''
rep(anchor,insert,1,'guardian showcase functions')

# Codex clearly identifies them as NEW Root Gate Guardians.
rep(
'${entry.isNew||entry.isNewRecruit?\'NEW · \':\'\'}${type==="survivors"?(entry.recruitOnly?"FLASHLIGHT RECRUIT ONLY":"AVAILABLE SURVIVOR"):"KNOWN THREAT"}',
'${entry.isNew||entry.isNewRecruit?\'NEW · \':\'\'}${type==="survivors"?(entry.recruitOnly?"FLASHLIGHT RECRUIT ONLY":"AVAILABLE SURVIVOR"):(entry.gateGuardian?"ROOT GATE GUARDIAN":"KNOWN THREAT")}',
1,'codex guardian label')

# ---------- STORY STATE / SAVE MIGRATION ----------
rep(
'  rootEntered:false,\n  rootDefeated:false,',
'  rootEntered:false,\n  rootGateMinionsSpawned:false,\n  rootGateMinionsDefeated:[],\n  rootGateUnlocked:false,\n  rootDefeated:false,',
1,'new game guardian state')

rep(
'  if(!(G.flashlightUsedLocations instanceof Set))G.flashlightUsedLocations=new Set(G.flashlightUsedLocations||[]);\n  G.extraPocketMax=30;',
'  if(!(G.flashlightUsedLocations instanceof Set))G.flashlightUsedLocations=new Set(G.flashlightUsedLocations||[]);\n  if(!Array.isArray(G.rootGateMinionsDefeated))G.rootGateMinionsDefeated=[];\n  G.rootGateMinionsSpawned=Boolean(G.rootGateMinionsSpawned||G.rootGateMinionsDefeated.length);\n  G.rootGateUnlocked=Boolean(G.rootGateUnlocked||G.rootGateMinionsDefeated.length>=3||G.rootDefeated);\n  G.extraPocketMax=30;',
1,'save migration guardian state')

# ---------- STORY OBJECTIVE ----------
rep(
'''  }else if(!G.rootDefeated){\n    objectiveText.innerHTML=`✅ Objective 13 — Entered the Root of Blackwood<br>➡️ Objective 14 — Destroy the Root of Blackwood`;\n  }else{\n    objectiveText.innerHTML=`✅ Objective 14 — Root destroyed<br>➡️ FINAL OBJECTIVE — Reach the Escape Gate`;\n  }''',
'''  }else if(!G.rootGateUnlocked){\n    const defeated=(G.rootGateMinionsDefeated||[]).length;\n    objectiveText.innerHTML=`✅ Objective 13 — Entered the Root of Blackwood<br>➡️ Objective 14 — Break the Root Gate (${defeated}/3 Guardians defeated)<br>${["The Thornbound","The Veinmaw","The Ash Wraith"].map(name=>(G.rootGateMinionsDefeated||[]).includes(name)?"✅":"⬜")+" "+name).join("<br>")}`;\n  }else if(!G.rootDefeated){\n    objectiveText.innerHTML=`✅ Objective 14 — Root Gate broken<br>➡️ Objective 15 — Destroy the Root of Blackwood`;\n  }else{\n    objectiveText.innerHTML=`✅ Objective 15 — Root destroyed<br>➡️ FINAL OBJECTIVE — Reach the Escape Gate`;\n  }''',
1,'story objective guardian phase')

rep(
'objectiveProgress.textContent=`Clues ${G.clues}/10 · Bosses ${[G.wardenDefeated,G.hollowDefeated,G.bloodkeeperDefeated,G.sentinelDefeated,G.rootDefeated].filter(Boolean).length}/5 · Relics ${relicCount}/3 · Night ${G.night} · No night limit`;',
'objectiveProgress.textContent=`Clues ${G.clues}/10 · Bosses ${[G.wardenDefeated,G.hollowDefeated,G.bloodkeeperDefeated,G.sentinelDefeated,G.rootDefeated].filter(Boolean).length}/5 · Gate Guardians ${(G.rootGateMinionsDefeated||[]).length}/3 · Relics ${relicCount}/3 · Night ${G.night} · No night limit`;',
1,'story progress guardian count')

# ---------- ROOT GATE SPAWNING ----------
spawn_anchor='''function spawnStoryBoss(loc){\n  if(G.clues<10)return false;'''
spawn_funcs='''const ROOT_GATE_GUARDIAN_NAMES=["The Thornbound","The Veinmaw","The Ash Wraith"];\nfunction allRootRelicsCollected(){return ["Bloodkeeper Relic","Sentinel Relic","Warden-Hollow Relic"].every(item=>G.storyItems.includes(item));}\nfunction spawnRootGateGuardians(loc){\n  if(loc!=="root"||G.rootDefeated||G.rootGateUnlocked||!allRootRelicsCollected())return false;\n  if(!Array.isArray(G.rootGateMinionsDefeated))G.rootGateMinionsDefeated=[];\n  let spawned=0;\n  ROOT_GATE_GUARDIAN_NAMES.forEach((name,index)=>{\n    if(G.rootGateMinionsDefeated.includes(name))return;\n    if(G.creatures.some(c=>c.name===name&&c.hp>0))return;\n    const base=CRE.find(c=>c.name===name);if(!base)return;\n    G.creatures.push({id:Date.now()+Math.random()+index,name:base.name,hp:base.hp,maxHp:base.hp,atk:base.atk,rarity:base.rarity,image:base.image,ability:base.ability,provoked:false,loc:"root",rootGateGuardian:true,gateOrder:base.gateOrder,rootGuardBlockUsed:false});\n    spawned++;\n  });\n  if(spawned){\n    G.rootGateMinionsSpawned=true;\n    log(`🌑 THE ROOT GATE SEALS SHUT. Three guardians stand between the survivors and the heart of Blackwood: The Thornbound, The Veinmaw, and The Ash Wraith.`,"bad");\n    updateStoryObjective();\n  }\n  return spawned>0;\n}\n\nfunction spawnStoryBoss(loc){\n  if(G.clues<10)return false;'''
rep(spawn_anchor,spawn_funcs,1,'root guardian spawn functions')

rep(
'  else if(loc==="root"&&relicsComplete&&!G.rootDefeated)bossName="The Root of Blackwood";',
'  else if(loc==="root"&&relicsComplete&&G.rootGateUnlocked&&!G.rootDefeated)bossName="The Root of Blackwood";',
1,'root boss gate condition')

# Avoid random trash at the final entrance: guardians first, then Root.
rep(
'''const storyBossSpawned=spawnStoryBoss(id);\nif(!storyBossSpawned && encounterChance>0 && Math.random()<encounterChance){\n  spawn(id);\n}''',
'''if(id==="root"){\n  const guardiansSpawned=spawnRootGateGuardians(id);\n  if(!guardiansSpawned && G.rootGateUnlocked)spawnStoryBoss(id);\n}else{\n  const storyBossSpawned=spawnStoryBoss(id);\n  if(!storyBossSpawned && encounterChance>0 && Math.random()<encounterChance)spawn(id);\n}''',
1,'root arrival encounter logic')

# ---------- GUARDIAN COMBAT ABILITIES ----------
rep(
'''// THE ROTTER — 20% chance to reduce incoming damage by 1\nif(combat.name==="The Rotter" && Math.random()<0.20){''',
'''// ROOT GATE — THORNBOUND BARKBOUND BULWARK\nif(combat.name==="The Thornbound" && !combat.rootGuardBlockUsed){\n  const originalDamage=dmg;\n  dmg=Math.max(1,Math.floor(dmg*0.50));\n  combat.rootGuardBlockUsed=true;\n  log(`🌿 BARKBOUND BULWARK! The Thornbound reduces the first strike from ${originalDamage} to ${dmg} damage.`,"bad");\n}\n// THE ROTTER — 20% chance to reduce incoming damage by 1\nif(combat.name==="The Rotter" && Math.random()<0.20){''',
1,'Thornbound ability')

rep(
'''  // ===============================\n// RARE CREATURE ABILITIES\n// ===============================''',
'''  // ===============================\n// ROOT GATE GUARDIAN ABILITIES\n// ===============================\nif(c.name==="The Veinmaw" && c.hp<=c.maxHp*0.50){\n  damage+=3;\n  log(`🩸 CRIMSON HUNGER! The Veinmaw smells the exposed heart of Blackwood and gains +3 damage.`,"bad");\n  if(c.hp>0&&c.hp<c.maxHp&&Math.random()<0.30){const before=c.hp;c.hp=Math.min(c.maxHp,c.hp+2);log(`🩸 The Veinmaw feeds and restores ${c.hp-before} HP.`,"bad");}\n}\nif(c.name==="The Ash Wraith" && Math.random()<0.35){\n  const lost=Math.min(2,p.san);p.san=Math.max(0,p.san-lost);\n  log(`🌫️ ASHEN WHISPER! ${p.name} loses ${lost} Sanity as the Wraith speaks their name.`,"bad");\n}\n\n  // ===============================\n// RARE CREATURE ABILITIES\n// ===============================''',
1,'guardian attack abilities')

# Track guardian kills, unlock gate only after all three, then awaken Root.
rep(
'''log(`${combat.name} is defeated!`,"good");\n    if(combat.name==="The Root of Blackwood"){''',
'''log(`${combat.name} is defeated!`,"good");\nif(combat.rootGateGuardian || ROOT_GATE_GUARDIAN_NAMES.includes(combat.name)){\n  if(!Array.isArray(G.rootGateMinionsDefeated))G.rootGateMinionsDefeated=[];\n  if(!G.rootGateMinionsDefeated.includes(combat.name))G.rootGateMinionsDefeated.push(combat.name);\n  const defeated=G.rootGateMinionsDefeated.length;\n  log(`🗝️ ROOT GATE GUARDIAN FALLEN: ${combat.name}. ${defeated}/3 seals broken.`,"good");\n  if(defeated>=3){\n    G.rootGateUnlocked=true;\n    log(`🌑 THE THREE SEALS BREAK. The entrance tears open and The Root of Blackwood awakens beyond the gate.`,"good");\n    spawnStoryBoss("root");\n  }\n  updateStoryObjective();\n}\n    if(combat.name==="The Root of Blackwood"){''',
1,'guardian defeat progression')

# ---------- GUIDE / PLAYER-FACING COPY ----------
rep(
'<li>Assemble all three relics, destroy the Root, then reach the Escape Gate.</li>',
'<li>Assemble all three relics, enter the Root, defeat the three NEW Root Gate Guardians, destroy the Root, then reach the Escape Gate.</li>',
1,'tips story path')

rep(
"Follow ten investigation objectives, defeat the relic guardians, destroy the Root of Blackwood, and reach the Escape Gate. Runs have no night limit.",
"Follow ten investigation objectives, defeat the relic guardians, break through the three Root Gate Guardians, destroy the Root of Blackwood, and reach the Escape Gate. Runs have no night limit.",
1,'library story copy')

# V0.5 patch notes.
rep(
'<li><strong>Combat Flow Improvements:</strong> Multi-survivor encounters now preserve creature health and battle state while the party rotates fighters, giving larger teams a more tactical role.</li>',
'<li><strong>Root Gate Guardians:</strong> Three NEW creatures now protect the entrance to the final chamber. The Thornbound, The Veinmaw, and The Ash Wraith must all be defeated before The Root of Blackwood can awaken.</li>\n      <li><strong>Combat Flow Improvements:</strong> Multi-survivor encounters now preserve creature health and battle state while the party rotates fighters, giving larger teams a more tactical role.</li>',
1,'V0.5 notes guardian bullet')

path.write_text(text)
print('V0.5 Root Gate guardians patch applied.')
