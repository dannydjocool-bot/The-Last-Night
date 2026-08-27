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
  // MANUALLY SELECT A SURVIVOR
