from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='horrorAudio.music.gain.setTargetAtTime(audioLevel("music",25)/100*.34,now,.12);'
new='/* V0.6_AUDIO_MUSIC_GAIN_RC */ horrorAudio.music.gain.setTargetAtTime(audioLevel("music",25)/100*.82,now,.12);'
if new in s:
    print('release audio gain already applied')
    raise SystemExit(0)
if old not in s:
    raise SystemExit('expected V0.6 music gain line not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('raised V0.6 music channel max gain from 0.34 to 0.82')
