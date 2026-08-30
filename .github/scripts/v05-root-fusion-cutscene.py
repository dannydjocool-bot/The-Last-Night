from pathlib import Path
p=Path('index.html')
t=p.read_text()

def rep(old,new,label,count=1):
    global t
    if t.count(old)<count: raise SystemExit(f'{label}: pattern not found')
    t=t.replace(old,new,count)

# CSS
rep('.gate-guardian-dot.active{background:#e36b75;box-shadow:0 0 10px rgba(227,107,117,.7)}', '.gate-guardian-dot.active{background:#e36b75;box-shadow:0 0 10px rgba(227,107,117,.7)}.root-fusion-overlay{position:fixed;inset:0;z-index:19000;display:none;align-items:center;justify-content:center;padding:18px;background:rgba(0,0,0,.94);backdrop-filter:blur(10px)}.root-fusion-overlay.open{display:flex}.root-fusion-dialog{width:min(900px,96vw);max-height:94vh;overflow:auto;border:1px solid #7b2832;border-radius:18px;background:radial-gradient(circle at 50% 0,rgba(166,29,43,.22),transparent 38%),#08090a;box-shadow:0 25px 90px #000;padding:18px}.root-fusion-kicker{text-align:center;color:#ef6d79;font-size:10px;font-weight:900;letter-spacing:3px}.root-fusion-title{text-align:center;font-family:Georgia,serif;font-size:clamp(24px,5vw,40px);letter-spacing:2px;margin:8px 0}.root-fusion-scene{position:relative;min-height:430px;border:1px solid #573038;border-radius:14px;overflow:hidden;background:#060708}.root-fusion-scene:after{content:"";position:absolute;inset:45% 0 0;background:linear-gradient(transparent,rgba(0,0,0,.88))}.root-fusion-art{position:absolute;inset:0;background-size:cover;background-position:center}.root-fusion-art.panel1{background-image:linear-gradient(90deg,rgba(0,0,0,.15),rgba(120,0,15,.18)),url("wendigo.png")}.root-fusion-art.panel2{background-image:linear-gradient(90deg,rgba(205,143,48,.12),rgba(150,0,15,.24),rgba(215,215,215,.12)),url("bonecollector.png"),url("palebride.png")}.root-fusion-art.panel3{background-image:radial-gradient(circle at 50% 45%,rgba(255,30,46,.45),transparent 38%),url("wendigo.png")}.root-fusion-art.panel4{background-image:radial-gradient(circle at 50% 40%,rgba(255,20,38,.35),transparent 45%),url("rootofblackwood.png")}.root-fusion-copy{position:absolute;z-index:2;left:18px;right:18px;bottom:16px;padding:14px;border-left:3px solid #e65260;background:rgba(6,7,8,.78);font-weight:800;line-height:1.5}.root-fusion-actions{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:12px}.root-fusion-progress{font-size:11px;color:#aaa}.root-fusion-next{margin:0;background:linear-gradient(#942f3b,#651923);border-color:#c9525e;font-weight:900}', 'fusion css')
rep('@media(max-width:600px){\n  .new-gate-showcase', '@media(max-width:600px){\n  .root-fusion-overlay{padding:8px}.root-fusion-dialog{padding:10px;border-radius:12px}.root-fusion-scene{min-height:58vh}.root-fusion-copy{left:10px;right:10px;bottom:10px;font-size:12px;padding:10px}\n  .new-gate-showcase', 'mobile fusion css')

# Overlay HTML before log button
rep('<button id="logButton"', '<div id="rootFusionOverlay" class="root-fusion-overlay" aria-hidden="true"><div class="root-fusion-dialog"><div class="root-fusion-kicker">BLACKWOOD ROOT GATE INCIDENT</div><h2 id="rootFusionTitle" class="root-fusion-title">THE THREE BECOME ONE</h2><div class="root-fusion-scene"><div id="rootFusionArt" class="root-fusion-art panel1"></div><div id="rootFusionCopy" class="root-fusion-copy"></div></div><div class="root-fusion-actions"><span id="rootFusionProgress" class="root-fusion-progress"></span><button id="rootFusionNext" class="root-fusion-next" onclick="nextRootFusionScene()">NEXT →</button></div></div></div>\n<button id="logButton"', 'fusion html')

