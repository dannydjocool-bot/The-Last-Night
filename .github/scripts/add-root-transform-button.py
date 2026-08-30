from pathlib import Path

p=Path('index.html')
t=p.read_text()

css_marker='/* V0.5 Root Gate showcase transformation action */'
if css_marker not in t:
    css='''\n/* V0.5 Root Gate showcase transformation action */\n.gate-transform-actions{display:flex;justify-content:center;margin-top:12px}\n.gate-transform-btn{min-width:210px!important;background:linear-gradient(#7f2833,#4c141b)!important;border-color:#b64b57!important;box-shadow:0 0 18px rgba(182,75,87,.18)}\n@media(max-width:600px){.gate-transform-actions{margin-top:10px}.gate-transform-btn{width:100%!important;max-width:none!important;min-width:0!important}}\n'''
    anchor='</style>'
    if anchor not in t:
        raise SystemExit('style closing tag not found')
    t=t.replace(anchor,css+anchor,1)

old='''</div><div class="gate-guardian-dots">${guardians.map((_,i)=>`<button class="gate-guardian-dot ${i===rootGuardianShowcaseIndex?'active':''}" onclick="showRootGateGuardian(${i})" aria-label="Show guardian ${i+1}"></button>`).join("")}</div>`;'''
new='''</div><div class="gate-guardian-dots">${guardians.map((_,i)=>`<button class="gate-guardian-dot ${i===rootGuardianShowcaseIndex?'active':''}" onclick="showRootGateGuardian(${i})" aria-label="Show guardian ${i+1}"></button>`).join("")}</div><div class="gate-transform-actions"><button class="showcase-next gate-transform-btn" onclick="viewRootFusionTransformation()">VIEW TRANSFORMATION</button></div>`;'''
if old in t:
    t=t.replace(old,new,1)
elif 'gate-transform-actions' not in t:
    raise SystemExit('guardian showcase anchor not found')

p.write_text(t)
print('Root Gate transformation button added')
