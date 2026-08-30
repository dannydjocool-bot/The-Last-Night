from pathlib import Path

path = Path('index.html')
text = path.read_text()

def replace(old, new, count=None):
    global text
    found = text.count(old)
    if count is not None and found != count:
        raise SystemExit(f'Expected {count} matches, found {found}: {old[:100]!r}')
    if found == 0:
        raise SystemExit(f'Pattern not found: {old[:100]!r}')
    text = text.replace(old, new)

# Transformation definitions and player-facing copy.
replace('ability:"Lunar Curse — Freely transform into The Eclipse Beast during testing.",isNew:true,transformKey:"moonbound",transform:{',
        'ability:"Lunar Curse — Transform into The Eclipse Beast during combat at 35% HP or lower.",isNew:true,transformKey:"moonbound",transformThreshold:0.35,transform:{', 1)
replace('ability:"Martyr Flame — Freely transform into The Burning Seraph during testing.",isNew:true,transformKey:"ashen",transform:{',
        'ability:"Martyr Flame — Transform into The Burning Seraph during combat at 40% HP or lower.",isNew:true,transformKey:"ashen",transformThreshold:0.40,transform:{', 1)
replace('Click either card to reveal its unrestricted test transformation and improved stats.',
        'Click either card to preview its low-health combat transformation and improved stats.', 1)
replace('NEW G.O.A.T survivors The Moonbound and The Ashen Saint can freely transform and revert during this test build.',
        'NEW G.O.A.T survivors unlock combat transformations at critical health: The Moonbound at 35% HP and The Ashen Saint at 40% HP.', 1)
replace('<b>Transform/Revert:</b> The Moonbound and The Ashen Saint currently shift forms freely with no cost, cooldown, or location restriction for testing.',
        '<b>Transform/Revert:</b> The Moonbound unlocks at 35% HP and The Ashen Saint at 40% HP during combat. Each transformation can trigger only once per encounter.', 1)

replace('transformKey:s.transformKey||null,\ntransformed:false,',
        'transformKey:s.transformKey||null,\ntransformThreshold:s.transformThreshold||null,\ntransformed:false,\ntransformationUsedThisCombat:false,', 1)

