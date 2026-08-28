/* The Last Night — combat system. Extracted during architecture refactor; gameplay behavior preserved. */

function useCombatAction(cost,fn){

  let p=G.ps[G.active];
// WARDEN HANDCUFF EFFECT
if(p.handcuffedTurns>0){

  p.handcuffedTurns--;

  log(
    `⛓️ ${p.name} is HANDCUFFED and loses this combat turn! ${p.handcuffedTurns} restrained turns remain.`,
    "bad"
  );

  if(p.handcuffedTurns===0){

    p.weak=true;

    log(
      `⚠️ ${p.name} breaks free but returns WEAK! Attack damage is reduced by 30% for the rest of this battle.`,
      "bad"
    );
  }

  render();
  return;
}
  if(!combat){
    log("You are not in combat.","bad");
    return;
  }

  if(p.combatActions<cost){
    log("You don't have enough Combat Actions.","bad");
    return;
  }

  p.combatActions-=cost;

  fn();
  render();
}

function combatActionCount(p){

  const bonus={
    "Common":0,
    "Uncommon":1,
    "Rare":2,
    "Epic":3,
    "Legendary":4,
    "G.O.A.T":5
  };

  return 10+(bonus[p.rarity]||0);
}

function startCombat(id){

combat=G.creatures.find(c=>String(c.id)===String(id));
  if(
  combat &&
  combat.name==="The Blackwood Sentinel"
){
  combat.ancientGuardUsed=false;
}
if(combat){
  let p=G.ps[G.active];
  p.combatActions=combatActionCount(p);
}
if(combat)
log(`Combat begins against ${combat.name}.`,"bad");

render();
}

