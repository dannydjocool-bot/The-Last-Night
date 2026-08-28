/* The Last Night — story system. Extracted during architecture refactor; gameplay behavior preserved. */

function updateStoryObjective(){

  if(!G)return;

  let objectiveText=document.getElementById("storyObjectiveText");
  let objectiveProgress=document.getElementById("storyObjectiveProgress");

  if(!objectiveText || !objectiveProgress)return;

  let currentObjective=STORY_OBJECTIVES[G.clues];
  let completedObjective=
    G.clues>0 ? STORY_OBJECTIVES[G.clues-1] : null;

  if(currentObjective){

    if(completedObjective){
      objectiveText.innerHTML=
        `✅ ${completedObjective.text}<br>` +
        `➡️ ${currentObjective.text}`;
    }
    else{
      objectiveText.innerHTML=
        `➡️ ${currentObjective.text}`;
    }

  }
else{

  if(!G.wardenDefeated || !G.hollowDefeated){

    let wardenStatus=
      G.wardenDefeated ? "✅ The Warden defeated" : "⬜ Defeat The Warden";

    let hollowStatus=
      G.hollowDefeated ? "✅ The Hollow defeated" : "⬜ Defeat The Hollow";

    objectiveText.innerHTML=
      `✅ All 10 story clues discovered.<br>` +
      `➡️ Objective 11 — Break the Guardians<br>` +
      `${wardenStatus}<br>` +
      `${hollowStatus}`;
  }

else{

  if(!G.bloodkeeperDefeated || !G.sentinelDefeated){

    let bloodkeeperStatus=
      G.bloodkeeperDefeated
        ? "✅ The Bloodkeeper defeated"
        : "⬜ Defeat The Bloodkeeper";

    let sentinelStatus=
      G.sentinelDefeated
        ? "✅ The Blackwood Sentinel defeated"
        : "⬜ Defeat The Blackwood Sentinel";

    objectiveText.innerHTML=
      `✅ Objective 11 — The Warden and The Hollow defeated<br>` +
      `🔑 Warden-Hollow Relic acquired<br>` +
      `➡️ Objective 12 — Hunt the Legendary Creatures<br>` +
      `${bloodkeeperStatus}<br>` +
      `${sentinelStatus}`;
  }

else{

  let hasBloodkeeper=
    G.storyItems.includes("Bloodkeeper Relic");

  let hasSentinel=
    G.storyItems.includes("Sentinel Relic");

  let hasWardenHollow=
    G.storyItems.includes("Warden-Hollow Relic");

  if(!hasBloodkeeper || !hasSentinel || !hasWardenHollow){

    objectiveText.innerHTML=
      `➡️ Objective 13 — Assemble the Three Relics<br>` +
      `${hasBloodkeeper ? "✅" : "⬜"} Bloodkeeper Relic<br>` +
      `${hasSentinel ? "✅" : "⬜"} Sentinel Relic<br>` +
      `${hasWardenHollow ? "✅" : "⬜"} Warden-Hollow Relic`;
  }

else{

  if(!G.rootEntered){
    objectiveText.innerHTML=
      `✅ Objective 13 — All Three Relics Assembled<br>` +
      `➡️ Objective 14 — Enter the Root of Blackwood`;
  }

else if(!G.rootDefeated){
  objectiveText.innerHTML=
    `✅ Objective 14 — Entered the Root of Blackwood<br>` +
    `➡️ Objective 15 — Destroy the Root of Blackwood`;
}

else{
  objectiveText.innerHTML=
    `✅ Objective 15 — The Root of Blackwood Destroyed<br>` +
    `➡️ Objective 16 — Reach the Escape Gate`;
}
}
}
}
}
  objectiveProgress.textContent=
    `Story Clues: ${G.clues} / 10`;
}

