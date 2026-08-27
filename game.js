/* The Last Night — core game state, data, turn flow, and shared helpers. */

/* The Last Night — core game logic.
   Refactor pass 1 preserves the original global API because index.html still
   uses inline onclick handlers. Follow-up passes can move those handlers to
   event listeners and split this file into modules safely. */

const L=[
["motel","Riverside Motel",["gas","store","station"]],
["gas","Abandoned Gas Station",["motel","store","forest"]],
["store","Blackwood General Store",["motel","gas","station","apartments"]],
["station","Police Station",["motel","store","library","firestation"]],
["library","Town Library",["station","apartments","school"]],
["apartments","Blackwood Apartments",["store","library","firestation","hotel"]],
["firestation","Abandoned Fire Station",["station","apartments","junkyard"]],
["cemetery","Old Cemetery",["chapel","monastery","forest"]],
["chapel","The Chapel",["cemetery","monastery","hospital"]],
["monastery","Ruined Monastery",["cemetery","chapel","cabins"]],
["cabins","Abandoned Cabins",["monastery","forest","huntercamp"]],

["forest","Blackwood Forest",["gas","cemetery","cabins","huntercamp","sawmill"]],
["huntercamp","Hunter's Camp",["cabins","forest","farm"]],
["junkyard","Blackwood Junkyard",["firestation","factory","farm"]],
["farm","Dead Man's Farm",["huntercamp","junkyard","sawmill"]],
["sawmill","Old Sawmill",["forest","farm","bridge"]],
["hospital","Abandoned Hospital",["chapel","school","sewers"]],
["school","Blackwood School",["library","hospital","subway"]],
["sewers","Blackwood Sewers",["hospital","tunnel","factory"]],
["tunnel","Underground Tunnel",["sewers","subway","house"]],
["bridge","Broken Bridge",["sawmill","hotel","mines"]],
["subway","Collapsed Subway",["school","tunnel","laboratory"]],

["house","The Old House",["tunnel","basement","hotel"]],
["hotel","Blackwood Hotel",["apartments","bridge","house","massgrave"]],
["factory","Abandoned Factory",["junkyard","sewers","massgrave","prison"]],
["mines","Blackwood Mines",["bridge","massgrave","laboratory"]],
["massgrave","Mass Grave",["hotel","factory","mines","slaughterhouse"]],
["basement","The Basement",["house","ritual"]],

["slaughterhouse","The Slaughterhouse",["massgrave","prison"]],
["prison","Blackwood Prison",["factory","slaughterhouse","asylum"]],
["asylum","Blackwood Asylum",["prison","laboratory"]],
["laboratory","Underground Laboratory",["subway","mines","asylum","ritual"]],
["ritual","The Ritual Chamber",["basement","laboratory","hollow"]],
["hollow","The Hollow",["ritual","root"]],
["root","The Root of Blackwood",["hollow","gate"]],
["gate","The Escape Gate",["root"]]
];
const LM=Object.fromEntries(L.map(x=>[x[0],x]));
// ===============================
// ZONE DANGER LEVELS
// ===============================

// 🟢 NORMAL — 25% encounter chance
const NORMAL_ZONES=[
  "motel",
  "gas",
  "store",
  "station",
  "library",
  "apartments",
  "firestation",
  "cemetery",
  "chapel",
  "monastery",
  "cabins"
];

// ⚠️ DANGER — 60% encounter chance
const DANGER_ZONES=[
  "forest",
  "huntercamp",
  "junkyard",
  "farm",
  "sawmill",
  "hospital",
  "school",
  "sewers",
  "tunnel",
  "bridge",
  "subway"
];

// ☠️ VERY RISKY — 90% encounter chance
const VERY_RISKY_ZONES=[
  "house",
  "hotel",
  "factory",
  "mines",
  "massgrave",
  "basement"
];

// 💀 VERY DEADLY — 100% encounter chance
const VERY_DEADLY_ZONES=[
  "slaughterhouse",
  "prison",
  "asylum",
  "laboratory",
  "ritual",
  "hollow"
];
  // ===============================
// BLACKWOOD STORY CLUES
// ===============================