function attack(){

if(!combat)return;

let p=G.ps[G.active];

let usingLootWeapon=!!p.equippedLootWeapon;

let w=usingLootWeapon
? p.equippedLootWeapon
: {
    name:p.weapon,
    val:p.weaponDamage,
    ammoType:null,
    durability:Infinity,
    maxDurability:Infinity
  };
// LOOT WEAPON CHECKS
if(usingLootWeapon){

  // Stop broken weapons from being used
  if(w.durability<=0){
    log(`🔧 ${w.name} is BROKEN! Use a Repair Kit before attacking.`,"bad");
    return;
  }

  // Check firearm ammo
  if(w.ammoType && w.ammoType!=="melee"){

    if((G.ammo[w.ammoType]||0)<=0){

      log(
        `🔫 ${w.name} is out of ${w.ammoType.toUpperCase()} ammo!`,
        "bad"
      );

      return;
    }
  }
}
useCombatAction(1,()=>{
// USE AMMO + DURABILITY
if(usingLootWeapon){

  // Firearms consume 1 round
  if(w.ammoType && w.ammoType!=="melee"){
    G.ammo[w.ammoType]--;
  }

  // Every loot weapon loses 1 durability
  w.durability--;

  log(
    `🔧 ${w.name} durability: ${w.durability}/${w.maxDurability}`
  );

  if(w.durability<=0){
    log(
      `💥 ${w.name} has BROKEN and needs a Repair Kit!`,
      "bad"
    );
  }
}
let r=d6();

log(`Attack roll: ${r}`);

if(r<=3){
log("Your attack misses.","bad");
}
else{

let dmg=w.val+(r===6?3:0);
  // WEAK STATUS — 30% less attack damage
if(p.weak){

  let originalDamage=dmg;

  dmg=Math.max(1,Math.floor(dmg*0.70));

  log(
    `⚠️ WEAK! ${p.name}'s attack is reduced from ${originalDamage} to ${dmg} damage.`,
    "bad"
  );
}
  // BLACKWOOD SENTINEL — ANCIENT GUARD
// First successful attack each combat deals 50% less damage
if(
  combat.name==="The Blackwood Sentinel" &&
  !combat.ancientGuardUsed
){
  let originalDamage=dmg;

  dmg=Math.max(1,Math.floor(dmg*0.50));
  combat.ancientGuardUsed=true;

  log(
    `🛡️ ANCIENT GUARD! The Blackwood Sentinel reduces the first attack from ${originalDamage} to ${dmg} damage.`,
    "bad"
  );
}
// THE ROTTER — 20% chance to reduce incoming damage by 1
if(combat.name==="The Rotter" && Math.random()<0.20){

  dmg=Math.max(0,dmg-1);

  log(
    `🧟 ROTTING GRIP! The Rotter reduces the attack damage by 1.`,
    "bad"
  );
}
// THE HOLLOW — VOID SHIELD absorbs damage first
if(
  combat.name==="The Hollow" &&
  combat.voidShield>0
){
  let absorbed=Math.min(dmg,combat.voidShield);

  combat.voidShield-=absorbed;
  dmg-=absorbed;

  log(
    `🛡️ VOID SHIELD absorbs ${absorbed} damage! ${combat.voidShield} Shield remains.`,
    "bad"
  );

  if(combat.voidShield<=0){
    log(
      `💥 The Hollow's VOID SHIELD SHATTERS!`,
      "good"
    );
  }
}

// Any remaining damage hits The Hollow normally
combat.hp-=dmg;
  // THE HOLLOW — LAST RESPONSE against normal attacks
if(
  combat.name==="The Hollow" &&
  combat.hp<=0 &&
  !combat.lastStandUsed
){
  combat.lastStandUsed=true;

  combat.hp=Math.ceil(combat.maxHp*0.30);
  combat.atk=Math.ceil(combat.atk*1.55);

  combat.voidShieldActivated=true;
  combat.voidShield=15;

  log(
    `👁️ LAST RESPONSE! The Hollow refuses to die! It restores 30% HP, gains +55% Attack Damage, and summons a 15-point Void Shield!`,
    "bad"
  );
}
  // THE HOLLOW — activate Void Shield once at 50% HP
if(
  combat.name==="The Hollow" &&
  combat.hp<=combat.maxHp*0.50 &&
  !combat.voidShieldActivated
){
  combat.voidShieldActivated=true;
  combat.voidShield=15;

  log(
   `🛡️ VOID SHIELD! The Hollow surrounds itself in a dark barrier that can absorb 15 damage!`,
    "bad"
  );
}
combat.provoked=true;
log(`You hit ${combat.name} with ${w.name} for ${dmg} damage.`,"good");
chargeSpecial(p);
  // THE MIMIC — 25% chance to imitate 50% of damage received
if(
  combat.name==="The Mimic" &&
  combat.hp>0 &&
  Math.random()<0.25
){
  let mimicDamage=Math.max(1,Math.floor(dmg*0.50));

  p.hp-=mimicDamage;

  log(
    `🎭 PERFECT IMITATION! The Mimic copies your attack and deals ${mimicDamage} damage back to ${p.name}!`,
    "bad"
  );

  check(p,combat);
}
// THE GRAVEBORN — 25% chance to survive a killing blow with 1 HP
if(
  combat.name==="The Graveborn" &&
  combat.hp<=0 &&
  Math.random()<0.25
){
  combat.hp=1;

  log(
    `💀 GRAVE RESILIENCE! The Graveborn refuses to die and survives with 1 HP!`,
    "bad"
  );
}
  if(combat.hp<=0){

log(`${combat.name} is defeated!`,"good");
    if(combat.name==="The Root of Blackwood"){
  G.rootDefeated=true;

  log(
    `🌑 OBJECTIVE COMPLETE! The Root of Blackwood has been destroyed.`,
    "good"
  );

  updateStoryObjective();
}
if(combat.name==="The Bloodkeeper"){
  G.bloodkeeperDefeated=true;

  log(
    `🩸 STORY BOSS DEFEATED! The Bloodkeeper has fallen.`,
    "good"
  );

  if(!G.storyItems.includes("Bloodkeeper Relic")){
    G.storyItems.push("Bloodkeeper Relic");

    log(
      `🔑 STORY ITEM ACQUIRED: Bloodkeeper Relic`,
      "good"
    );  }

  updateStoryObjective();
}
 if(combat.name==="The Blackwood Sentinel"){
  G.sentinelDefeated=true;

  log(
    `🛡️ STORY BOSS DEFEATED! The Blackwood Sentinel has fallen.`,
    "good"
  );

  if(!G.storyItems.includes("Sentinel Relic")){
    G.storyItems.push("Sentinel Relic");

    log(
      `🔑 STORY ITEM ACQUIRED: Sentinel Relic`,
      "good"
    );
  }

  updateStoryObjective();
}
 if(combat.name==="The Warden"){
  G.wardenDefeated=true;

  log(
    `⛓️ STORY BOSS DEFEATED! The Warden has fallen.`,
    "good"
  );

  if(
    G.wardenDefeated &&
    G.hollowDefeated &&
    !G.storyItems.includes("Warden-Hollow Relic")
  ){
    G.storyItems.push("Warden-Hollow Relic");

  log(
  `🔑 STORY ITEM ACQUIRED: Warden-Hollow Relic`,
  "good"
);
}

  updateStoryObjective();
}

if(combat.name==="The Hollow"){
  G.hollowDefeated=true;

  log(
    `👁️ STORY BOSS DEFEATED! The Hollow has fallen.`,
    "good"
  );

  if(
    G.wardenDefeated &&
    G.hollowDefeated &&
    !G.storyItems.includes("Warden-Hollow Relic")
  ){
    G.storyItems.push("Warden-Hollow Relic");

log(
  `🔑 STORY ITEM ACQUIRED: Warden-Hollow Relic`,
  "good"
);
}

  updateStoryObjective();
}
    if(combat.name==="The Root of Blackwood"){
  G.rootDefeated=true;

  log(
    `🌑 FINAL BOSS DEFEATED! The Root of Blackwood has fallen.`,
    "good"
  );
}
G.creatures=G.creatures.filter(c=>c!==combat);
G.ps.forEach(s=>{

    if(s.dead)return;

    // Restore normal stats after Berserk
    s.maxHp=s.baseMaxHp;
    s.weaponDamage=s.baseWeaponDamage;
  s.hp=Math.min(s.hp,s.maxHp);
    s.berserk=false;
    s.berserkUsedThisBattle=false;
    s.berserkSpecialBoostReady=false;
if(s.rarity==="Legendary" || s.rarity==="G.O.A.T"){
    s.lifeRestoreReady=true;
}
    // Wake up knocked-out survivors after battle
    s.knockedOut=false;

    // If below 15% HP, recover to 75%
    if(s.hp < s.maxHp*0.15){
        s.hp=Math.ceil(s.maxHp*0.75);

        log(
            `❤️ ${s.name} feels better after resting and recovers to 75% HP.`,
            "good"
        );
    }
});
  G.ps.forEach(s=>{
  s.combatActions=0;
});
combat=null;
return;
}
}



});
}

