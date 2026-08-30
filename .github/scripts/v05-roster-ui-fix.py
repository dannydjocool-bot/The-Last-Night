from pathlib import Path

p = Path('index.html')
t = p.read_text()

css = r'''
/* V0.5 guardian showcase polish */
.new-survivor-showcase .new-goat-head,.new-gate-showcase .new-goat-head{display:flex;align-items:center;justify-content:space-between;gap:16px;text-align:left;margin-bottom:14px}
.new-survivor-showcase .new-goat-head>div,.new-gate-showcase .new-goat-head>div{min-width:0;flex:1}
.new-survivor-showcase .new-goat-head h2,.new-gate-showcase .new-goat-head h2{text-align:left;margin:0 0 5px}
.new-survivor-showcase .new-goat-head p,.new-gate-showcase .new-goat-head p{text-align:left;margin:0}
.showcase-next{width:auto!important;height:auto!important;min-width:172px!important;max-width:230px;padding:10px 14px!important;margin:0!important;white-space:normal;line-height:1.2;font-size:11px!important;font-weight:900;letter-spacing:.7px;border-radius:10px;background:linear-gradient(#2a2022,#171113);border:1px solid #89505a;color:#fff}
.gate-guardian-card{background:#0d0f11}
.gate-guardian-card img{object-fit:contain!important;object-position:center!important;background:radial-gradient(circle at 50% 44%,#211719 0,#0a0c0e 72%);padding:4px}
.codex-card img.codex-special-art{object-fit:contain;background:radial-gradient(circle at 50% 45%,#211719 0,#0a0c0e 75%);padding:3px}
@media(max-width:850px){.new-survivor-showcase .new-goat-head,.new-gate-showcase .new-goat-head{align-items:stretch;flex-direction:column;text-align:center}.new-survivor-showcase .new-goat-head h2,.new-gate-showcase .new-goat-head h2,.new-survivor-showcase .new-goat-head p,.new-gate-showcase .new-goat-head p{text-align:center}.showcase-next{width:100%!important;max-width:none!important;min-width:0!important}.gate-guardian-card img{height:auto!important;aspect-ratio:2/3!important;max-height:430px}}
'''

if '/* V0.5 guardian showcase polish */' not in t:
    t = t.replace('</style>', css + '\n</style>', 1)

t = t.replace('class="gate-guardian-nav showcase-next" onclick="showNewGuardianSection()"', 'class="showcase-next" onclick="showNewGuardianSection()"')
t = t.replace('class="gate-guardian-nav showcase-next" onclick="showNewSurvivorSection()"', 'class="showcase-next" onclick="showNewSurvivorSection()"')

# Remove the preview-only duplicate Triune Maw from the creature codex.
t = t.replace("Creatures ('+(CRE.length+1)+')", "Creatures ('+CRE.length+')")
t = t.replace('codexCards(type==="survivors"?S:[...CRE,{...ROOT_FUSION_CODEX,isNew:true,fusionPreview:true}],type)', 'codexCards(type==="survivors"?S:CRE,type)')

# Replace codex renderer with a single-source roster and full-art treatment for the new bosses.
start = t.find('function codexCards(list,type){')
end = t.find('\n\nfunction showCodex(type){', start)
if start < 0 or end < 0:
    raise SystemExit('codexCards block not found')

codex = r'''function codexCards(list,type){
  return `<div class="codex-grid">${list.map(entry=>{
    const isTriune=type==="creatures"&&entry.name==="The Triune Maw";
    const specialCreature=type==="creatures"&&(entry.gateGuardian||isTriune);
    const availability=type==="survivors"?(entry.recruitOnly?"FLASHLIGHT RECRUIT ONLY":"AVAILABLE SURVIVOR"):(isTriune?"FUSION THREAT":entry.gateGuardian?"ROOT GATE GUARDIAN":"KNOWN THREAT");
    return `<article class="codex-card"><img class="${specialCreature?'codex-special-art':''}" src="${entry.image}" alt="${entry.name}"><div><span class="codex-availability">${entry.isNew||entry.isNewRecruit||isTriune?'NEW · ':''}${availability}</span><h3>${entry.name}</h3><div class="codex-stats"><span>${entry.rarity}</span>${type==="survivors"?`<span>❤️ ${entry.hp}</span><span>🧠 ${entry.san}</span><span>⚔️ ${entry.damage}</span>`:`<span>❤️ ${entry.hp}</span>${entry.armor?`<span>🛡️ ${entry.armor}</span>`:""}<span>⚔️ ${entry.atk}</span>`}</div>${type==="survivors"?`<p><b>${entry.weapon}</b> — ${entry.weaponAbility}</p><p><b>Ability:</b> ${entry.ability}</p>${entry.recruitOnly?`<p class="recruit-only-badge">Found only through Flashlight exploration; joins at 30% HP.</p>`:""}${entry.transform?`<div class="wisdom-summary"><b>Transforms: ${entry.transform.name}</b><br>❤️ ${entry.hp+entry.transform.hpBonus} · ⚔️ ${entry.damage+entry.transform.damageBonus}<br>${entry.transform.weapon} — ${entry.transform.ability}</div>`:''}`:`<p><b>Creature Ability:</b> ${entry.ability}</p>${entry.bossZone?`<p><b>Story Location:</b> ${LM[entry.bossZone][1]}</p>`:""}${specialCreature?`<button onclick="viewRootFusionTransformation()">VIEW TRANSFORMATION</button>`:""}`}</div></article>`;
  }).join("")}</div>`;
}'''

t = t[:start] + codex + t[end:]

old = '''function showCodex(type){
  document.getElementById("codexSurvivors").classList.toggle("load-save",type==="survivors");
  document.getElementById("codexCreatures").classList.toggle("load-save",type==="creatures");
  document.getElementById("codexContent").innerHTML=codexCards(type==="survivors"?S:CRE,type);
}'''
new = '''function showCodex(type){
  document.getElementById("codexSurvivors").classList.toggle("load-save",type==="survivors");
  document.getElementById("codexCreatures").classList.toggle("load-save",type==="creatures");
  const source=type==="survivors"?S:CRE.filter((entry,index,array)=>array.findIndex(other=>other.name===entry.name)===index);
  document.getElementById("codexContent").innerHTML=codexCards(source,type);
}'''
if old in t:
    t = t.replace(old, new)

p.write_text(t)