const STORY_CLUES={

  station:{
    name:"Missing Persons Report",
    story:"Over several weeks, people began disappearing from Blackwood. Police records show every victim vanished sometime after midnight."
  },

  library:{
    name:"The Blackwood Disappearances",
    story:"Old newspaper records reveal the disappearances are not new. The same pattern has repeated every few decades for more than a century."
  },

  chapel:{
    name:"Father Elias' Confession",
    story:"A priest discovered that Blackwood was built over something ancient. His final warning reads: They aren't hunting us for food. They're keeping us here."
  },

  huntercamp:{
    name:"The Photograph in the Woods",
    story:"A hunter photographed a massive shadow watching Blackwood from the forest. On the back he wrote: The creatures never cross the town boundary."
  },

  hospital:{
    name:"Patient 013's Journal",
    story:"A survivor from an earlier cycle claimed the creatures become more aggressive every night, and that fear somehow makes them stronger."
  },

  school:{
    name:"The Final Recording",
    story:"Security footage from the night Blackwood fell shows people being dragged underground. A voice repeats: Ten must remember. Ten must know."
  },

  factory:{
    name:"The Underground Map",
    story:"Hidden tunnels connect Blackwood's oldest buildings. The map points toward a secret laboratory, a mass grave, and a ritual site beneath the town."
  },

  massgrave:{
    name:"The First Victims",
    story:"The bodies here are more than a century old. Symbols carved into their bones match symbols beneath the Chapel. Blackwood has repeated this nightmare for generations."
  },

  laboratory:{
    name:"Project BLACKWOOD",
    story:"Researchers discovered the creatures were never invading Blackwood. They were already here. Something beneath the town awakens them, and every attempt to destroy it has made the cycle worse."
  },

  ritual:{
    name:"The Blackwood Ritual",
    story:"The final document reveals that the creatures guard an entity known as The Hollow. The ten discoveries reveal how to break its hold over Blackwood and unseal the Escape Gate."
  }

};
  const STORY_OBJECTIVES=[
  {loc:"station",text:"Objective 1 — Investigate the Police Station"},
  {loc:"library",text:"Objective 2 — Investigate the Town Library"},
  {loc:"chapel",text:"Objective 3 — Investigate The Chapel"},
  {loc:"huntercamp",text:"Objective 4 — Investigate Hunter's Camp"},
  {loc:"hospital",text:"Objective 5 — Investigate the Abandoned Hospital"},
  {loc:"school",text:"Objective 6 — Investigate Blackwood School"},
  {loc:"factory",text:"Objective 7 — Investigate the Abandoned Factory"},
  {loc:"massgrave",text:"Objective 8 — Investigate the Mass Grave"},
  {loc:"laboratory",text:"Objective 9 — Investigate the Underground Laboratory"},
  {loc:"ritual",text:"Objective 10 — Investigate the Ritual Chamber"}
];
const S=[
{name:"The Doctor",hp:8,san:7,rarity:"Common",weight:20,image:"doctor.png",weapon:"Surgical Scalpel",damage:3,weaponAbility:"Precision Cut — Successful attacks restore 1 Sanity.",ability:"Medical Training — Heal 2 HP."},
{name:"The Hunter",hp:10,san:5,rarity:"Common",weight:20,image:"hunter.png",weapon:"Hunting Bow",damage:5,weaponAbility:"Deadeye — Rolling a 6 deals double damage.",ability:"Tracker — Reveal enemy information at combat start."},
{name:"The Runaway",hp:6,san:7,rarity:"Common",weight:20,image:"runaway.png",weapon:"Switchblade",damage:3,weaponAbility:"Quick Strike — First attack each combat costs 0 Actions.",ability:"Adrenaline Rush — Below 4 HP, gain +1 Action."},

{name:"The Journalist",hp:7,san:8,rarity:"Uncommon",weight:12,image:"journalist.png",weapon:"Heavy Camera",damage:2,weaponAbility:"Flashbang — Once per combat, prevent the enemy's next attack.",ability:"Expose — Better rewards from investigations."},
{name:"The Priest",hp:7,san:9,rarity:"Uncommon",weight:12,image:"priest.png",weapon:"Blessed Crucifix",damage:4,weaponAbility:"Exorcism — Bonus damage against supernatural creatures.",ability:"Faith — Remove 1 Fear from all Survivors once per game."},

{name:"The Mechanic",hp:9,san:6,rarity:"Rare",weight:6,image:"mechanic.png",weapon:"Modified Nail Gun",damage:5,weaponAbility:"Overcharge — Spend +1 Action to deal +4 damage.",ability:"Engineering — Improved repair and item effects."},
{name:"The Ex-Cop",hp:10,san:7,rarity:"Rare",weight:6,image:"excop.png",weapon:"Service Revolver",damage:6,weaponAbility:"Double Tap — Successful attacks may fire again.",ability:"Tactical Training — Gain +1 Action when combat begins."},

{name:"The Occultist",hp:7,san:10,rarity:"Epic",weight:2,image:"occultist.png",weapon:"Ritual Dagger",damage:5,weaponAbility:"Blood Magic — Sacrifice 2 HP to deal +5 damage.",ability:"Dark Knowledge — See enemy weaknesses."},

{name:"The Stranger",hp:8,san:8,rarity:"Legendary",weight:1,image:"stranger.png",weapon:"Blackwood Blade",damage:7,weaponAbility:"Unknown Power — Critical hits restore 2 HP and 2 Sanity.",ability:"Beyond Understanding — Resistant to negative events."},

{name:"The Chosen",hp:12,san:9,rarity:"G.O.A.T",weight:0.5,image:"chosen.png",weapon:"Blade of Dawn",damage:8,weaponAbility:"Divine Judgment — Once per combat, guaranteed critical hit and stun.",ability:"Second Life — First death returns you at 50% HP with +2 Actions."},
{name:"The Reaper",hp:11,san:8,rarity:"G.O.A.T",weight:0.5,image:"reaper.png",weapon:"Soul Scythe",damage:8,weaponAbility:"Soul Harvest — Kills restore 1 HP and 1 Sanity.",ability:"Death Sentence — Once per game, remove 50% of a creature's maximum HP."}
];

