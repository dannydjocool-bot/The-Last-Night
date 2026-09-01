from pathlib import Path

js_path = Path('v06-enhancements.js')
css_path = Path('v06-enhancements.css')
js = js_path.read_text()
css = css_path.read_text()

repls = [
    (
        "if(typeof endNight==='function'){const o=endNight;window.endNight=function(){const old=hasGame()?G.night:null;const r=o.apply(this,arguments);if(hasGame()&&G.night!==old)setTimeout(newNightMod,90);return r}}",
        "if(typeof endNight==='function'){const o=endNight;window.endNight=function(){const old=hasGame()?G.night:null;const r=o.apply(this,arguments);if(hasGame()&&G.night!==old)setTimeout(newNightMod,1650);return r}}"
    ),
    (
        "if(typeof render==='function'){const o=render;window.render=function(){const r=o.apply(this,arguments);psych();badge();syncUi();return r}}",
        "if(typeof render==='function'){const o=render;window.render=function(){const c=currentCombat();if(c)phase(c);const r=o.apply(this,arguments);psych();badge();syncUi();return r}}"
    ),
    (
        "box.innerHTML='<div class=\"v06-guidance-head\"><b>🧭 NEXT STEP</b><button id=\"v06GuidanceHelp\" type=\"button\">?</button></div><div id=\"v06GuidanceText\"></div><div id=\"v06GuidanceMeta\"></div>';",
        "box.innerHTML='<div class=\"v06-guidance-head\"><b>🧭 NEXT STEP</b><button id=\"v06GuidanceHelp\" type=\"button\">?</button></div><div id=\"v06GuidanceText\"></div><div id=\"v06GuidanceLock\" class=\"v06-guidance-lock\" hidden></div><div id=\"v06GuidanceMeta\"></div>';"
    ),
    (
        "function explainLocks(){\n  document.querySelectorAll('.loc.locked').forEach(el=>{el.title='Locked by story progression. Follow NEXT STEP / Story Objective to unlock this location.'});\n  document.querySelectorAll('button:disabled').forEach(btn=>{\n    const label=(btn.textContent||'').trim();\n    if(!btn.title)btn.title=label.toLowerCase().includes('end night')?'Cannot end the Night while a hostile creature is unresolved here.':'This action is unavailable right now. Check NEXT STEP for the current requirement.';\n  });\n}",
        "function explainLocks(){\n  document.querySelectorAll('.loc.locked').forEach(el=>{el.title='Locked by story progression. Follow NEXT STEP / Story Objective to unlock this location.'});\n  document.querySelectorAll('button:disabled').forEach(btn=>{\n    const label=(btn.textContent||'').trim();\n    if(!btn.title)btn.title=label.toLowerCase().includes('end night')?'Cannot end the Night while a hostile creature is unresolved here.':'This action is unavailable right now. Check NEXT STEP for the current requirement.';\n  });\n}\nfunction visibleLockReason(){\n  if(!hasGame())return '';\n  const p=activeSurvivor(),c=combatNow();\n  if(c)return `🔒 Travel and Night actions are locked until ${c.name} is defeated.`;\n  try{if(typeof hostileAtCurrentLocation==='function'&&p&&hostileAtCurrentLocation(p))return '🔒 Travel is locked because a hostile creature is still at this location.'}catch{}\n  if(p&&Number(p.actions||0)<=0)return '🔒 Exploration actions are locked because this survivor has no Night AP left.';\n  if(document.querySelector('.loc.locked'))return '🔒 Some locations are story-locked. Advance the Story Objective to open them.';\n  return '';\n}"
    ),
    (
        "const m=document.getElementById('v06GuidanceMeta');if(m)m.innerHTML=meta.map(x=>`<span>${x}</span>`).join('');\n  highlightObjective();explainLocks();contextualTips();journalDot();",
        "const lock=document.getElementById('v06GuidanceLock'),reason=visibleLockReason();if(lock){lock.hidden=!reason;lock.textContent=reason}\n  const m=document.getElementById('v06GuidanceMeta');if(m)m.innerHTML=meta.map(x=>`<span>${x}</span>`).join('');\n  highlightObjective();explainLocks();contextualTips();journalDot();"
    )
]

for old, new in repls:
    if old not in js:
        raise SystemExit('Expected JS target not found: ' + old[:80])
    js = js.replace(old, new, 1)

css_add = """

/* V0.6 FINAL POLISH */
body.v06-fear-high.v06-sanity-low #game{filter:saturate(.72) contrast(1.12) brightness(.92)}
.v06-guidance-lock{margin-top:8px;padding:7px 9px;border-left:3px solid #a96068;background:rgba(75,31,37,.34);color:#efc6ca;font-size:11px;line-height:1.45}
.v06-guidance-lock[hidden]{display:none!important}
@media(max-width:850px){.v06-guidance-lock{font-size:10px;padding:7px 8px}}
"""
if '/* V0.6 FINAL POLISH */' not in css:
    css += css_add

js_path.write_text(js)
css_path.write_text(css)
print('V0.6 final polish applied.')
