from pathlib import Path
import base64

ASSETS = {
    'thornbound.webp.b64': 'thornbound.webp',
    'veinmaw.webp.b64': 'veinmaw.webp',
    'ashwraith.webp.b64': 'ashwraith.webp',
    'root_fusion_1.webp.b64': 'root-fusion-1.webp',
    'root_fusion_2.webp.b64': 'root-fusion-2.webp',
    'root_fusion_3.webp.b64': 'root-fusion-3.webp',
    'root_fusion_4.webp.b64': 'root-fusion-4.webp',
}

src = Path('.github/v05_assets')
for encoded_name, output_name in ASSETS.items():
    raw = (src / encoded_name).read_text().strip()
    try:
        data = base64.b64decode(raw, validate=True)
    except Exception as exc:
        raise SystemExit(f'Invalid base64 for {encoded_name}: {exc}')
    if len(data) < 100 or data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        raise SystemExit(f'Invalid WebP payload for {encoded_name}')
    Path(output_name).write_bytes(data)
    print(f'{output_name}: {len(data)} bytes OK')

print('All seven V0.5 guardian/fusion WebP assets decoded and validated.')