function move(id){

let p=G.ps[G.active];

if(!LM[p.loc][2].includes(id)){
log("That location isn't connected.");
return;
}

if(id==="gate"&&G.clues<10){
  log(`🔒 The Escape Gate is sealed. Find all 10 clues. (${G.clues}/10)`,"bad");
  return;
}
  if(id==="gate" && !G.rootDefeated){
  log(
    `🔒 The Escape Gate remains sealed. Destroy the Root of Blackwood first.`,
    "bad"
  );
  return;
}
if(
  id==="root" &&
  (
    !G.storyItems.includes("Bloodkeeper Relic") ||
    !G.storyItems.includes("Sentinel Relic") ||
    !G.storyItems.includes("Warden-Hollow Relic")
  )
){
  log(
    `🔒 The Root of Blackwood is sealed. All 3 story relics are required.`,
    "bad"
  );
  return;
}
// ===============================
// DANGER WARNING BEFORE ENTERING
// ===============================

let warningText="";

if(DANGER_ZONES.includes(id)){
  warningText=
    `⚠️ DANGER ZONE\n\n` +
    `${LM[id][1]}\n\n` +
    `Creature Encounter Chance: 60%\n\n` +
    `Enter anyway?`;
}

else if(VERY_RISKY_ZONES.includes(id)){
  warningText=
    `☠️ VERY RISKY ZONE\n\n` +
    `${LM[id][1]}\n\n` +
    `Creature Encounter Chance: 90%\n\n` +
    `Enter anyway?`;
}

else if(VERY_DEADLY_ZONES.includes(id)){
  warningText=
    `💀 VERY DEADLY ZONE\n\n` +
    `${LM[id][1]}\n\n` +
    `Creature Encounter Chance: 100%\n\n` +
    `Enter anyway?`;
}

if(warningText && !confirm(warningText)){
  log(`${p.name} decides not to enter ${LM[id][1]}.`);
  return;
}
// Move the entire surviving party together
G.ps.forEach(s=>{
  if(!s.dead){
    s.loc=id;
  }
});
  // STORY — ROOT ENTERED
if(id==="root"){
  G.rootEntered=true;
  updateStoryObjective();
}
G.discovered.add(id);

LM[id][2].forEach(x=>G.discovered.add(x));

log(`The party moves to ${LM[id][1]}.`);
// ===============================
// ZONE ENCOUNTER CHANCE
// ===============================

let encounterChance=0;

if(NORMAL_ZONES.includes(id)){
  encounterChance=0.25;
}
else if(DANGER_ZONES.includes(id)){
  encounterChance=0.60;
}
else if(VERY_RISKY_ZONES.includes(id)){
  encounterChance=0.90;
}
else if(VERY_DEADLY_ZONES.includes(id)){
  encounterChance=1.00;
}

if(encounterChance>0 && Math.random()<encounterChance){
  spawn(id);
}

}

function search(){

let p=G.ps[G.active];
let r=d6();

log(`${p.name} searches and rolls ${r}.`);

if(r===1){
encounter();
}
else if(r<=3){
log("Nothing useful.");
}
else if(r===4){
gainItem();
}
else if(r===5){
gainClue();
}
else{
gainItem();
gainClue();
}
}

function investigate(){

  let p=G.ps[G.active];

  // First Investigate each Night is FREE
  if(!p.freeInvestigateUsed){

    p.freeInvestigateUsed=true;

    log(
      `🔎 ${p.name} uses their FREE Investigate for Night ${G.night}.`,
      "good"
    );

    gainClue();
    render();
    return;
  }

  // Later Investigates cost 1 Action
  if(p.actions<1){

    log(
      `⚡ ${p.name} needs 1 Action to Investigate again.`,
      "bad"
    );

    return;
  }

  p.actions-=1;

  log(
    `🔎 ${p.name} Investigates for 1 Action.`,
    "good"
  );

  gainClue();
  render();
}

function gainClue(){

  let p=G.ps[G.active];
  let clue=STORY_CLUES[p.loc];
// STORY OBJECTIVES MUST BE COMPLETED IN ORDER
let currentObjective=STORY_OBJECTIVES[G.clues];

if(
  currentObjective &&
  p.loc!==currentObjective.loc
){
  log(
    `📜 CURRENT OBJECTIVE: ${currentObjective.text}`,
    "bad"
  );
  return;
}
  if(!clue){
    log(`🔎 There is no major story clue at ${LM[p.loc][1]}.`);
    return;
  }

  if(G.foundClues.has(p.loc)){
    log(`📖 You already discovered the clue at ${LM[p.loc][1]}.`);
    return;
  }

  G.foundClues.add(p.loc);
  G.clues=G.foundClues.size;

  log(
    `📖 STORY CLUE FOUND: <b>${clue.name}</b>`,
    "good"
  );

  log(
    `${clue.story}`,
    "good"
  );

updateStoryObjective();
if(G.clues===10){

  log(
    `📖 ALL 10 STORY CLUES FOUND! The truth of Blackwood has been uncovered. New story objectives await.`,
    "good"
  );
}
}

function encounter(){

let p=G.ps[G.active];
let r=d6();

if(r<=2){
p.san=Math.max(0,p.san-1);
log("A whisper crawls through the darkness. Lose 1 Sanity.","bad");
}
else if(r<=4){
p.fear++;
log("Something watches you. Gain 1 Fear.","bad");
}
else if(r===5){
gainItem();
}
else{
spawn(p.loc);
}

check(p);
}

