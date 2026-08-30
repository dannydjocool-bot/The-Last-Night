from pathlib import Path
p=Path('index.html')
t=p.read_text()

if 'ROOTSTORM coils around' not in t:
    needle='''if(c.name==="The Triune Maw"){
  c.triuneAttackCount=(c.triuneAttackCount||0)+1;
  if(c.hp<=c.maxHp*0.5)dmg+=3;
  if(c.triuneAttackCount%3===0){dmg+=6;p.san=Math.max(0,p.san-2);log(`🔥 TRIUNE BERSERK! ${p.name} loses 2 Sanity as the fused guardian unleashes a crushing strike.`,"bad");}
}'''
    replacement='''if(c.name==="The Triune Maw"){
  c.triuneAttackCount=(c.triuneAttackCount||0)+1;
  if(c.hp<=c.maxHp*0.5)dmg+=3;
  if(c.triuneAttackCount%3===0){dmg+=6;p.san=Math.max(0,p.san-2);log(`🔥 TRIUNE BERSERK! ${p.name} loses 2 Sanity as the fused guardian unleashes a crushing strike.`,"bad");}
  if(Math.random()<0.25){p.combatAp=Math.max(0,(p.combatAp||0)-1);log(`🌿 ROOTSTORM coils around ${p.name}, draining 1 Combat AP.`,"bad");}
}'''
    if needle in t:
        t=t.replace(needle,replacement,1)
    else:
        # Fallback: place the Rootstorm roll immediately before the rare creature ability section.
        anchor='// ===============================\n// RARE CREATURE ABILITIES'
        if anchor not in t:
            raise SystemExit('Rootstorm patch anchor not found')
        block='''if(c.name==="The Triune Maw" && Math.random()<0.25){
  p.combatAp=Math.max(0,(p.combatAp||0)-1);
  log(`🌿 ROOTSTORM coils around ${p.name}, draining 1 Combat AP.`,"bad");
}

'''
        t=t.replace(anchor,block+anchor,1)

p.write_text(t)
print('Triune Maw Rootstorm hook verified.')
