from pathlib import Path

p=Path('v06-enhancements.js')
s=p.read_text(encoding='utf-8')

# Existing clarity changes are already present in current dev. Only apply them if needed.
repls={
"if(Math.random()<.55&&typeof gainItem==='function'){gainItem();lg(`🎒 ${p.name}'s deeper search uncovers an additional item.`,'good')}":"if(!currentCombat()&&Math.random()<.55&&typeof gainItem==='function'){gainItem();lg(`🎒 ${p.name}'s deeper search uncovers an additional item.`,'good')}",
"if(Math.random()<.5)lg(`👂 ${p.name} hears movement before it reaches the room.`,'good')":"if(!currentCombat()&&Math.random()<.5)lg(`👂 ${p.name} hears movement before it reaches the room.`,'good')",
}
for old,new in repls.items():
    if old in s:
        s=s.replace(old,new,1)

# Journal UI must never remain visible on the main menu, even if a save object remains in memory.
old="if(!inGame){const b=document.getElementById('v06NightBadge');if(b)b.hidden=true}"
new="if(!inGame){const b=document.getElementById('v06NightBadge');if(b)b.hidden=true;const o=document.getElementById('v06Overlay');if(o&&o.classList.contains('open'))close()}"
if old in s:
    s=s.replace(old,new,1)

# Journal can only open during active gameplay. Mark the current save's entries as read on open.
old="function openJournal(){if(!hasGame())return;"
new="function openJournal(){if(!hasGame()||document.body.classList.contains('menu-mode'))return;G.v06JournalReadCount=(G.v06Journal||[]).length;"
if old in s:
    s=s.replace(old,new,1)

# Replace browser-wide unread state with state stored inside G so every save slot tracks its own Journal.
s=s.replace("const last=Number(sessionStorage.getItem('theLastNightJournalReadCount')||0);","const last=Number(G.v06JournalReadCount||0);",1)
s=s.replace("sessionStorage.setItem('theLastNightJournalReadCount',String((G.v06Journal||[]).length));","G.v06JournalReadCount=(G.v06Journal||[]).length;",1)

# Validation: fail if old shared Journal read-state remains.
if "theLastNightJournalReadCount" in s:
    raise SystemExit('shared Journal read-state still present')
if "document.body.classList.contains('menu-mode'))return;G.v06JournalReadCount" not in s:
    raise SystemExit('Journal menu guard missing')
if "const last=Number(G.v06JournalReadCount||0);" not in s:
    raise SystemExit('save-local Journal read count missing')

p.write_text(s,encoding='utf-8')
print('patched Journal visibility and save isolation')
