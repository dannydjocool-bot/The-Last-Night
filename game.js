/* The Last Night — core game state, data, turn flow, and shared helpers. */

/* The Last Night — core game logic.
   Refactor pass 1 preserves the original global API because index.html still
   uses inline onclick handlers. Follow-up passes can move those handlers to
   event listeners and split this file into modules safely. */
// ===============================
// ZONE DANGER LEVELS
// ===============================

// 🟢 NORMAL — 25% encounter chance

// ⚠️ DANGER — 60% encounter chance

// ☠️ VERY RISKY — 90% encounter chance

// 💀 VERY DEADLY — 100% encounter chance
  // ===============================
// BLACKWOOD STORY CLUES
// ===============================

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