function drawSurvivors(amount){
let pool=[...S];
let chosen=[];

while(chosen.length<amount && pool.length){
let total=pool.reduce((sum,s)=>sum+s.weight,0);
let roll=Math.random()*total;
let pick=0;

for(let i=0;i<pool.length;i++){
roll-=pool[i].weight;
if(roll<=0){
pick=i;
break;
}
}

chosen.push(pool[pick]);
pool.splice(pick,1);
}

return chosen;
}

const ITEMS=[
["Flashlight","tool",0,"tool",5],
["First Aid Kit","heal",4],
["Healing Potion","healweak",5],
["Pistol","weapon",5,"pistol",5],
["Shotgun","weapon",8,"shotgun",5],
["MP5","weapon",7,"smg",5],
["AK-47","weapon",10,"rifle",5],

["Pistol Ammo","ammo",12,"pistol"],
["Shotgun Ammo","ammo",6,"shotgun"],
["SMG Ammo","ammo",20,"smg"],
["Rifle Ammo","ammo",12,"rifle"],

["Repair Kit","repair",5],

["Rusty Key","key",0], 
["Camera","tool",0,"tool",5],
["Hunting Knife","weapon",2,"melee",5],
["Fire Axe","weapon",6,"melee",5],
["Calmative","san",3],
["Emergency Rations","fear",2]
];

const ITEM_META={ 

  "Pistol":{
    rarity:"Rare",
    image:"pistol.png"
  },

  "Shotgun":{
    rarity:"Legendary",
    image:"shotgun.png"
  },

  "MP5":{
    rarity:"Epic",
    image:"mp5.png"
  },

  "AK-47":{
    rarity:"Epic",
    image:"ak47.png"
  },

  "Hunting Knife":{
    rarity:"Common",
    image:"huntingknife.png"
  },

  "Fire Axe":{
    rarity:"Rare",
    image:"fireaxe.png"
  },

  "Repair Kit":{
    rarity:"Uncommon",
    image:"repairkit.png"
  },

  "Flashlight":{
    rarity:"Common",
    image:"flashlight.png"
  },

  "Camera":{
    rarity:"Common",
    image:"camera.png"
  },

  "First Aid Kit":{
    rarity:"Uncommon",
    image:"firstaid.png"
  },
"Healing Potion":{
  rarity:"Rare",
  image:"healingpotion.png"
},
  "Rusty Key":{
    rarity:"Uncommon",
    image:"rustykey.png"
  },

  "Calmative":{
    rarity:"Uncommon",
    image:"calmative.png"
  },

  "Emergency Rations":{
    rarity:"Common",
    image:"rations.png"
  }
};
  