function flee(){

if(!combat)return;

useCombatAction(1,()=>{
let p=G.ps[G.active];
let r=d6();

if(r<=2){

p.fear++;

log("You fail to escape. Gain 1 Fear.","bad");

creatureAttack(combat);

}
else{

let exits=LM[p.loc][2];

let escapeLoc=rnd(exits);

// Move the entire surviving party together
G.ps.forEach(s=>{
  if(!s.dead){
    s.loc=escapeLoc;
  }
});

G.discovered.add(escapeLoc);

log(`The party escapes to ${LM[escapeLoc][1]}.`,"good");
G.ps.forEach(s=>{
  s.combatActions=0;
});
combat=null;
}

});
}

function creatureAttack(c){

  let p=G.ps[G.active];

  let damage=c.atk;

  // Fear bonus
  if(p.fear>=4){
    damage++;
  }
  // ===============================
// MYTHIC — THE WARDEN
// ===============================

// Re-enable handcuffs after The Warden loses 35% Max HP
if(
  c.name==="The Warden" &&
  c.handcuffActive &&
  c.handcuffCooldownHp!==null &&
  c.hp<=c.handcuffCooldownHp
){
  c.handcuffActive=false;

  log(
    `⛓️ The Warden's restraints are ready again!`,
    "bad"
  );
}

// PRISONER'S RESTRAINT — handcuff wounded Survivor for 3 turns
if(
  c.name==="The Warden" &&
  p.hp>0 &&
  p.hp<p.maxHp*0.40 &&
  p.handcuffedTurns===0 &&
  !c.handcuffActive
){
  p.handcuffedTurns=3;

  c.handcuffActive=true;
  c.handcuffCooldownHp=Math.max(
    0,
    c.hp-(c.maxHp*0.35)
  );

  log(
    `⛓️ PRISONER'S RESTRAINT! The Warden handcuffs ${p.name}! They will lose their next 3 turns.`,
    "bad"
  );
}
  // PRISONER'S JUDGMENT — punish wounded Survivors
if(
  c.name==="The Warden" &&
  p.hp<=p.maxHp*0.50 &&
  Math.random()<0.40
){
  damage+=5;

  log(
    `⚖️ PRISONER'S JUDGMENT! The Warden punishes ${p.name} for being wounded and gains +5 damage!`,
    "bad"
  );
}
  // ===============================
// LEGENDARY — THE BLOODKEEPER
// ===============================

// BLOOD TRIBUTE — 35% chance to restore 3 HP when attacking
if(
  c.name==="The Bloodkeeper" &&
  c.hp>0 &&
  c.hp<c.maxHp &&
  Math.random()<0.35
){
  let oldHp=c.hp;

  c.hp=Math.min(c.maxHp,c.hp+3);

  let healed=c.hp-oldHp;

  log(
    `🩸 BLOOD TRIBUTE! The Bloodkeeper restores ${healed} HP.`,
    "bad"
  );
}
  // ===============================
// ANCIENT — THE HOLLOW
// ===============================

// VOID CONSUMPTION — 35% chance to drain 2 Combat Actions
if(
  c.name==="The Hollow" &&
Math.random()<0.35
){
  let drained=Math.min(2,p.combatActions);

  p.combatActions=Math.max(0,p.combatActions-drained);

  log(
    `🕳️ VOID CONSUMPTION! The Hollow drains ${drained} Combat Actions from ${p.name}!`,
    "bad"
  );
}
// ===============================
// RARE CREATURE ABILITIES
// ===============================

// THE STALKER — 30% chance for +2 damage once provoked
if(
  c.name==="The Stalker" &&
  c.provoked &&
  Math.random()<0.30
){
  damage+=2;

  log(
    `👁️ RELENTLESS PURSUIT! The Stalker gains +2 damage!`,
    "bad"
  );
}
  // THE BUTCHER — 30% chance for +3 damage against wounded Survivors
if(
  c.name==="The Butcher" &&
  p.hp<=p.maxHp*0.50 &&
  Math.random()<0.30
){
  damage+=3;

  log(
    `🔪 BLOOD FRENZY! The Butcher smells blood and gains +3 damage!`,
    "bad"
  );
}
  // ===============================
// EPIC CREATURE ABILITIES
// ===============================

// THE CRAWLING MAN — 35% chance for +3 damage
if(
  c.name==="The Crawling Man" &&
  Math.random()<0.35
){
  damage+=3;

  log(
    `🕷️ UNNATURAL REACH! The Crawling Man strikes from an impossible angle for +3 damage!`,
    "bad"
  );
}
  // THE WENDIGO — gets stronger as its HP gets lower
if(c.name==="The Wendigo"){

  if(c.hp<=c.maxHp*0.25){
    damage+=4;

    log(
      `🦌 PREDATOR'S HUNGER! The Wendigo is near death and gains +4 damage!`,
      "bad"
    );
  }

  else if(c.hp<=c.maxHp*0.50){
    damage+=2;

    log(
      `🦌 PREDATOR'S HUNGER! The Wendigo becomes more aggressive and gains +2 damage!`,
      "bad"
    );
  }
}
  // ===============================
  // COMMON CREATURE ABILITIES
  // ===============================

  // THE DRIFTER — 20% chance for +1 damage
  if(c.name==="The Drifter" && Math.random()<0.20){
    damage+=1;

    log(
      `🩸 DESPERATE LUNGE! The Drifter deals +1 bonus damage.`,
      "bad"
    );
  }

  // Deal HP damage
  p.hp-=damage;

  log(
    `👹 COUNTER-ATTACK! ${c.name} attacks ${p.name} for ${damage} damage!`,
    "bad"
  );
// THE NIGHT HAG — 30% chance to drain Sanity and increase Fear
if(c.name==="The Night Hag" && Math.random()<0.30){

  p.san=Math.max(0,p.san-1);
  p.fear=Math.min(5,p.fear+1);

  log(
    `🌙 NIGHTMARE TOUCH! ${p.name} loses 1 Sanity and gains 1 Fear.`,
    "bad"
  );
}
  // THE PALE BRIDE — 35% chance to curse the entire party
if(c.name==="The Pale Bride" && Math.random()<0.35){

  p.san=Math.max(0,p.san-2);
  p.fear=Math.min(5,p.fear+1);

  G.ps.forEach(s=>{
    if(!s.dead && s!==p){
      s.fear=Math.min(5,s.fear+1);
    }
  });

  log(
    `👰 MOURNING CURSE! ${p.name} loses 2 Sanity and gains 1 Fear. The rest of the party gains 1 Fear.`,
    "bad"
  );
}
  // THE WHISPERER — 20% chance to drain 1 Sanity
  if(c.name==="The Whisperer" && Math.random()<0.20){
    p.san=Math.max(0,p.san-1);

    log(
      `👻 WHISPERS OF FEAR! ${p.name} loses 1 Sanity.`,
      "bad"
    );
  }

  // THE WEEPER — 20% chance to add 1 Fear
  if(c.name==="The Weeper" && Math.random()<0.20){
    p.fear=Math.min(5,p.fear+1);

    log(
      `😭 DISTURBING CRIES! ${p.name} gains 1 Fear.`,
      "bad"
    );
  }
// ===============================
// UNCOMMON CREATURE ABILITIES
// ===============================

// THE SCREECHER — 25% chance to drain 1 Sanity
if(c.name==="The Screecher" && Math.random()<0.25){

  p.san=Math.max(0,p.san-1);

  log(
    `📢 PIERCING SCREAM! ${p.name} loses 1 Sanity.`,
    "bad"
  );
}
 // THE SKINWALKER — 25% chance to confuse and add 1 Fear
if(c.name==="The Skinwalker" && Math.random()<0.25){

  p.fear=Math.min(5,p.fear+1);

  log(
    `🎭 FALSE FACE! ${p.name} becomes confused and gains 1 Fear.`,
    "bad"
  );
}
  check(p,c);
}