# Add fused creature definition before Root boss
needle='''  {\n  name:"The Root of Blackwood",\nhp:55,'''
fused='''{\nname:"The Triune Maw",\nhp:120,\natk:14,\nrarity:"Abyssal",\nweight:0,\nimage:"rootofblackwood.png",\nability:"Triune Berserk — 80 Armor. Every third strike erupts for +6 damage and drains 2 Sanity. While below 50% HP, gains +3 ATK.",\nbossZone:"root",rootFusionBoss:true,isNew:true,\nlore:"Thorn, blood, and ash forced into one impossible gate-beast. The three guardian seals now beat as a single heart."\n},\n  {\n  name:"The Root of Blackwood",\nhp:55,'''
rep(needle,fused,'fused definition')

# State fields
rep('  rootGateUnlocked:false,\n  rootDefeated:false,','  rootGateUnlocked:false,\n  rootFusionTriggered:false,\n  rootFusionDefeated:false,\n  rootDefeated:false,','fusion state')
rep('G.rootGateUnlocked=Boolean(G.rootGateUnlocked||G.rootGateMinionsDefeated.length>=3||G.rootDefeated);','G.rootGateUnlocked=Boolean(G.rootGateUnlocked||G.rootFusionDefeated||G.rootDefeated);\n  G.rootFusionTriggered=Boolean(G.rootFusionTriggered||G.rootFusionDefeated);\n  G.rootFusionDefeated=Boolean(G.rootFusionDefeated);','fusion migration')

# Helper/cutscene functions before spawnStoryBoss
anchor='''function spawnStoryBoss(loc){\n  if(G.clues<10)return false;'''
helpers='''let rootFusionSceneIndex=0;\nconst ROOT_FUSION_SCENES=[\n {title:"THE LAST SEAL SHUDDERS",copy:"All three Gate Guardians fall. The Veinmaw refuses to die quietly as the ruined entrance begins to pulse."},\n {title:"ROOT-KEY RESONANCE",copy:"Thornbound and Ash Wraith unravel into root-key energy. Their remaining power is dragged toward the red guardian."},\n {title:"TWO LOCKS OPEN",copy:"A lock ignites in the creature's chest and another burns behind its neck. Bark armor, crimson veins, and ash fuse into one body."},\n {title:"THE TRIUNE MAW",copy:"The fusion completes. A colossal armored gate-beast rises with impossible strength. The Root remains sealed behind it."}\n];\nfunction showRootFusionCutscene(){\n rootFusionSceneIndex=0;\n G.rootFusionTriggered=true;\n combat=null;\n const ov=document.getElementById("rootFusionOverlay"); if(!ov)return spawnTriuneMaw();\n ov.classList.add("open");ov.setAttribute("aria-hidden","false");document.body.style.overflow="hidden";renderRootFusionScene();\n}\nfunction renderRootFusionScene(){\n const s=ROOT_FUSION_SCENES[rootFusionSceneIndex];\n document.getElementById("rootFusionTitle").textContent=s.title;\n document.getElementById("rootFusionCopy").textContent=s.copy;\n document.getElementById("rootFusionArt").className="root-fusion-art panel"+(rootFusionSceneIndex+1);\n document.getElementById("rootFusionProgress").textContent=`SCENE ${rootFusionSceneIndex+1} / ${ROOT_FUSION_SCENES.length}`;\n document.getElementById("rootFusionNext").textContent=rootFusionSceneIndex===ROOT_FUSION_SCENES.length-1?"FACE THE TRIUNE MAW →":"NEXT →";\n}\nfunction nextRootFusionScene(){\n if(rootFusionSceneIndex<ROOT_FUSION_SCENES.length-1){rootFusionSceneIndex++;renderRootFusionScene();return;}\n const ov=document.getElementById("rootFusionOverlay");ov.classList.remove("open");ov.setAttribute("aria-hidden","true");document.body.style.overflow="";spawnTriuneMaw();render();\n}\nfunction spawnTriuneMaw(){\n if(G.rootFusionDefeated||G.creatures.some(c=>c.name==="The Triune Maw"&&c.hp>0))return false;\n const base=CRE.find(c=>c.name==="The Triune Maw");if(!base)return false;\n G.creatures.push({id:Date.now()+Math.random(),name:base.name,hp:base.hp,maxHp:base.hp,armor:80,maxArmor:80,atk:base.atk,rarity:base.rarity,image:base.image,ability:base.ability,provoked:false,loc:"root",rootFusionBoss:true,triuneAttackCount:0});\n log("🔥 THE TRIUNE MAW AWAKENS — 120 HP · 80 ARMOR · 14 ATK. The Root Gate remains sealed.","bad");\n updateStoryObjective();return true;\n}\n\nfunction spawnStoryBoss(loc){\n  if(G.clues<10)return false;'''
rep(anchor,helpers,'fusion helpers')