const CRE=[

{
name:"The Whisperer",
hp:7,
atk:2,
rarity:"Common",
weight:20,
image:"whisperer.png",
ability:"Whispers of Fear — Counter-attacks can drain Sanity."
},
{
name:"The Drifter",
hp:8,
atk:2,
rarity:"Common",
weight:20,
image:"drifter.png",
ability:"Desperate Lunge — Occasionally deals +1 damage when counter-attacking."
},

{
name:"The Weeper",
hp:6,
atk:2,
rarity:"Common",
weight:20,
image:"weeper.png",
ability:"Disturbing Cries — Its cries can increase Fear during combat."
},

{
name:"The Rotter",
hp:10,
atk:2,
rarity:"Common",
weight:20,
image:"rotter.png",
ability:"Rotting Grip — Tougher than most Common creatures and difficult to put down."
},
{
name:"The Mimic",
hp:9,
atk:4,
rarity:"Uncommon",
weight:12,
image:"mimic.png",
ability:"Perfect Imitation — Can copy the last attack used against it."
},
{
name:"The Screecher",
hp:10,
atk:3,
rarity:"Uncommon",
weight:12,
image:"screecher.png",
ability:"Piercing Scream — Its screams can damage Sanity during combat."
},

{
name:"The Skinwalker",
hp:11,
atk:3,
rarity:"Uncommon",
weight:12,
image:"skinwalker.png",
ability:"False Face — Can confuse Survivors and increase Fear."
},

{
name:"The Graveborn",
hp:12,
atk:3,
rarity:"Uncommon",
weight:12,
image:"graveborn.png",
ability:"Grave Resilience — Has a chance to survive a killing blow with 1 HP."
},
{
name:"The Stalker",
hp:12,
atk:3,
rarity:"Rare",
weight:6,
image:"stalker.png",
ability:"Relentless Pursuit — Becomes stronger after being provoked."
},
{
name:"The Butcher",
hp:16,
atk:5,
rarity:"Rare",
weight:6,
image:"butcher.png",
ability:"Blood Frenzy — Becomes more dangerous after damaging a wounded Survivor."
},

{
name:"The Night Hag",
hp:14,
atk:4,
rarity:"Rare",
weight:6,
image:"nighthag.png",
ability:"Nightmare Touch — Can drain Sanity and increase Fear during combat."
},
{
name:"The Crawling Man",
hp:15,
atk:5,
rarity:"Epic",
weight:2,
image:"crawlingman.png",
ability:"Unnatural Reach — Its attacks can bypass some protection."
},
{
name:"The Pale Bride",
hp:18,
atk:6,
rarity:"Epic",
weight:2,
image:"palebride.png",
ability:"Mourning Curse — Her attacks can drain Sanity and spread Fear through the party."
},

{
name:"The Bone Collector",
hp:22,
atk:5,
rarity:"Epic",
weight:2,
image:"bonecollector.png",
ability:"Harvest the Fallen — Becomes stronger when a Survivor is knocked out."
},

{
name:"The Wendigo",
hp:20,
atk:7,
rarity:"Epic",
weight:2,
image:"wendigo.png",
ability:"Predator's Hunger — Becomes more aggressive as its Health gets lower."
},
{
name:"The Bloodkeeper",
hp:28,
atk:7,
rarity:"Legendary",
weight:1,
image:"bloodkeeper.png",
ability:"Blood Tribute — 35% chance when attacking to restore 3 HP."
},
{
name:"The Blackwood Sentinel",
hp:30,
atk:8,
rarity:"Legendary",
weight:1,
image:"blackwoodsentinel.png",
ability:"Ancient Guard — The first successful attack against it each combat deals 50% less damage."
},
{
name:"The Hollow",
hp:38,
atk:9,
rarity:"Ancient",
weight:0,
image:"hollow.png",
ability:"Void Consumption — Can drain Actions from its victim. Last Response — If a normal attack would kill The Hollow, it revives once at 30% HP, gains +55% Attack Damage, and summons a 15-point Void Shield.",
bossZone:"hollow"
},
{
name:"The Warden",
hp:34,
atk:9,
rarity:"Mythic",
weight:0,
image:"warden.png",
ability:"Prisoner's Judgment — The Warden punishes wounded Survivors with devastating attacks.",
bossZone:"prison"
},
  {
  name:"The Root of Blackwood",
hp:55,
atk:11,
  rarity:"Abyssal",
  weight:0,
  image:"rootofblackwood.png",
  ability:"Blackwood Awakens — The ancient source of the nightmare grows stronger as it is wounded.",
  bossZone:"root"
}
];