function spawn(loc){
 // ===============================
// SPECIAL BOSS ENCOUNTER ROLLS
// ===============================

// MYTHIC — THE WARDEN
if(loc==="prison"){

  // TRUE 20% chance
  if(Math.random() < 0.20){

    let b=CRE.find(c=>
      c.rarity==="Mythic" &&
      c.bossZone==="prison"
    );

    if(b){

      let c={
        id:Date.now()+Math.random(),
        name:b.name,
        hp:b.hp,
        maxHp:b.hp,
        atk:b.atk,
        rarity:b.rarity,
        image:b.image,
        ability:b.ability,
        provoked:false,
        handcuffActive:false,
handcuffCooldownHp:null,
        loc
      };

      G.creatures.push(c);

      log(
        `🔥 MYTHIC ENCOUNTER! <b>${c.name}</b> has appeared!`,
        "bad"
      );

      return;
    }
  }
}

// ANCIENT — THE HOLLOW
if(loc==="hollow"){

  // TRUE 10% chance
  if(Math.random() < 0.10){

    let b=CRE.find(c=>
      c.rarity==="Ancient" &&
      c.bossZone==="hollow"
    );

    if(b){

      let c={
        id:Date.now()+Math.random(),
        name:b.name,
        hp:b.hp,
        maxHp:b.hp,
        atk:b.atk,
        rarity:b.rarity,
        image:b.image,
        ability:b.ability,
        provoked:false,
        voidShield:0,
voidShieldActivated:false,
        lastStandUsed:false,
        loc
      };

      G.creatures.push(c);

      log(
        `👁️ ANCIENT ENCOUNTER! <b>${c.name}</b> has appeared!`,
        "bad"
      );

      return;
    }
  }
}
 // ABYSSAL — THE ROOT OF BLACKWOOD
if(loc==="root"){
  if(G.rootDefeated){
  return;
}
if(!G.storyItems.includes("Warden-Hollow Relic")){
  log(
    `🌑 Something ancient sleeps beneath Blackwood. The Warden-Hollow Relic is required to awaken it.`,
    "bad"
  );
  return;
}
  let b=CRE.find(c=>
    c.rarity==="Abyssal" &&
    c.bossZone==="root"
  );

  if(b){

    let alreadySpawned=G.creatures.some(c=>
      c.name==="The Root of Blackwood"
    );

    if(!alreadySpawned){

      let c={
        id:Date.now()+Math.random(),
        name:b.name,
        hp:b.hp,
        maxHp:b.hp,
        atk:b.atk,
        rarity:b.rarity,
        image:b.image,
        ability:b.ability,
        provoked:false,
        loc
      };

      G.creatures.push(c);

      log(
        `🌑 ABYSSAL ENCOUNTER! <b>${c.name}</b> has awakened!`,
        "bad"
      );
    }

    return;
  }
}
// ===============================
// ZONE-BASED CREATURE POOLS
// ===============================

let allowedRarities=[];

if(NORMAL_ZONES.includes(loc)){
  allowedRarities=["Common","Uncommon"];
}

else if(DANGER_ZONES.includes(loc)){
  allowedRarities=["Common","Uncommon","Rare"];
}

else if(VERY_RISKY_ZONES.includes(loc)){
  allowedRarities=["Uncommon","Rare","Epic"];
}

else if(VERY_DEADLY_ZONES.includes(loc)){
  allowedRarities=["Rare","Epic"];
}

else{
  allowedRarities=["Common","Uncommon"];
}

let regularPool=CRE.filter(c=>
  allowedRarities.includes(c.rarity)
);

let total=regularPool.reduce((sum,c)=>sum+c.weight,0);
let roll=Math.random()*total;
let b=regularPool[0];

for(let i=0;i<regularPool.length;i++){
  roll-=regularPool[i].weight;

  if(roll<=0){
    b=regularPool[i];
    break;
  }
}
let c={
  id:Date.now()+Math.random(),
  name:b.name,
  hp:b.hp,
  maxHp:b.hp,
  atk:b.atk,
  rarity:b.rarity,
  image:b.image,
  ability:b.ability,
  provoked:false,
  loc
};

G.creatures.push(c);

log(
  `👹 A <b>${c.rarity} ${c.name}</b> appears!`,
  "bad"
);
}

function canEndNight(){

  if(!G)return false;

  return G.ps
    .filter(p=>!p.dead)
    .every(p=>p.actions<=0);
}

function endNight(){

  if(!canEndNight()){
    log(
      `🌙 The Night cannot end until all living Survivors have 0 Action Points.`,
      "bad"
    );
    render();
    return;
  }

  G.night++;

  // Reset every living Survivor for the new Night
  G.ps.forEach(p=>{

    if(p.dead)return;

    p.actions=15;
    p.restsThisNight=0;
    p.freeInvestigateUsed=false;
  });

  log(
    `🌙 NIGHT ${G.night} BEGINS! Action Points, Rest chances, and FREE Investigates have been refreshed.`,
    "good"
  );

  render();
}

function recover(){

  let p=G.ps[G.active];

  if(combat){
    log(
      `⚔️ ${p.name} cannot Rest during combat.`,
      "bad"
    );
    return;
  }

  let maxRests=maxRestsPerNight(p);

  if(p.restsThisNight>=maxRests){
    log(
      `😴 ${p.name} has used all Rest chances for Night ${G.night} (${p.restsThisNight}/${maxRests}).`,
      "bad"
    );
    return;
  }

  p.restsThisNight++;

  let oldHp=p.hp;
  let oldSan=p.san;
  let oldFear=p.fear;

  p.hp=Math.min(p.maxHp,p.hp+3);
  p.san=Math.min(p.maxSan,p.san+2);
  p.fear=Math.max(0,p.fear-1);

  // Rest gives 3 Action Points
  p.actions+=3;

  log(
    `😴 ${p.name} RESTS! ❤️ +${p.hp-oldHp} HP • 🧠 +${p.san-oldSan} Sanity • 😨 -${oldFear-p.fear} Fear • ⚡ +3 Actions • Rest ${p.restsThisNight}/${maxRests}.`,
    "good"
  );

  render();
}