function activateBerserk(p){

  p.berserk=true;
  p.berserkUsedThisBattle=true;
  p.berserkSpecialBoostReady=true;

  p.maxHp=p.baseMaxHp+10;
  p.weaponDamage=p.baseWeaponDamage+8;

  p.hp=p.maxHp;
  p.knockedOut=false;

  log(
    `🔥 ${p.name} ENTERS BERSERK MODE! +10 Max HP, +8 Attack, and their next Special gains +55% damage!`,
    "good"
  );

  render();
}

function check(p,killer=null){

if(p.hp<=0){

  p.hp=0;
  // LEGENDARY / G.O.A.T BERSERK
if(
  (p.rarity==="Legendary" || p.rarity==="G.O.A.T")
  && !p.berserkUsedThisBattle
){
  activateBerserk(p);
  return;
}

  // G.O.A.T characters can never permanently die
if(p.rarity==="G.O.A.T"){

  p.hp=0;
  p.knockedOut=true;

  log(
    `🐐 ${p.name} cannot be killed! They are KNOCKED OUT but lose no Lives.`,
    "good"
  );

  return;
}

  // Lose one life
  p.lives=Math.max(0,p.lives-1);

  if(p.lives>0){

    p.knockedOut=true;
// THE BONE COLLECTOR — gains +2 Attack when it knocks out a Survivor
if(killer && killer.name==="The Bone Collector"){

  killer.atk+=2;

  log(
    `💀 HARVEST THE FALLEN! The Bone Collector grows stronger and gains +2 Attack!`,
    "bad"
  );
}
    log(
      `💀 ${p.name} has been KNOCKED OUT! ${p.lives}/${p.maxLives} Lives remain.`,
      "bad"
    );
  switchCombatSurvivor();
    return;
  
  }

  // Final life lost
  p.dead=true;
  p.knockedOut=true;

  log(
    `☠️ ${p.name} has lost their FINAL LIFE!`,
    "bad"
  );
  if(killer){

    killer.maxHp+=10;
    killer.hp=Math.min(killer.maxHp,killer.hp+10);
    killer.atk+=5;

    log(
        `👹 ${killer.name} DEVOURS ${p.name}! +10 Max HP and +5 Attack!`,
        "bad"
    );
}
switchCombatSurvivor();
return;
}
if(p.san<=0){

p.san=1;
p.fear=Math.min(5,p.fear+2);

log(`${p.name} BREAKS. Gain 2 Fear.`,"bad");
}
}