const EVENTS=[
["Lights Out","Your flashlight flickers."],
["Something Moved","Lose 1 Sanity."],
["Footsteps","A creature appears nearby."],
["Don't Look Behind You","Gain 1 Fear."],
["The Door Opens","A creature appears immediately."]
];

let G=null;
let combat=null;

const d6=()=>1+Math.floor(Math.random()*6);
const rnd=a=>a[Math.floor(Math.random()*a.length)];
function specialChargeRate(rarity){
  const rates={
    "Common":20,
    "Uncommon":25,
    "Rare":34,
    "Epic":50,
    "Legendary":100,
    "G.O.A.T":50
  };

  return rates[rarity]||20;
}

function chargeSpecial(p){
  if(p.specialCharge>=100)return;

  let amount=specialChargeRate(p.rarity);

  p.specialCharge=Math.min(100,p.specialCharge+amount);

  log(`🔥 ${p.name}'s Special Meter increased to ${p.specialCharge}%.`,
      p.specialCharge>=100?"good":"");

  if(p.specialCharge>=100){
    log(`⚡ ${p.name}'s SPECIAL ABILITY IS READY!`,"good");
  }
}
  
function maxRestsPerNight(p){

  if(p.rarity==="G.O.A.T"){
    return 5;
  }

  if(p.rarity==="Legendary"){
    return 4;
  }

  if(p.rarity==="Epic"){
    return 3;
  }

  return 2;
}
function startGame(n){
let ps=drawSurvivors(n).map(s=>({
name:s.name,
maxHp:s.hp,
hp:s.hp,
  baseMaxHp:s.hp,
baseWeaponDamage:s.damage,
san:s.san,
maxSan:s.san,
rarity:s.rarity,
image:s.image,
weapon:s.weapon,
weaponDamage:s.damage,
weaponAbility:s.weaponAbility,
ability:s.ability,
specialCharge:s.rarity==="G.O.A.T"?100:0,
specialUses:0,
  lives:s.rarity==="G.O.A.T"?Infinity:3,
maxLives:s.rarity==="G.O.A.T"?Infinity:3,
knockedOut:false,
dead:false,
  berserk:false,
berserkUsedThisBattle:false,
berserkSpecialBoostReady:false,
  lifeRestoreReady:false,
enemyStunned:false,
handcuffedTurns:0,
weak:false,
fear:0,
loc:"motel",
actions:25,
combatActions:0,
restsThisNight:0,
  freeInvestigateUsed:false,
items:[
{name:"Flashlight",type:"tool",val:0},
objItem(rnd(ITEMS.slice(1)))
]
}));

G={
ps,
active:0,
night:1,
clues:0,
foundClues:new Set(),
discovered:new Set(["motel","gas","forest","station"]),
  wardenDefeated:false,
hollowDefeated:false,
bloodkeeperDefeated:false,
sentinelDefeated:false,
  rootEntered:false,
  rootDefeated:false,
storyItems:[],
creatures:[],
  extraPockets:[],
extraPocketMax:10,
  ammo:{
  pistol:0,
  shotgun:0,
  smg:0,
  rifle:0
},
log:[]
};

document.getElementById("setup").style.display="none";
document.getElementById("game").style.display="grid";

updateStoryObjective();

log("The survivors wake at the Riverside Motel.","good");
log("Find all 10 story clues and reach the Escape Gate before Night 10.");
startTurn();
}

