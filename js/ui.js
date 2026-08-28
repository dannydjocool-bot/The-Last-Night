/* The Last Night — ui system. Extracted during architecture refactor; gameplay behavior preserved. */

function log(t,c=""){
  G.log.unshift(`<div class="${c}">${t}</div>`);

  const latest=document.getElementById("latestEvent");

  if(latest){
    latest.className="latest-event";

    if(c==="good") latest.classList.add("good");
    if(c==="bad") latest.classList.add("bad");

    latest.innerHTML=t;
  }

  renderLog();
}

function selectSurvivor(index){

  if(!G)return;
if(combat){
  log(
    `⚔️ You cannot manually switch Survivors during combat.`,
    "bad"
  );
  return;
}
  let survivor=G.ps[index];

  if(!survivor || survivor.dead){
    return;
  }

  // Selecting does NOT restore Action Points
  G.active=index;

  log(
    `👤 ${survivor.name} is now selected.`,
    "good"
  );

  render();
}

function render(){
updateStoryObjective();
let p=G.ps[G.active];
// EXTRA POCKETS UI
document.getElementById("extraPocketsCount").innerHTML=
`${G.extraPockets.length} / ${G.extraPocketMax} Slots`;

document.getElementById("extraPockets").innerHTML=

Array.from({length:G.extraPocketMax},(_,index)=>{

  let item=G.extraPockets[index];

  if(!item){
    return `
      <div class="extra-pocket-slot">
        <span class="muted">Slot ${index+1}: Empty</span>
      </div>
    `;
  }

  let rarityColor=
    item.rarity==="Common"?"#a8a8a8":
    item.rarity==="Uncommon"?"#4caf50":
    item.rarity==="Rare"?"#2196f3":
    item.rarity==="Epic"?"#9c27b0":
    item.rarity==="Legendary"?"#ffc107":
    "#777";

  return `
    <div class="extra-pocket-slot"
    style="border-color:${rarityColor};">

      ${item.image
      ? `<img class="extra-pocket-img"
          src="${item.image}"
          alt="${item.name}">`
      : ""}

      <b>${item.name}</b><br>

      <span style="
      color:${rarityColor};
      font-weight:bold;">
      ${item.rarity}
      </span>

      ${item.type==="weapon"
      ? `
        <br>⚔️ Damage: ${item.val}

        ${item.maxDurability!==undefined
        ? `<br>🔧 Durability:
           ${item.durability}/${item.maxDurability}`
        : ""}
${item.type==="tool"
? `
  <br>🛠️ Uses:
  ${item.durability}/${item.maxDurability}
`
: ""}
        ${item.ammoType && item.ammoType!=="melee"
        ? `<br>🔫 Uses:
           ${item.ammoType.toUpperCase()} Ammo`
        : ""}
        <br><br>
<button onclick="equipExtraPocketWeapon(${index})">
  ⚔️ EQUIP
</button>
      `
      : ""}
${item.type!=="weapon"
? `
  <br><br>
  <button onclick="useExtraPocketItem(${index})">
    🎒 USE
  </button>
`
: ""}
    </div>
  `;

}).join("");
  // SHARED AMMO DISPLAY
document.getElementById("ammoDisplay").innerHTML=`
  🔫 Pistol Ammo: <b>${G.ammo.pistol}</b><br>
  💥 Shotgun Ammo: <b>${G.ammo.shotgun}</b><br>
  ⚡ SMG Ammo: <b>${G.ammo.smg}</b><br>
  🎯 Rifle Ammo: <b>${G.ammo.rifle}</b>
`;
document.getElementById("turnTitle").innerHTML=
`<h2>Night ${G.night}/10 — ${p.name}</h2>
<div class="muted">
Clues: ${G.clues}/10 • ${
  combat
    ? `Combat AP: ${p.combatActions}`
    : `Night AP: ${p.actions}`
}
</div>`;

document.getElementById("map").innerHTML=L.map(x=>{

let discovered=G.discovered.has(x[0]);
let connected=LM[p.loc][2].includes(x[0]);
let zoneLabel=
  NORMAL_ZONES.includes(x[0]) ? "🟢 NORMAL" :
  DANGER_ZONES.includes(x[0]) ? "⚠️ DANGER" :
  VERY_RISKY_ZONES.includes(x[0]) ? "☠️ VERY RISKY" :
  VERY_DEADLY_ZONES.includes(x[0]) ? "💀 VERY DEADLY" :
  x[0]==="gate" ? "🏁 ESCAPE" :
  "";
return`
<div class="loc
${p.loc===x[0]?"current":""}
${discovered?"":"locked"}">

<b>${discovered?x[1]:"UNKNOWN"}</b>

${discovered && zoneLabel
  ? `<div style="margin-top:4px;font-weight:bold;">${zoneLabel}</div>`
  : ""
}

${p.loc===x[0]?"<div>📍 YOU ARE HERE</div>":""}


${discovered&&connected?
`<button onclick="useAction(1,()=>move('${x[0]}'))">Move</button>`:""}

</div>`;

}).join("");

const rarityStyles={
Common:{color:"#a8a8a8",label:"COMMON"},
Uncommon:{color:"#4caf50",label:"UNCOMMON"},
Rare:{color:"#2196f3",label:"RARE"},
Epic:{color:"#9c27b0",label:"EPIC"},
Legendary:{color:"#ffc107",label:"LEGENDARY"},
"G.O.A.T":{color:"#ffffff",label:"🐐 G.O.A.T"}
};

document.getElementById("player").innerHTML=
G.ps.map((sp,index)=>{

let rarity=rarityStyles[sp.rarity]||rarityStyles.Common;

let goatGlow=sp.rarity==="G.O.A.T"
?`box-shadow:0 0 18px #fff,0 0 32px #7c4dff,0 0 44px #00e5ff;`
:"";

return`

<div class="survivor-card-shell" style="
border:2px solid ${rarity.color};
${goatGlow}
${index===G.active
?'transform:scale(1.01);'
:'opacity:.82;'}
">

<img class="survivor-card-art"
src="${sp.image}"
alt="${sp.name}">

<div class="survivor-live-state">

<div class="survivor-card-status">
  <b>${index===G.active?'▶️ CURRENT TURN':'WAITING'}</b>
</div>

${!sp.dead
? `
<button onclick="selectSurvivor(${index})">
  👤 SELECT
</button>
`
: '<div class="bad"><b>DEAD</b></div>'}

<div class="stats survivor-live-stats">
<span class="stat">❤️ ${sp.hp}/${sp.maxHp}</span>
<span class="stat">🧠 ${sp.san}/${sp.maxSan}</span>
<span class="stat">😨 ${sp.fear}/5</span>
<span class="stat">
  ${combat ? `⚔️ ${sp.combatActions} Combat AP` : `🌙 ${sp.actions} Night AP`}
</span>
</div>

${sp.equippedLootWeapon
? `
<div class="survivor-live-box">
<b>🔫 EQUIPPED LOOT WEAPON</b><br>
${sp.equippedLootWeapon.name}<br>
<span class="muted">Damage: ${sp.equippedLootWeapon.val}</span>
${sp.equippedLootWeapon.maxDurability!==undefined
? `<br><span class="muted">🔧 Durability: ${sp.equippedLootWeapon.durability}/${sp.equippedLootWeapon.maxDurability}</span>`
: ""}
${sp.equippedLootWeapon.ammoType && sp.equippedLootWeapon.ammoType!=="melee"
? `<br><span class="muted">🔫 Ammo: ${G.ammo[sp.equippedLootWeapon.ammoType] || 0}</span>`
: ""}
<br><br>
<button onclick="switchToSignatureWeapon(${index})">
⚔️ Use Signature Weapon
</button>
</div>
`
: '<div class="good survivor-equipped-label">⚔️ Signature Weapon Equipped</div>'}

${index===G.active &&
!combat &&
sp.lifeRestoreReady &&
(sp.rarity==="Legendary" || sp.rarity==="G.O.A.T")
? `
<div class="survivor-live-box">
<b>💖 LIFE RESTORE READY</b><br>
${G.ps.map((target,targetIndex)=>{
  if(
    targetIndex===index ||
    target.dead ||
    target.rarity==="G.O.A.T" ||
    target.lives>=target.maxLives
  ){
    return "";
  }
  return "<button onclick='restoreLives(" + targetIndex + ")'>Restore " + target.name + " (+2 Lives)</button>";
}).join("")}
</div>
`
: ""}

<div class="survivor-live-box">
<b>⚡ SPECIAL ABILITY</b><br>
<div class="special-bar">
 <div class="special-fill" style="width:${sp.specialCharge}%"></div>
</div>
<span class="muted">${sp.specialCharge}% Charged</span>
</div>

</div>
</div>

`;

}).join("");

document.getElementById("inventory").innerHTML=

p.items.map((i,idx)=>

`<div class="card">
<b>${i.name}</b><br>
<span class="muted">${i.type}</span><br>
<button onclick="useItem(${idx})">Use</button>
</div>`

).join("");

document.getElementById("location").innerHTML=

`<b>${LM[p.loc][1]}</b>

<br><br>

<button onclick="useAction(1,search)">
Search (1 Action)
</button>

<button onclick="investigate()">
  🔎 Investigate
</button>

<button onclick="recover()">
  😴 Rest
</button>

<button
  id="endNightButton"
  onclick="endNight()"
  ${canEndNight() ? "" : "disabled"}
>
  🌙 End Night
</button>
`;

let here=G.creatures.filter(c=>c.loc===p.loc);

document.getElementById("creatures").innerHTML=

here.map(c=>

`<div class="card ${c.name==="The Hollow" && c.voidShield>0 ? "void-shield-active" : ""}" style="border:2px solid ${
c.rarity==="Common"?"#a8a8a8":
c.rarity==="Uncommon"?"#4caf50":
c.rarity==="Rare"?"#2196f3":
c.rarity==="Epic"?"#9c27b0":
c.rarity==="Legendary"?"#ffc107":
"#777"
};
">

<img class="survivor-img"
src="${c.image}"
alt="${c.name}">

<div style="
font-size:18px;
font-weight:bold;
margin-bottom:4px;
">
👹 ${c.name}
</div>

<div style="
font-weight:bold;
letter-spacing:1px;
margin-bottom:8px;
">
${c.rarity.toUpperCase()}
</div>

❤️ ${c.hp}/${c.maxHp}

<br>

⚔️ Damage ${c.atk}

<br><br>

<b>🔥 CREATURE ABILITY</b><br>
<span class="muted">${c.ability}</span>

<br><br>

<button onclick="startCombat('${c.id}')">
Fight
</button>

</div>`

).join("")

||"<span class='muted'>Nothing is here... yet.</span>";

if(combat){

document.getElementById("actions").innerHTML=

`<b>⚠️ COMBAT: ${combat.name}</b>

<br>

❤️ ${combat.hp}/${combat.maxHp}

<br><br>

<button onclick="attack()">Attack</button>

<button onclick="useSpecial()">⚡ USE SPECIAL</button>

<button onclick="flee()">Flee</button>

<button onclick="endTurn()">🔄 END TURN</button>`;

}
else{

document.getElementById("actions").innerHTML=

`<button onclick="endTurn()">END TURN</button>`;
}

renderLog();
}

