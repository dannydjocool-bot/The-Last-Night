from pathlib import Path
import re

p=Path('index.html')
t=p.read_text()

def add_once(anchor, addition, label, before=False):
    global t
    if addition.strip() in t:
        return
    if anchor not in t:
        raise SystemExit(f'{label}: anchor not found')
    t=t.replace(anchor, (addition+anchor) if before else (anchor+addition), 1)

# Ensure fusion CSS exists and use the final cutscene assets.
if '.root-fusion-overlay{' not in t:
    css='.root-fusion-overlay{position:fixed;inset:0;z-index:19000;display:none;align-items:center;justify-content:center;padding:18px;background:rgba(0,0,0,.94);backdrop-filter:blur(10px)}.root-fusion-overlay.open{display:flex}.root-fusion-dialog{width:min(900px,96vw);max-height:94vh;overflow:auto;border:1px solid #7b2832;border-radius:18px;background:radial-gradient(circle at 50% 0,rgba(166,29,43,.22),transparent 38%),#08090a;box-shadow:0 25px 90px #000;padding:18px}.root-fusion-kicker{text-align:center;color:#ef6d79;font-size:10px;font-weight:900;letter-spacing:3px}.root-fusion-title{text-align:center;font-family:Georgia,serif;font-size:clamp(24px,5vw,40px);letter-spacing:2px;margin:8px 0}.root-fusion-scene{position:relative;min-height:430px;border:1px solid #573038;border-radius:14px;overflow:hidden;background:#060708}.root-fusion-scene:after{content:"";position:absolute;inset:45% 0 0;background:linear-gradient(transparent,rgba(0,0,0,.88))}.root-fusion-art{position:absolute;inset:0;background-size:cover;background-position:center}.root-fusion-copy{position:absolute;z-index:2;left:18px;right:18px;bottom:16px;padding:14px;border-left:3px solid #e65260;background:rgba(6,7,8,.78);font-weight:800;line-height:1.5}.root-fusion-actions{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:12px}.root-fusion-progress{font-size:11px;color:#aaa}.root-fusion-next{margin:0;background:linear-gradient(#942f3b,#651923);border-color:#c9525e;font-weight:900}'
    add_once('</style>', css, 'fusion css', before=True)

# Replace any temporary art references with final image names.
for cls, img in [('panel1','root-fusion-1.webp'),('panel2','root-fusion-2.webp'),('panel3','root-fusion-3.webp'),('panel4','root-fusion-4.webp')]:
    pat=rf'\.root-fusion-art\.{cls}\{{[^}}]*\}}'
    rule=f'.root-fusion-art.{cls}{{background-image:linear-gradient(0deg,rgba(0,0,0,.10),rgba(0,0,0,.10)),url("{img}");background-size:cover;background-position:center}}'
    if re.search(pat,t):
        t=re.sub(pat,rule,t,count=1)
    else:
        add_once('</style>', rule, f'{cls} css', before=True)

mobile='.root-fusion-overlay{padding:8px}.root-fusion-dialog{padding:10px;border-radius:12px}.root-fusion-scene{min-height:58vh}.root-fusion-copy{left:10px;right:10px;bottom:10px;font-size:12px;padding:10px}.root-fusion-actions{position:sticky;bottom:0;background:#08090a;padding-top:8px}.root-fusion-next{min-height:44px}'
if mobile not in t:
    if '@media(max-width:600px){' in t:
        t=t.replace('@media(max-width:600px){','@media(max-width:600px){\n  '+mobile,1)
    else:
        add_once('</style>', '@media(max-width:600px){'+mobile+'}', 'mobile fusion css', before=True)