function switchCombatSurvivor(){

  if(!combat)return false;

  for(let step=1;step<=G.ps.length;step++){

    let next=(G.active+step)%G.ps.length;
    let survivor=G.ps[next];

    if(!survivor.dead && !survivor.knockedOut && survivor.hp>0){

      G.active=next;
   survivor.combatActions=combatActionCount(survivor);

      log(
        `⚔️ ${survivor.name} steps forward to continue the battle!`,
        "good"
      );

      render();
      return true;
    }
  }

  partyDefeated();
return false;
}

function partyDefeated(){

    log(`☠️ THE ENTIRE PARTY HAS FALLEN...`, "bad");
    log(`🏚️ The survivors awaken back at the Riverside Motel.`, "good");

    // End the current combat
    combat=null;

    // Recover every survivor and return them to the motel
    G.ps.forEach(p=>{

      if(p.dead)return;
        p.knockedOut=false;

        // Restore HP and sanity
       p.hp=Math.ceil(p.maxHp*0.75);
        p.san=Math.max(1,p.san);

        // Return survivor to Riverside Motel
        p.loc="motel";

        // Reset combat states
        p.fear=0;
        p.enemyStunned=false;
        p.berserk=false;
        p.berserkUsedThisBattle=false;
        p.berserkSpecialBoostReady=false;
p.maxHp=p.baseMaxHp;
p.weaponDamage=p.baseWeaponDamage;
      // Lose one random regular item
if(p.items && p.items.length>0){
    let lostIndex=Math.floor(Math.random()*p.items.length);
    let lostItem=p.items.splice(lostIndex,1)[0];

    log(`🎒 ${p.name} lost ${lostItem.name} while escaping back to the motel.`, "bad");
}
        // Reset actions
        p.actions=15;
      p.combatActions=0;
    });

    // Return control to first survivor
    G.active=0;

    log(`🔥 The party survived... but Blackwood has taken its toll.`, "bad");

    render();
}

