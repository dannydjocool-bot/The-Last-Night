/* The Last Night — inventory system. Extracted during architecture refactor; gameplay behavior preserved. */

function gainItem(){

let p=G.ps[G.active];

let i=objItem(rnd(ITEMS));

// AMMO PICKUPS
if(i.type==="ammo"){

  G.ammo[i.ammoType]+=i.val;

  log(
    `🔫 Found <b>${i.name}</b>! +${i.val} rounds.`,
    "good"
  );

  return;
}

// PERSONAL INVENTORY HAS ROOM
if(p.items.length<4){

  p.items.push(i);

  log(
    `🎒 Found <b>${i.name}</b> and stored it in ${p.name}'s inventory.`,
    "good"
  );

  return;
}

// PERSONAL INVENTORY FULL → EXTRA POCKETS
if(G.extraPockets.length<G.extraPocketMax){

  G.extraPockets.push(i);

  log(
    `🎒 Personal inventory full — <b>${i.name}</b> was stored in Extra Pockets (${G.extraPockets.length}/${G.extraPocketMax}).`,
    "good"
  );

  return;
}

// BOTH INVENTORIES FULL
log(
  `❌ Inventory and Extra Pockets are full. ${i.name} was left behind.`,
  "bad"
);

}

function useItem(i){

let p=G.ps[G.active];
let it=p.items[i];

if(!it)return;

if(it.type==="heal"){

p.hp=Math.min(p.maxHp,p.hp+it.val);

log(`${p.name} uses ${it.name} and restores ${it.val} Health.`,"good");

p.items.splice(i,1);

}
else if(it.type==="healweak"){

  let oldHp=p.hp;

  p.hp=Math.min(p.maxHp,p.hp+it.val);
  p.weak=false;

  log(
    `🧪 ${p.name} uses ${it.name}, restores ${p.hp-oldHp} Health, and removes the WEAK status!`,
    "good"
  );

  p.items.splice(i,1);
}
else if(it.type==="san"){

p.san=Math.min(10,p.san+it.val);

log(`${p.name} regains ${it.val} Sanity.`,"good");

p.items.splice(i,1);

}
else if(it.type==="fear"){

p.fear=Math.max(0,p.fear-it.val);

log(`${p.name} reduces Fear.`,"good");

p.items.splice(i,1);

}
else if(it.type==="key"){

let locked=L.find(x=>!G.discovered.has(x[0]));

if(locked){

G.discovered.add(locked[0]);

log(`The Rusty Key reveals ${locked[1]}.`,"good");

}

p.items.splice(i,1);
}
else if(it.type==="weapon"){

  // Equip the found weapon
  p.equippedLootWeapon=it;

  log(
    `⚔️ ${p.name} equips ${it.name}.`,
    "good"
  );
}
else if(it.type==="repair"){

  let weapon=p.equippedLootWeapon;

  // No loot weapon equipped
  if(!weapon){
    log(
      `🔧 ${p.name} has no loot weapon equipped to repair.`,
      "bad"
    );
    return;
  }

  // Weapon cannot be repaired
  if(weapon.maxDurability===undefined){
    log(
      `🔧 ${weapon.name} cannot be repaired.`,
      "bad"
    );
    return;
  }

  // Already full durability
  if(weapon.durability>=weapon.maxDurability){
    log(
      `🔧 ${weapon.name} is already at full durability.`,
      "bad"
    );
    return;
  }

  // Repair weapon
  weapon.durability=weapon.maxDurability;

  // Consume Repair Kit
  p.items.splice(i,1);

  log(
    `🔧 ${p.name} repairs ${weapon.name} to ${weapon.durability}/${weapon.maxDurability} durability!`,
    "good"
  );

}
else{

  log(`${it.name} has no active effect right now.`);
}

render();
}

function switchToSignatureWeapon(index){

  let p=G.ps[index];

  if(!p)return;

  // Return equipped loot weapon to Extra Pockets first
  if(p.equippedLootWeapon){

    if(G.extraPockets.length>=G.extraPocketMax){
      log(
        `🎒 Extra Pockets are full! Cannot switch to Signature Weapon.`,
        "bad"
      );
      return;
    }

    G.extraPockets.push(p.equippedLootWeapon);

    log(
      `🎒 ${p.equippedLootWeapon.name} returned to Extra Pockets.`,
      "good"
    );

    p.equippedLootWeapon=null;
  }

  log(
    `⚔️ ${p.name} switches back to ${p.weapon}.`,
    "good"
  );

  render();
}