# Overlay UI.
if 'id="rootFusionOverlay"' not in t:
    overlay='<div id="rootFusionOverlay" class="root-fusion-overlay" aria-hidden="true"><div class="root-fusion-dialog"><div class="root-fusion-kicker">BLACKWOOD ROOT GATE INCIDENT</div><h2 id="rootFusionTitle" class="root-fusion-title">THE THREE BECOME ONE</h2><div class="root-fusion-scene"><div id="rootFusionArt" class="root-fusion-art panel1"></div><div id="rootFusionCopy" class="root-fusion-copy"></div></div><div class="root-fusion-actions"><span id="rootFusionProgress" class="root-fusion-progress"></span><button id="rootFusionNext" class="root-fusion-next" onclick="nextRootFusionScene()">NEXT →</button></div></div></div>\n'
    if '<button id="logButton"' not in t: raise SystemExit('fusion html: log button anchor missing')
    t=t.replace('<button id="logButton"',overlay+'<button id="logButton"',1)

# Unique guardian artwork.
for name,img in [('The Thornbound','thornbound.webp'),('The Veinmaw','veinmaw.webp'),('The Ash Wraith','ashwraith.webp')]:
    pat=rf'(name:"{re.escape(name)}"[\s\S]*?image:")[^"]+("[\s\S]*?gateOrder:)'
    if re.search(pat,t):
        t=re.sub(pat,rf'\1{img}\2',t,count=1)

# Add fused boss definition.
if 'name:"The Triune Maw"' not in t:
    needle='  {\n  name:"The Root of Blackwood",\nhp:55,'
    if needle not in t: raise SystemExit('fused definition: root boss anchor missing')
    fused='{\nname:"The Triune Maw",\nhp:120,\natk:14,\nrarity:"Abyssal",\nweight:0,\nimage:"root-fusion-4.webp",\nability:"Triune Berserk — 80 Armor. Every third strike erupts for +6 damage and drains 2 Sanity. Below 50% HP, gains +3 ATK. Rootstorm has a 25% chance to entangle the active survivor, costing 1 extra Combat AP on their next action.",\nbossZone:"root",rootFusionBoss:true,isNew:true,\nlore:"Thorn, blood, and ash fused into one impossible gate-beast. The three guardian seals now beat as a single heart."\n},\n  {\n  name:"The Root of Blackwood",\nhp:55,'
    t=t.replace(needle,fused,1)
else:
    t=t.replace('image:"rootofblackwood.png",\nability:"Triune Berserk','image:"root-fusion-4.webp",\nability:"Triune Berserk',1)

# State fields + save migration.
if 'rootFusionTriggered:false' not in t:
    t=t.replace('  rootGateUnlocked:false,\n  rootDefeated:false,','  rootGateUnlocked:false,\n  rootFusionTriggered:false,\n  rootFusionDefeated:false,\n  rootDefeated:false,',1)
if 'G.rootFusionTriggered=Boolean' not in t:
    old='G.rootGateUnlocked=Boolean(G.rootGateUnlocked||G.rootGateMinionsDefeated.length>=3||G.rootDefeated);'
    new='G.rootGateUnlocked=Boolean(G.rootGateUnlocked||G.rootFusionDefeated||G.rootDefeated);\n  G.rootFusionTriggered=Boolean(G.rootFusionTriggered||G.rootFusionDefeated);\n  G.rootFusionDefeated=Boolean(G.rootFusionDefeated);'
    if old in t: t=t.replace(old,new,1)