old_toggle = '''function toggleTransformation(index){
  const p=G&&G.ps[index];
  if(!p||p.dead||!p.transform)return;
  const t=p.transform;
  if(!p.transformed){
    p.transformed=true;
    p.name=t.name;
    p.image=t.image;
    p.maxHp=p.normalMaxHp+t.hpBonus;
    p.baseMaxHp=p.maxHp;
    p.hp=Math.min(p.maxHp,p.hp+t.hpBonus);
    p.weapon=t.weapon;
    p.weaponDamage=p.normalWeaponDamage+t.damageBonus;
    p.baseWeaponDamage=p.weaponDamage;
    p.weaponAbility=t.weaponAbility;
    p.ability=t.ability;
    p.maxShield=p.normalMaxShield+(t.shieldBonus||0);
    p.shield=Math.min(p.maxShield,(p.shield||0)+(t.shieldBonus||0));
    if(combat&&index===G.active)p.combatActions+=t.combatActionBonus||0;
    log(`✨ ${p.originalName} transforms into ${p.name}! Testing mode has no transformation restrictions.`,"good");
  }else{
    p.transformed=false;
    p.name=p.originalName;
    p.image=p.normalImage;
    p.maxHp=p.normalMaxHp;
    p.baseMaxHp=p.normalMaxHp;
    p.hp=Math.min(p.hp,p.maxHp);
    p.weapon=p.normalWeapon;
    p.weaponDamage=p.normalWeaponDamage;
    p.baseWeaponDamage=p.normalWeaponDamage;
    p.weaponAbility=p.normalWeaponAbility;
    p.ability=p.normalAbility;
    p.maxShield=p.normalMaxShield;
    p.shield=Math.min(p.shield||0,p.maxShield);
    log(`🌘 ${p.originalName} reverts to human form.`,"good");
  }
  showTransformationFlash(p);
  render();
}'''
new_toggle = '''function transformationThreshold(p){
  if(p.transformThreshold)return p.transformThreshold;
  return p.transformKey==="moonbound"?0.35:p.transformKey==="ashen"?0.40:0.40;
}

function revertTransformationState(p,announce=false){
  if(!p||!p.transformed)return;
  p.transformed=false;
  p.name=p.originalName;
  p.image=p.normalImage;
  p.maxHp=p.normalMaxHp;
  p.baseMaxHp=p.normalMaxHp;
  p.hp=Math.min(p.hp,p.maxHp);
  p.weapon=p.normalWeapon;
  p.weaponDamage=p.normalWeaponDamage;
  p.baseWeaponDamage=p.normalWeaponDamage;
  p.weaponAbility=p.normalWeaponAbility;
  p.ability=p.normalAbility;
  p.maxShield=p.normalMaxShield;
  p.shield=Math.min(p.shield||0,p.maxShield);
  if(announce)log(`🌘 ${p.originalName} returns to normal form.`,"good");
}

function resetCombatTransformations(){
  if(!G)return;
  G.ps.forEach(p=>{
    revertTransformationState(p,false);
    p.transformationUsedThisCombat=false;
  });
}

function toggleTransformation(index){
  const p=G&&G.ps[index];
  if(!p||p.dead||!p.transform)return;
  const t=p.transform;
  if(!p.transformed){
    if(!combat){
      log(`✨ ${p.originalName}'s transformation can only be activated during combat.`,"bad");
      return;
    }
    const threshold=transformationThreshold(p);
    if(p.hp>p.normalMaxHp*threshold){
      log(`✨ ${p.originalName} must fall to ${Math.round(threshold*100)}% HP or lower before transforming.`,"bad");
      return;
    }
    if(p.transformationUsedThisCombat){
      log(`✨ ${p.originalName} has already transformed during this encounter.`,"bad");
      return;
    }
    p.transformationUsedThisCombat=true;
    p.transformed=true;
    p.name=t.name;
    p.image=t.image;
    p.maxHp=p.normalMaxHp+t.hpBonus;
    p.baseMaxHp=p.maxHp;
    p.hp=Math.min(p.maxHp,p.hp+t.hpBonus);
    p.weapon=t.weapon;
    p.weaponDamage=p.normalWeaponDamage+t.damageBonus;
    p.baseWeaponDamage=p.weaponDamage;
    p.weaponAbility=t.weaponAbility;
    p.ability=t.ability;
    p.maxShield=p.normalMaxShield+(t.shieldBonus||0);
    p.shield=Math.min(p.maxShield,(p.shield||0)+(t.shieldBonus||0));
    if(index===G.active)p.combatActions+=t.combatActionBonus||0;
    log(`✨ ${p.originalName} transforms into ${p.name} at critical health!`,"good");
  }else{
    revertTransformationState(p,true);
  }
  showTransformationFlash(p);
  render();
}'''
replace(old_toggle, new_toggle, 1)

old_start = '''function startCombat(id){

if(combat){
  log(`You are already fighting ${combat.name}. Finish or flee from this encounter first.`,"bad");
  render();
  return;
}
combat=G.creatures.find(c=>String(c.id)===String(id));
  if(
  combat &&
  combat.name==="The Blackwood Sentinel"
){
  combat.ancientGuardUsed=false;
}
if(combat){
  let p=G.ps[G.active];
  log(`Combat begins against ${combat.name}.`,"bad");
  showCombatIntro(combat);
  p.combatActions=combatActionCount(p)+(p.originalName==="The Signalman"?1:0);
  combat.attacksSinceCounter=0;
  if(combat.firstStrike){
    combat.firstStrike=false;
    log(`⚡ ${combat.name} was ready and attacks before the survivors can act!`,"bad");
    creatureAttack(combat);
  }
}

render();
}'''
new_start = '''function startCombat(id){

if(combat){
  log(`You are already fighting ${combat.name}. Finish or flee from this encounter first.`,"bad");
  render();
  return;
}
resetCombatTransformations();
combat=G.creatures.find(c=>String(c.id)===String(id));
  if(
  combat &&
  combat.name==="The Blackwood Sentinel"
){
  combat.ancientGuardUsed=false;
}
if(combat){
  let p=G.ps[G.active];
  log(`Combat begins against ${combat.name}.`,"bad");
  showCombatIntro(combat);
  G.ps.forEach(s=>{
    if(s.dead||s.knockedOut||s.hp<=0){s.combatActions=0;return;}
    s.combatActions=combatActionCount(s)+(s.originalName==="The Signalman"?1:0);
    s.transformationUsedThisCombat=false;
  });
  combat.attacksSinceCounter=0;
  if(combat.firstStrike){
    combat.firstStrike=false;
    log(`⚡ ${combat.name} was ready and attacks before the survivors can act!`,"bad");
    creatureAttack(combat);
  }
}

render();
}'''
replace(old_start, new_start, 1)

