from pathlib import Path
import re

p=Path('v06-enhancements.js')
s=p.read_text(encoding='utf-8')

# Close V0.6 overlays and hide Journal when returning to menu.
s=s.replace("if(!inGame){const b=document.getElementById('v06NightBadge');if(b)b.hidden=true}","if(!inGame){const b=document.getElementById('v06NightBadge');if(b)b.hidden=true;const o=document.getElementById('v06Overlay');if(o&&o.classList.contains('open'))close()}",1)

# Journal cannot open from menu. Opening it marks this save's Journal as read.
s=s.replace("function openJournal(){if(!hasGame())return;","function openJournal(){if(!hasGame()||document.body.classList.contains('menu-mode'))return;G.v06JournalReadCount=(G.v06Journal||[]).length;",1)

# Replace browser/session-wide unread tracking with save-local tracking stored on G.
pattern=r"function journalDot\(\)\{.*?\n\}"
replacement="""function journalDot(){
  if(!hasGame())return;
  const count=(G.v06Journal||[]).length,last=Number(G.v06JournalReadCount||0),dot=document.getElementById('v06JournalDot');
  if(dot)dot.hidden=!(count>last);
  const journal=document.getElementById('v06JournalBtn');
  if(journal&&!journal.dataset.v06ReadHook){journal.dataset.v06ReadHook='1';journal.addEventListener('click',()=>{G.v06JournalReadCount=(G.v06Journal||[]).length;if(dot)dot.hidden=true})}
}"""
s,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
if n!=1: raise SystemExit('journalDot function not found')

if 'theLastNightJournalReadCount' in s: raise SystemExit('shared Journal read-state still present')
if "document.body.classList.contains('menu-mode'))return;G.v06JournalReadCount" not in s: raise SystemExit('Journal menu guard missing')
if 'last=Number(G.v06JournalReadCount||0)' not in s: raise SystemExit('save-local Journal unread state missing')

p.write_text(s,encoding='utf-8')
print('patched Journal visibility and per-save state')