# Cutscene/fusion helpers.
if 'const ROOT_FUSION_SCENES=' not in t:
    anchor='function spawnStoryBoss(loc){\n  if(G.clues<10)return false;'
    if anchor not in t: raise SystemExit('fusion helpers: spawnStoryBoss anchor missing')
    helpers='''let rootFusionSceneIndex=0;\nconst ROOT_FUSION_SCENES=[\n {title:"THE LAST SEAL SHUDDERS",copy:"All three Gate Guardians fall. The Veinmaw refuses to fade as the ruined entrance begins to pulse."},\n {title:"ROOT-KEY RESONANCE",copy:"Thornbound and Ash Wraith dissolve into root-key energy. Their remaining power spirals toward the red guardian."},\n {title:"TWO LOCKS OPEN",copy:"A keyhole ignites in its chest and another burns behind its neck. Bark armor, crimson veins, and ash fuse into one body."},\n {title:"THE TRIUNE MAW",copy:"The fusion completes. A colossal armored gate-beast rises with impossible strength. The Root remains sealed behind it."}\n];\nfunction showRootFusionCutscene(){\n rootFusionSceneIndex=0;G.rootFusionTriggered=true;combat=null;\n const ov=document.getElementById("rootFusionOverlay");if(!ov)return spawnTriuneMaw();\n ov.classList.add("open");ov.setAttribute("aria-hidden","false");document.body.style.overflow="hidden";renderRootFusionScene();\n}\nfunction renderRootFusionScene(){\n const s=ROOT_FUSION_SCENES[rootFusionSceneIndex];\n document.getElementById("rootFusionTitle").textContent=s.title;\n document.getElementById("rootFusionCopy").textContent=s.copy;\n document.getElementById("rootFusionArt").className="root-fusion-art panel"+(rootFusionSceneIndex+1);\n document.getElementById("rootFusionProgress").textContent=`SCENE ${rootFusionSceneIndex+1} / ${ROOT_FUSION_SCENES.length}`;\n document.getElementById("rootFusionNext").textContent=rootFusionSceneIndex===ROOT_FUSION_SCENES.length-1?"FACE THE TRIUNE MAW →":"NEXT →";\n}\nfunction nextRootFusionScene(){\n if(rootFusionSceneIndex<ROOT_FUSION_SCENES.length-1){rootFusionSceneIndex++;renderRootFusionScene();return;}\n const ov=document.getElementById("rootFusionOverlay");ov.classList.remove("open");ov.setAttribute("aria-hidden","true");document.body.style.overflow="";spawnTriuneMaw();render();\n}\nfunction spawnTriuneMaw(){\n if(G.rootFusionDefeated||G.creatures.some(c=>c.name==="The Triune Maw"&&c.hp>0))return false;\n const base=CRE.find(c=>c.name==="The Triune Maw");if(!base)return false;\n G.creatures.push({id:Date.now()+Math.random(),name:base.name,hp:base.hp,maxHp:base.hp,armor:80,maxArmor:80,atk:base.atk,rarity:base.rarity,image:base.image,ability:base.ability,provoked:false,loc:"root",rootFusionBoss:true,triuneAttackCount:0,rootstormReady:false});\n log("🔥 THE TRIUNE MAW AWAKENS — 120 HP · 80 ARMOR · 14 ATK. The Root Gate remains sealed.","bad");\n updateStoryObjective();return true;\n}\n\nfunction spawnStoryBoss(loc){\n  if(G.clues<10)return false;'''
    t=t.replace(anchor,helpers,1)

# Root spawn remains locked until Triune Maw defeat.
t=t.replace('relicsComplete&&G.rootGateUnlocked&&!G.rootDefeated','relicsComplete&&G.rootGateUnlocked&&G.rootFusionDefeated&&!G.rootDefeated')

# Three guardian defeat trigger.
old='''  if(defeated>=3){\n    G.rootGateUnlocked=true;\n    log(`🌑 THE THREE SEALS BREAK. The entrance tears open and The Root of Blackwood awakens beyond the gate.`,"good");\n    spawnStoryBoss("root");\n  }'''
new='''  if(defeated>=3 && !G.rootFusionTriggered){\n    log(`🌑 THE THREE GUARDIANS FALL... but the gate does not open. Their remaining power begins to converge.`,"bad");\n    showRootFusionCutscene();\n  }'''
if old in t: t=t.replace(old,new,1)