function equipExtraPocketWeapon(index){

  let p=G.ps[G.active];
  let weapon=G.extraPockets[index];

  if(!p || !weapon)return;

  // Make sure the selected item is actually a weapon
  if(weapon.type!=="weapon"){
    log(`❌ ${weapon.name} is not a weapon.`,"bad");
    return;
  }

  // Don't equip a broken weapon
  if(
    weapon.maxDurability!==undefined &&
    weapon.durability<=0
  ){
    log(
      `🔧 ${weapon.name} is BROKEN! Repair it before equipping.`,
      "bad"
    );
    return;
  }

  // Save the selected weapon
  let selectedWeapon=weapon;

  // Remove selected weapon from Extra Pockets first
  G.extraPockets.splice(index,1);

  // Return currently equipped loot weapon to Extra Pockets
  if(p.equippedLootWeapon){

    G.extraPockets.push(p.equippedLootWeapon);

    log(
      `🎒 ${p.equippedLootWeapon.name} returned to Extra Pockets.`,
      "good"
    );
  }

  // Equip the selected weapon
  p.equippedLootWeapon=selectedWeapon;

  render();
}

function useExtraPocketItem(index){

  let p=G.ps[G.active];
  let item=G.extraPockets[index];

  if(!p || !item)return;

  // Weapons must use EQUIP
  if(item.type==="weapon"){
    log(`❌ Use the EQUIP button for ${item.name}.`,"bad");
    return;
  }

  // HEAL ITEM
  if(item.type==="heal"){

    p.hp=Math.min(p.maxHp,p.hp+item.val);

    log(
      `❤️ ${p.name} uses ${item.name} and restores ${item.val} Health.`,
      "good"
    );

    G.extraPockets.splice(index,1);
  }

  // SANITY ITEM
  else if(item.type==="san"){

    p.san=Math.min(p.maxSan,p.san+item.val);

    log(
      `🧠 ${p.name} uses ${item.name} and restores ${item.val} Sanity.`,
      "good"
    );

    G.extraPockets.splice(index,1);
  }

  // FEAR ITEM
  else if(item.type==="fear"){

    p.fear=Math.max(0,p.fear-item.val);

    log(
      `😨 ${p.name} uses ${item.name} and reduces Fear by ${item.val}.`,
      "good"
    );

    G.extraPockets.splice(index,1);
  }

  // KEY ITEM
  else if(item.type==="key"){

    let locked=L.find(x=>!G.discovered.has(x[0]));

    if(locked){

      G.discovered.add(locked[0]);

      log(
        `🗝️ ${item.name} reveals ${locked[1]}.`,
        "good"
      );

      G.extraPockets.splice(index,1);
    }
    else{

      log(
        `🗝️ There are no locked locations left to reveal.`,
        "bad"
      );

      return;
    }
  }

  // REPAIR KIT
  else if(item.type==="repair"){

    let weapon=p.equippedLootWeapon;

    if(!weapon){
      log(
        `🔧 ${p.name} has no loot weapon equipped to repair.`,
        "bad"
      );
      return;
    }

    if(weapon.maxDurability===undefined){
      log(
        `🔧 ${weapon.name} cannot be repaired.`,
        "bad"
      );
      return;
    }

    if(weapon.durability>=weapon.maxDurability){
      log(
        `🔧 ${weapon.name} is already at full durability.`,
        "bad"
      );
      return;
    }

    weapon.durability=weapon.maxDurability;

    G.extraPockets.splice(index,1);

    log(
      `🔧 ${p.name} repairs ${weapon.name} to ${weapon.durability}/${weapon.maxDurability} durability!`,
      "good"
    );
  }

  // TOOL — not implemented yet
  else if(item.type==="tool"){

    log(
      `🛠️ ${item.name} does not have an active effect yet.`,
      "bad"
    );

    return;
  }

  else{

    log(
      `❌ ${item.name} cannot be used right now.`,
      "bad"
    );

    return;
  }

  render();
}

function restoreLives(targetIndex){
  let healer=G.ps[G.active];
    let target=G.ps[targetIndex];

    if(!healer || !target)return;

    if(healer.rarity!=="Legendary" && healer.rarity!=="G.O.A.T"){
        log(`❌ ${healer.name} cannot restore Lives.`,"bad");
        return;
    }

    if(!healer.lifeRestoreReady){
        log(`❌ ${healer.name}'s Life Restore is not ready.`,"bad");
        return;
    }

    if(target.dead){
        log(`☠️ ${target.name} is permanently dead and cannot be revived.`,"bad");
        return;
    }

    if(target.rarity==="G.O.A.T"){
        log(`🐐 ${target.name} already has unlimited Lives.`,"bad");
        return;
    }

    if(target.lives>=target.maxLives){
        log(`❤️ ${target.name} already has maximum Lives.`,"bad");
        return;
    }

    let before=target.lives;

    target.lives=Math.min(target.maxLives,target.lives+2);

    healer.lifeRestoreReady=false;

    log(
        `✨ ${healer.name} restores ${target.name} from ${before}/${target.maxLives} to ${target.lives}/${target.maxLives} Lives!`,
        "good"
    );

    render();
}
