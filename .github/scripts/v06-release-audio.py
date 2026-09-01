from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old_gain='horrorAudio.music.gain.setTargetAtTime(audioLevel("music",25)/100*.34,now,.12);'
new_gain='/* V0.6_AUDIO_MUSIC_GAIN_RC */ horrorAudio.music.gain.setTargetAtTime(audioLevel("music",25)/100*.82,now,.12);'
if new_gain not in s:
    if old_gain not in s:
        raise SystemExit('expected V0.6 music gain line not found')
    s=s.replace(old_gain,new_gain,1)
    print('raised V0.6 music channel max gain from 0.34 to 0.82')
else:
    print('release audio gain already applied')

old_copy='Most of all, thank you to anyone who takes time out of their day to try The Last Night and experience The Last Night.'
new_copy='Most of all, thank you to anyone who takes time out of their day to try The Last Night and experience Blackwood County for yourself.'
if old_copy in s:
    s=s.replace(old_copy,new_copy,1)
    print('polished beta thank-you copy')
elif new_copy not in s:
    raise SystemExit('expected beta thank-you copy not found')

p.write_text(s,encoding='utf-8')
