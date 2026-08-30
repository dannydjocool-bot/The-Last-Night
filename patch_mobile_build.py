from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '/* MOBILE_VISUAL_BUILD_FIX_V1 */'

if marker not in text:
    css = r'''
/* MOBILE_VISUAL_BUILD_FIX_V1 */
@media(max-width:600px){
  /* Preserve the correct sprite grid for each item atlas so weapons are not cropped. */
  .item-codex-card .item-codex-art{
    height:180px!important;
    background-repeat:no-repeat!important;
    background-color:#090a0b!important;
  }
  .item-codex-card .item-codex-art[style*="weapon-items.png"]{
    background-size:300% 200%!important;
  }
  .item-codex-card .item-codex-art[style*="item-atlas.png"]{
    background-size:400% 400%!important;
  }

  /* Mobile-only menu portraits: keep complete heads/portraits visible. */
  #newSurvivorShowcase .recruit-card{
    min-height:0!important;
    background:#090a0b!important;
  }
  #newSurvivorShowcase .recruit-card img{
    display:block!important;
    width:100%!important;
    height:auto!important;
    aspect-ratio:2/3!important;
    object-fit:contain!important;
    object-position:center top!important;
    background:#090a0b!important;
  }
  #newSurvivorShowcase .recruit-card:after{
    inset:42% 0 0!important;
  }
}
'''
    text = text.replace('</style>', css + '\n</style>', 1)
    p.write_text(text, encoding='utf-8')