function objItem(x){

  let item={
    name:x[0],
    type:x[1],
    val:x[2]
  };

  if(x[3]!==undefined){
    item.ammoType=x[3];
  }

  if(x[4]!==undefined){
    item.maxDurability=x[4];
    item.durability=x[4];
  }
let meta=ITEM_META[item.name];

if(meta){
  item.rarity=meta.rarity;
  item.image=meta.image;
}
else{
  item.rarity="Common";
  item.image=null;
}
  return item;
}

function startTurn(){

let p=G.ps[G.active];
// Actions are now refreshed only when a new Night begins

let e=rnd(EVENTS);

log(`<b>EVENT:</b> ${e[0]} — ${e[1]}`);

if(e[0]==="Something Moved")
p.san=Math.max(0,p.san-1);

if(e[0]==="Footsteps"||e[0]==="The Door Opens")
spawn(p.loc);

if(e[0]==="Don't Look Behind You")
p.fear++;

check(p);
render();
}

function useAction(cost,fn){

  let p=G.ps[G.active];

  if(p.actions<cost){
    log("You don't have enough actions.","bad");
    return;
  }

  p.actions-=cost;

  fn();
  render();
}
  // MANUALLY SELECT A SURVIVOR
  function endTurn(){

  let p=G.ps[G.active];

  // COMBAT END TURN
if(combat){

    // Creature only attacks after being provoked
    if(combat.provoked){
        creatureAttack(combat);

        // Party may have been defeated during the creature attack
        if(!combat){
            return;
        }

        // If this survivor was knocked out/dead,
        // switchCombatSurvivor() already handled the next fighter
        if(p.knockedOut || p.dead || p.hp<=0){
            return;
        }
    }

    // Reset combat Actions for the active survivor
  p.combatActions=combatActionCount(p);

    // All living, conscious allies recover +1 HP
    G.ps.forEach(ally=>{

        if(
            ally.dead ||
            ally.knockedOut ||
            ally.hp<=0
        ) return;

        if(ally.hp<ally.maxHp){

            ally.hp=Math.min(
                ally.maxHp,
                ally.hp+1
            );

            log(
                `❤️ ${ally.name} recovers 1 HP after the combat round.`,
                "good"
            );
        }
    });

    log(
    `🔄 ${p.name} begins another combat round with ${p.combatActions} Combat Actions.`,
    );

    render();
    return;
}

  // NORMAL ESCAPE CHECK
 if(p.loc==="gate"&&G.clues>=10){
  
    alert("YOU ESCAPED BLACKWOOD!\n\nYou survived The Last Night.");

    location.reload();
    return;
  }

// NORMAL SURVIVOR ADVANCE
let startingActive=G.active;

do{

  G.active++;

  if(G.active>=G.ps.length){
    G.active=0;
  }

  // Stop when we find a living Survivor with Actions remaining
  if(
    !G.ps[G.active].dead &&
    G.ps[G.active].actions>0
  ){
    break;
  }

}while(G.active!==startingActive);
// EVERYONE IS OUT OF ACTIONS
if(canEndNight()){

  // Keep the current Survivor active so Rest/items can still be used
  G.active=startingActive;

  log(
    `🌙 All living Survivors are out of Action Points. You may Rest, use healing/effect items, or End the Night.`,
    "good"
  );

  render();
  return;
}
  if(G.night>=10){

if(G.clues>=10){

      G.discovered.add("gate");

        log(
          "THE FINAL NIGHT HAS BEGUN. THE ESCAPE GATE IS OPEN.",
          "bad"
        );

      }
      else{

        alert(
          "Night 10 arrives before you uncover the truth.\n\nTHE DARKNESS CONSUMES BLACKWOOD."
        );

        location.reload();
        return;
      }
    }

  startTurn();
}

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
