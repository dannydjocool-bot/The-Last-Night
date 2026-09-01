from pathlib import Path
p=Path('v06-enhancements.js')
s=p.read_text()
s=s.replace("function openJournal(){if(!hasGame())return;", "function openJournal(){if(!hasGame()||document.body.classList.contains('menu-mode'))return;G.v06JournalReadCount=(G.v06Journal||[]).length;", 1)
s=s.replace("const last=Number(sessionStorage.getItem('theLastNightJournalReadCount')||0);", "const last=Number(G.v06JournalReadCount||0);", 1)
s=s.replace("sessionStorage.setItem('theLastNightJournalReadCount',String((G.v06Journal||[]).length));", "G.v06JournalReadCount=(G.v06Journal||[]).length;", 1)
s=s.replace("if(!inGame){const b=document.getElementById('v06NightBadge');if(b)b.hidden=true}", "if(!inGame){const b=document.getElementById('v06NightBadge');if(b)b.hidden=true;const o=document.getElementById('v06Overlay');if(o&&o.classList.contains('open'))close()}", 1)
p.write_text(s)