replace('''    if(!survivor.dead && !survivor.knockedOut && survivor.hp>0){

      G.active=next;
   survivor.combatActions=combatActionCount(survivor);

      log(
        `⚔️ ${survivor.name} steps forward to continue the battle!`,
        "good"
      );

      render();
      return true;
    }''',
        '''    if(!survivor.dead && !survivor.knockedOut && survivor.hp>0 && survivor.combatActions>0){

      G.active=next;

      log(
        `⚔️ ${survivor.name} steps forward to continue the battle with ${survivor.combatActions} Combat AP!`,
        "good"
      );

      render();
      return true;
    }''', 1)

old_select = '''function selectSurvivor(index){

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
}'''
new_select = '''function selectSurvivor(index){

  if(!G)return;
  let survivor=G.ps[index];

  if(!survivor || survivor.dead || survivor.knockedOut || survivor.hp<=0){
    return;
  }

  if(combat){
    const outgoing=G.ps[G.active];
    if(index===G.active)return;
    if(outgoing.combatActions>0){
      log(`⚔️ ${outgoing.name} must spend all Combat AP before switching.`,"bad");
      return;
    }
    if(survivor.combatActions<=0){
      log(`⚔️ ${survivor.name} has no Combat AP left this round.`,"bad");
      return;
    }

    log(`🔄 ${outgoing.name} attempts to fall back. ${survivor.name} prepares to enter combat.`);
    if(Math.random()<0.30){
      log(`⚠️ ${combat.name} lunges at ${outgoing.name} during the swap!`,"bad");
      creatureAttack(combat);
      if(!combat)return;
      if(survivor.dead||survivor.knockedOut||survivor.hp<=0||survivor.combatActions<=0){render();return;}
    }else{
      log(`✅ ${outgoing.name} escapes the creature's reach.`,"good");
    }
    G.active=index;
    log(`⚔️ ${survivor.name} takes over with ${survivor.combatActions} Combat AP.`,"good");
    render();
    return;
  }

  G.active=index;
  log(`👤 ${survivor.name} is now selected.`,"good");
  render();
}'''
replace(old_select, new_select, 1)

replace('''<button ${combat?'disabled class="combat-locked" title="Survivors cannot be switched manually during combat"':''} onclick="selectSurvivor(${index})">
  👤 SELECT
</button>''',
        '''<button ${combat&&!(G.ps[G.active].combatActions<=0&&index!==G.active&&!sp.knockedOut&&sp.hp>0&&sp.combatActions>0)?'disabled class="combat-locked" title="Switching unlocks when the active survivor reaches 0 Combat AP"':''} onclick="selectSurvivor(${index})">
  ${combat&&index!==G.active?'🔄 SWITCH IN':'👤 SELECT'}
</button>''', 1)

replace('''${sp.transform?`<button onclick="toggleTransformation(${index})">${sp.transformed?'🌘 Revert to '+sp.originalName:'✨ Transform into '+sp.transform.name}</button><div class="muted">Testing: unrestricted transformation</div><br>`:''}''',
        '''${sp.transform?`<button ${!sp.transformed&&(!combat||sp.transformationUsedThisCombat||sp.hp>sp.normalMaxHp*transformationThreshold(sp))?'disabled class="combat-locked"':''} onclick="toggleTransformation(${index})">${sp.transformed?'🌘 Revert to '+sp.originalName:sp.hp<=sp.normalMaxHp*transformationThreshold(sp)&&combat&&!sp.transformationUsedThisCombat?'✨ TRANSFORMATION READY: '+sp.transform.name:'🔒 Transform at '+Math.round(transformationThreshold(sp)*100)+'% HP'}</button><div class="muted">${sp.transformed?'Transformation active':sp.transformationUsedThisCombat?'Transformation already used this combat':!combat?'Available during combat':`Unlocks at ${Math.round(transformationThreshold(sp)*100)}% HP or lower`}</div><br>`:''}''', 1)