function useSpecial(){

  if(!combat)return;

  let p=G.ps[G.active];
// Special must be fully charged first
if(p.specialCharge<100){
  log(`⚡ ${p.name}'s Special Ability is only ${p.specialCharge}% charged.`,"bad");
  return;
}

// Must have 3 Combat AP
if(p.combatActions<3){
  log(`⚡ ${p.name} needs 3 Combat AP to use their Special Ability.`,"bad");
  return;
}

// Charge the 3 AP ONLY when the Special can actually be used
p.combatActions-=3;

  let dmg=Math.ceil(p.weaponDamage*1.5);

  if(p.rarity==="G.O.A.T" && p.specialUses===0){
    dmg=Math.ceil(dmg*1.25);
    log(`🐐 G.O.A.T BONUS! ${p.name}'s first Special deals 25% extra damage!`,"good");
  }
if(p.berserkSpecialBoostReady){
    dmg=Math.ceil(dmg*1.55);
    p.berserkSpecialBoostReady=false;

    log(
        `🔥 BERSERK SPECIAL! ${p.name}'s Special gains +55% damage!`,
        "good"
    );
}
  // THE HOLLOW — SPECIAL ATTACKS MUST HIT VOID SHIELD FIRST
if(
  combat.name==="The Hollow" &&
  combat.voidShield>0
){
  let absorbed=Math.min(dmg,combat.voidShield);

  combat.voidShield-=absorbed;
  dmg-=absorbed;

  log(
    `🛡️ VOID SHIELD absorbs ${absorbed} Special damage! ${combat.voidShield} Shield remains.`,
    "bad"
  );

  if(combat.voidShield<=0){
    log(
      `💥 The Hollow's VOID SHIELD SHATTERS!`,
      "good"
    );
  }
}

// Any remaining Special damage hits The Hollow
combat.hp-=dmg;
  // THE HOLLOW — activate Void Shield once at 50% HP
if(
  combat.name==="The Hollow" &&
  combat.hp>0 &&
combat.hp<=combat.maxHp*0.50 &&
  !combat.voidShieldActivated
){
  combat.voidShieldActivated=true;
  combat.voidShield=15;

  log(
    `🛡️ VOID SHIELD! The Hollow surrounds itself in a dark barrier that can absorb 15 damage!`,
    "bad"
  );
}
combat.provoked=true;
  log(`⚡ ${p.name} unleashes ${p.ability} for ${dmg} damage!`,"good");

  p.specialCharge=0;
  p.specialUses++;
if(combat.hp<=0){
  log(`${combat.name} is destroyed by the Special Ability!`,"good");
if(combat.name==="The Warden"){
  G.wardenDefeated=true;

  log(
    `⛓️ STORY BOSS DEFEATED! The Warden has fallen.`,
    "good"
  );

  if(
    G.wardenDefeated &&
    G.hollowDefeated &&
    !G.storyItems.includes("Warden-Hollow Relic")
  ){
    G.storyItems.push("Warden-Hollow Relic");

    log(
      `🔑 STORY ITEM ACQUIRED: Warden-Hollow Relic`,
      "good"
    );
  }
}

if(combat.name==="The Hollow"){
  G.hollowDefeated=true;

  log(
    `👁️ STORY BOSS DEFEATED! The Hollow has fallen.`,
    "good"
  );

  if(
    G.wardenDefeated &&
    G.hollowDefeated &&
    !G.storyItems.includes("Warden-Hollow Relic")
  ){
    G.storyItems.push("Warden-Hollow Relic");

    log(
      `🔑 STORY ITEM ACQUIRED: Warden-Hollow Relic`,
      "good"
    );
  }
}
if(combat.name==="The Bloodkeeper"){
  G.bloodkeeperDefeated=true;

  log(
    `🩸 STORY BOSS DEFEATED! The Bloodkeeper has fallen.`,
    "good"
  );

  if(!G.storyItems.includes("Bloodkeeper Relic")){
    G.storyItems.push("Bloodkeeper Relic");

    log(
      `🔑 STORY ITEM ACQUIRED: Bloodkeeper Relic`,
      "good"
    );
  }
}

if(combat.name==="The Blackwood Sentinel"){
  G.sentinelDefeated=true;

  log(
    `🛡️ STORY BOSS DEFEATED! The Blackwood Sentinel has fallen.`,
    "good"
  );

  if(!G.storyItems.includes("Sentinel Relic")){
    G.storyItems.push("Sentinel Relic");

    log(
      `🔑 STORY ITEM ACQUIRED: Sentinel Relic`,
      "good"
    );
  }
}
    if(combat.name==="The Root of Blackwood"){
  G.rootDefeated=true;

  log(
    `🌑 FINAL BOSS DEFEATED! The Root of Blackwood has fallen.`,
    "good"
  );
}

updateStoryObjective();

G.creatures=G.creatures.filter(c=>c!==combat);
  G.ps.forEach(s=>{

    if(s.dead)return;

    // Restore normal stats after Berserk
    s.maxHp=s.baseMaxHp;
    s.weaponDamage=s.baseWeaponDamage;
    s.hp=Math.min(s.hp,s.maxHp);

    s.berserk=false;
    s.berserkUsedThisBattle=false;
    s.berserkSpecialBoostReady=false;
    if(s.rarity==="Legendary" || s.rarity==="G.O.A.T"){
    s.lifeRestoreReady=true;
}

    // Wake up knocked-out survivors after battle
    s.knockedOut=false;

    // If below 15% HP, recover to 75%
    if(s.hp < s.maxHp*0.15){
        s.hp=Math.ceil(s.maxHp*0.75);

        log(
            `❤️ ${s.name} feels better after resting and recovers to 75% HP.`,
            "good"
        );
    }
});
G.ps.forEach(s=>{
  s.combatActions=0;
});
combat=null;
  }

  render();
}