# Triune Maw defeat opens the gate and only then spawns the Root.
if 'if(combat.name==="The Triune Maw"){' not in t:
    anchor='if(combat.name==="The Root of Blackwood"){' 
    if anchor not in t: raise SystemExit('fusion defeat: root handler anchor missing')
    t=t.replace(anchor,'if(combat.name==="The Triune Maw"){\n  G.rootFusionDefeated=true;G.rootGateUnlocked=true;\n  log("🗝️ THE TRIUNE MAW COLLAPSES. The fused seal breaks and the path to The Root of Blackwood finally opens.","good");\n  spawnStoryBoss("root");\n}\n'+anchor,1)

# Armor absorption for player damage against the fused boss.
if 'combat.rootFusionBoss && (combat.armor||0)>0' not in t:
    if 'combat.hp-=dmg;' not in t: raise SystemExit('fusion armor: damage anchor missing')
    t=t.replace('combat.hp-=dmg;','if(combat.rootFusionBoss && (combat.armor||0)>0){\n  const blocked=Math.min(combat.armor,dmg);combat.armor-=blocked;dmg-=blocked;\n  if(blocked>0)log(`🛡️ TRIUNE ARMOR absorbs ${blocked} damage. Armor ${combat.armor}/${combat.maxArmor||80}.`,"good");\n}\ncombat.hp-=dmg;',1)

# Berserk + Rootstorm creature ability.
if 'TRIUNE BERSERK!' not in t:
    anchor='// ===============================\n// RARE CREATURE ABILITIES'
    if anchor not in t: raise SystemExit('triune attack: rare ability anchor missing')
    code='''if(c.name==="The Triune Maw"){\n  c.triuneAttackCount=(c.triuneAttackCount||0)+1;\n  if(c.hp<=c.maxHp*0.5)dmg+=3;\n  if(c.triuneAttackCount%3===0){dmg+=6;p.san=Math.max(0,p.san-2);log(`🔥 TRIUNE BERSERK! ${p.name} loses 2 Sanity as the fused guardian unleashes a crushing strike.`,"bad");}\n  if(Math.random()<0.25){p.combatAp=Math.max(0,(p.combatAp||0)-1);log(`🌿 ROOTSTORM coils around ${p.name}, draining 1 Combat AP.`,"bad");}\n}\n\n'''
    t=t.replace(anchor,code+anchor,1)

# Objective progression.
if 'Objective 15 — Defeat The Triune Maw' not in t:
    anchor='  }else if(!G.rootGateUnlocked){\n    const defeated=(G.rootGateMinionsDefeated||[]).length;'
    repl='  }else if(!G.rootFusionDefeated && (G.rootGateMinionsDefeated||[]).length>=3){\n    objectiveText.innerHTML=`✅ Objective 14 — Three Gate Guardians defeated<br>➡️ Objective 15 — Defeat The Triune Maw`;\n  }else if(!G.rootGateUnlocked){\n    const defeated=(G.rootGateMinionsDefeated||[]).length;'
    if anchor in t: t=t.replace(anchor,repl,1)
if 'Objective 16 — Destroy the Root of Blackwood' not in t:
    t=t.replace('✅ Objective 14 — Root Gate broken<br>➡️ Objective 15 — Destroy the Root of Blackwood','✅ Objective 15 — Triune Maw destroyed · Root Gate broken<br>➡️ Objective 16 — Destroy the Root of Blackwood')
    t=t.replace('✅ Objective 15 — Root destroyed','✅ Objective 16 — Root destroyed')

# V0.5 player-facing patch note.
if 'Fusion Cutscene:' not in t and '<li><b>Root Gate Guardians:' in t:
    t=t.replace('<li><b>Root Gate Guardians:','<li><b>Fusion Cutscene:</b> Defeating all three Root Gate Guardians now triggers a four-scene transformation sequence before the new Abyssal fusion boss, The Triune Maw, enters combat.</li><li><b>Root Gate Guardians:',1)

p.write_text(t)
print('Final V0.5 Root fusion implementation applied.')