replace('<button onclick="endTurn()">🔄 END TURN</button>`;',
        '<button ${G.ps.some(s=>!s.dead&&!s.knockedOut&&s.hp>0&&s.combatActions>0)?\'disabled class="combat-locked" title="Spend the party Combat AP before ending the round"\':\'\'} onclick="endTurn()">🔄 END COMBAT ROUND</button>`;', 1)

old_end = '''  // COMBAT END TURN
if(combat){

    // Resolve one pending attack attempt before refreshing the round
    if(combat.provoked && (combat.attacksSinceCounter||0)>0){
        combat.attacksSinceCounter=0;
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
}'''
new_end = '''  // COMBAT END TURN
if(combat){

    const ready=G.ps.filter(s=>!s.dead&&!s.knockedOut&&s.hp>0&&s.combatActions>0);
    if(ready.length){
      log(`⚔️ ${ready.map(s=>s.name).join(", ")} still ${ready.length===1?"has":"have"} Combat AP. Switch fighters and spend it before ending the round.`,"bad");
      render();
      return;
    }

    if(combat.provoked && (combat.attacksSinceCounter||0)>0){
        combat.attacksSinceCounter=0;
        creatureAttack(combat);
        if(!combat)return;
    }

    G.ps.forEach(ally=>{
      if(ally.dead||ally.knockedOut||ally.hp<=0){ally.combatActions=0;return;}
      ally.combatActions=combatActionCount(ally)+(ally.originalName==="The Signalman"?1:0);
    });

    G.ps.forEach(ally=>{
        if(ally.dead||ally.knockedOut||ally.hp<=0)return;
        if(ally.hp<ally.maxHp){
            ally.hp=Math.min(ally.maxHp,ally.hp+1);
            log(`❤️ ${ally.name} recovers 1 HP after the combat round.`,"good");
        }
    });

    const firstReady=G.ps.findIndex(s=>!s.dead&&!s.knockedOut&&s.hp>0&&s.combatActions>0);
    if(firstReady>=0)G.active=firstReady;
    log(`🔄 A new combat round begins. Every conscious survivor's Combat AP is refreshed.`,"good");
    render();
    return;
}'''
replace(old_end, new_end, 1)

# Reset forms at encounter boundaries. Two victory paths share similar text.
replace('const defeatedName=combat.name;\ncombat=null;\nshowPostCombatReward(defeatedName);',
        'const defeatedName=combat.name;\nresetCombatTransformations();\ncombat=null;\nshowPostCombatReward(defeatedName);')
replace('''G.ps.forEach(s=>{
  s.combatActions=0;
});
combat=null;
}''',
        '''G.ps.forEach(s=>{
  s.combatActions=0;
});
resetCombatTransformations();
combat=null;
}''', 1)
replace('''    // End the current combat
    combat=null;''',
        '''    // End the current combat
    resetCombatTransformations();
    combat=null;''', 1)