function renderLog(){

if(!G)return;

document.getElementById("log").innerHTML=G.log.join("");
}

function toggleLog(){
  document.getElementById("logPanel").classList.toggle("log-open");
}

/* Extra Pockets panel positioning */
// DRAGGABLE EXTRA POCKETS
const extraPocketsPanel=document.getElementById("extraPocketsPanel");
const extraPocketsHandle=document.getElementById("extraPocketsHandle");
const resetExtraPocketsPosition=
  document.getElementById("resetExtraPocketsPosition");

let draggingExtraPockets=false;
let extraPocketOffsetX=0;
let extraPocketOffsetY=0;

const savedExtraPocketsPosition=
  localStorage.getItem("extraPocketsPosition");

if(savedExtraPocketsPosition && window.innerWidth>850){

  const savedPosition=
    JSON.parse(savedExtraPocketsPosition);

  if(savedPosition.left){
    extraPocketsPanel.style.left=savedPosition.left;
  }

  if(savedPosition.top){
    extraPocketsPanel.style.top=savedPosition.top;
  }

  extraPocketsPanel.style.right="auto";
  extraPocketsPanel.style.bottom="auto";
}
  
extraPocketsHandle.addEventListener("mousedown",function(e){

  if(window.innerWidth<=850)return;

  draggingExtraPockets=true;

  const rect=extraPocketsPanel.getBoundingClientRect();

  extraPocketOffsetX=e.clientX-rect.left;
  extraPocketOffsetY=e.clientY-rect.top;

  extraPocketsHandle.style.cursor="grabbing";

  e.preventDefault();
});