# Root boss may only spawn after fusion boss defeated
rep('relicsComplete&&G.rootGateUnlocked&&!G.rootDefeated','relicsComplete&&G.rootGateUnlocked&&G.rootFusionDefeated&&!G.rootDefeated','root spawn gate')

# Replace guardian completion block
old='''  if(defeated>=3){\n    G.rootGateUnlocked=true;\n    log(`🌑 THE THREE SEALS BREAK. The entrance tears open and The Root of Blackwood awakens beyond the gate.`,"good");\n    spawnStoryBoss("root");\n  }'''
new='''  if(defeated>=3 && !G.rootFusionTriggered){\n    log(`🌑 THE THREE GUARDIANS FALL... but the gate does not open. Something is pulling their power together.`,"bad");\n    showRootFusionCutscene();\n  }'''
rep(old,new,'guardian completion')

# Fused boss defeat handler before Root handler
rep('''if(combat.name==="The Root of Blackwood"){''','''if(combat.name==="The Triune Maw"){\n  G.rootFusionDefeated=true;\n  G.rootGateUnlocked=true;\n  log("🗝️ THE TRIUNE MAW COLLAPSES. The fused seal breaks and the path to The Root of Blackwood finally opens.","good");\n  spawnStoryBoss("root");\n}\nif(combat.name==="The Root of Blackwood"){''','fusion defeat')

# Creature armor damage absorption immediately before combat hp reduction
rep('''combat.hp-=dmg;''','''if(combat.rootFusionBoss && (combat.armor||0)>0){\n  const blocked=Math.min(combat.armor,dmg);combat.armor-=blocked;dmg-=blocked;\n  if(blocked>0)log(`🛡️ TRIUNE ARMOR absorbs ${blocked} damage. Armor ${combat.armor}/${combat.maxArmor||80}.`,"good");\n}\ncombat.hp-=dmg;''','fusion armor')

# Triune attack buffs before rare creature abilities section
rep('''// ===============================\n// RARE CREATURE ABILITIES''','''if(c.name==="The Triune Maw"){\n  c.triuneAttackCount=(c.triuneAttackCount||0)+1;\n  if(c.hp<=c.maxHp*0.5)dmg+=3;\n  if(c.triuneAttackCount%3===0){dmg+=6;p.san=Math.max(0,p.san-2);log(`🔥 TRIUNE BERSERK! ${p.name} loses 2 Sanity as the fused guardian unleashes a crushing strike.`,"bad");}\n}\n\n// ===============================\n// RARE CREATURE ABILITIES''','triune attack ability')

# Objective states
rep('''  }else if(!G.rootGateUnlocked){\n    const defeated=(G.rootGateMinionsDefeated||[]).length;''','''  }else if(!G.rootFusionDefeated && (G.rootGateMinionsDefeated||[]).length>=3){\n    objectiveText.innerHTML=`✅ Objective 14 — Three Gate Guardians defeated<br>➡️ Objective 15 — Defeat The Triune Maw`;\n  }else if(!G.rootGateUnlocked){\n    const defeated=(G.rootGateMinionsDefeated||[]).length;''','fusion objective')
rep('''  }else if(!G.rootDefeated){\n    objectiveText.innerHTML=`✅ Objective 14 — Root Gate broken<br>➡️ Objective 15 — Destroy the Root of Blackwood`;\n  }else{\n    objectiveText.innerHTML=`✅ Objective 15 — Root destroyed''','''  }else if(!G.rootDefeated){\n    objectiveText.innerHTML=`✅ Objective 15 — Triune Maw destroyed · Root Gate broken<br>➡️ Objective 16 — Destroy the Root of Blackwood`;\n  }else{\n    objectiveText.innerHTML=`✅ Objective 16 — Root destroyed''','objective numbering')

# Update patch notes with fusion feature
if 'Three Gate Guardians' in t and 'Triune Maw' in t:
    marker='<li><b>Root Gate Guardians:'
    if marker in t and 'Fusion Cutscene' not in t:
        t=t.replace(marker,'<li><b>Fusion Cutscene:</b> Defeating all three Root Gate Guardians now triggers a four-scene transformation sequence before the new Abyssal fusion boss, The Triune Maw, enters combat.</li>'+marker,1)

p.write_text(t)
print('V0.5 Root fusion cutscene patch applied.')