# Horror score: remove bass-heavy emphasis and add sparse musical tension.
replace('''    // Dark cinematic pad: layered musical intervals instead of a single static tone.
    const padFilter=ctx.createBiquadFilter();
    padFilter.type="lowpass";padFilter.frequency.value=420;padFilter.Q.value=.7;padFilter.connect(music);
    const padNotes=[43.65,65.41,87.31];
    const padOscillators=padNotes.map((freq,index)=>{
      const osc=ctx.createOscillator(),gain=ctx.createGain();
      osc.type=index===0?"sine":"triangle";
      osc.frequency.value=freq;
      osc.detune.value=index===1?-7:index===2?5:0;
      gain.gain.value=index===0?.46:index===1?.16:.10;
      osc.connect(gain);gain.connect(padFilter);osc.start();
      return {osc,gain};
    });
    const musicLfo=ctx.createOscillator(),musicLfoGain=ctx.createGain();
    musicLfo.type="sine";musicLfo.frequency.value=.055;musicLfoGain.gain.value=75;
    musicLfo.connect(musicLfoGain);musicLfoGain.connect(padFilter.frequency);musicLfo.start();''',
        '''    // V0.5 horror score: restrained midrange drone with sparse, eerie musical notes.
    const padFilter=ctx.createBiquadFilter();
    padFilter.type="lowpass";padFilter.frequency.value=950;padFilter.Q.value=.55;padFilter.connect(music);
    const padNotes=[110.00,164.81,220.00];
    const padOscillators=padNotes.map((freq,index)=>{
      const osc=ctx.createOscillator(),gain=ctx.createGain();
      osc.type=index===0?"triangle":"sine";
      osc.frequency.value=freq;
      osc.detune.value=index===1?-9:index===2?7:0;
      gain.gain.value=index===0?.12:index===1?.055:.035;
      osc.connect(gain);gain.connect(padFilter);osc.start();
      return {osc,gain};
    });
    const musicLfo=ctx.createOscillator(),musicLfoGain=ctx.createGain();
    musicLfo.type="sine";musicLfo.frequency.value=.04;musicLfoGain.gain.value=110;
    musicLfo.connect(musicLfoGain);musicLfoGain.connect(padFilter.frequency);musicLfo.start();

    const horrorMotif=[220.00,233.08,174.61,164.81,277.18,220.00,null,146.83];
    let horrorMotifStep=0;
    const playHorrorNote=()=>{
      if(!audioEnabled()||ctx.state!=="running")return;
      const freq=horrorMotif[horrorMotifStep++%horrorMotif.length];
      if(!freq)return;
      const now=ctx.currentTime,osc=ctx.createOscillator(),noteGain=ctx.createGain(),noteFilter=ctx.createBiquadFilter();
      osc.type="sine";osc.frequency.setValueAtTime(freq,now);
      osc.detune.setValueAtTime((Math.random()-.5)*10,now);
      noteFilter.type="bandpass";noteFilter.frequency.value=1100;noteFilter.Q.value=.8;
      noteGain.gain.setValueAtTime(.0001,now);
      noteGain.gain.exponentialRampToValueAtTime(.028,now+.12);
      noteGain.gain.exponentialRampToValueAtTime(.0001,now+2.8);
      osc.connect(noteFilter);noteFilter.connect(noteGain);noteGain.connect(music);
      osc.start(now);osc.stop(now+3);
    };
    const motifTimer=setInterval(playHorrorNote,4200);''', 1)
replace('horrorAudio={ctx,master,music,ambience,effects,padOscillators,padFilter,musicLfo,wind,windFilter,windGain,windLfo,howl,howlGain,howlLfo};',
        'horrorAudio={ctx,master,music,ambience,effects,padOscillators,padFilter,musicLfo,motifTimer,wind,windFilter,windGain,windLfo,howl,howlGain,howlLfo};', 1)
replace('function updateAudioMix(){if(!horrorAudio)return;const now=horrorAudio.ctx.currentTime;horrorAudio.master.gain.setTargetAtTime(audioEnabled()?.55:0,now,.08);horrorAudio.music.gain.setTargetAtTime(audioLevel("music",20)/100*.11,now,.08);horrorAudio.ambience.gain.setTargetAtTime(audioLevel("ambience",35)/100*.08,now,.08);horrorAudio.effects.gain.setTargetAtTime(audioLevel("effects",55)/100,now,.04);}',
        'function updateAudioMix(){if(!horrorAudio)return;const now=horrorAudio.ctx.currentTime;horrorAudio.master.gain.setTargetAtTime(audioEnabled()?.55:0,now,.08);horrorAudio.music.gain.setTargetAtTime(audioLevel("music",25)/100*.16,now,.12);horrorAudio.ambience.gain.setTargetAtTime(audioLevel("ambience",30)/100*.07,now,.12);horrorAudio.effects.gain.setTargetAtTime(audioLevel("effects",55)/100,now,.04);}', 1)
replace('${audioSlider("music","Music",20)}\n    ${audioSlider("ambience","Ambience",35)}',
        '${audioSlider("music","Music",25)}\n    ${audioSlider("ambience","Ambience",30)}', 1)
replace('Low cinematic drone beneath exploration.', 'Quiet horror score with sparse musical tension beneath exploration.', 1)

path.write_text(text)
print('V0.5 patch applied successfully')