document.addEventListener("mousemove",function(e){

  if(!draggingExtraPockets)return;

  let newLeft=e.clientX-extraPocketOffsetX;
  let newTop=e.clientY-extraPocketOffsetY;

  // Keep panel inside screen
  newLeft=Math.max(
    0,
    Math.min(newLeft,window.innerWidth-extraPocketsPanel.offsetWidth)
  );

  newTop=Math.max(
    0,
    Math.min(newTop,window.innerHeight-extraPocketsPanel.offsetHeight)
  );

  extraPocketsPanel.style.left=newLeft+"px";
  extraPocketsPanel.style.top=newTop+"px";
  extraPocketsPanel.style.right="auto";
  extraPocketsPanel.style.bottom="auto";
});

document.addEventListener("mouseup",function(){

  if(!draggingExtraPockets)return;

  draggingExtraPockets=false;
  extraPocketsHandle.style.cursor="move";
  localStorage.setItem(
  "extraPocketsPosition",
  JSON.stringify({
    left:extraPocketsPanel.style.left,
    top:extraPocketsPanel.style.top
  })
);
});
  
  resetExtraPocketsPosition.addEventListener("click",function(){

  localStorage.removeItem("extraPocketsPosition");

  extraPocketsPanel.style.left="12px";
  extraPocketsPanel.style.top="90px";
  extraPocketsPanel.style.right="auto";
  extraPocketsPanel.style.bottom="auto";

});
