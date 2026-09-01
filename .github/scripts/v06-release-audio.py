from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old_gain='horrorAudio.music.gain.setTargetAtTime(audioLevel("music",25)/100*.34,now,.12);'
release_gain='/* V0.6_AUDIO_MUSIC_GAIN_RC */ horrorAudio.music.gain.setTargetAtTime(audioLevel("music",25)/100*.82,now,.12);'
mobile_gain='''/* V0.6_AUDIO_MUSIC_GAIN_RC */
  const desktopMusicGain=audioLevel("music",25)/100*.82;
  const phoneMusicGain=(window.matchMedia&&window.matchMedia("(max-width:850px)").matches)?desktopMusicGain*1.22:desktopMusicGain;
  horrorAudio.music.gain.setTargetAtTime(phoneMusicGain,now,.12);'''

if mobile_gain not in s:
    if release_gain in s:
        s=s.replace(release_gain,mobile_gain,1)
        print('added a 22% phone-only music boost while preserving the desktop V0.6 mix')
    elif old_gain in s:
        s=s.replace(old_gain,mobile_gain,1)
        print('applied V0.6 release music gain with a 22% phone-only boost')
    else:
        raise SystemExit('expected V0.6 music gain line not found')
else:
    print('phone-specific release audio gain already applied')

old_copy='Most of all, thank you to anyone who takes time out of their day to try The Last Night and experience The Last Night.'
new_copy='Most of all, thank you to anyone who takes time out of their day to try The Last Night and experience Blackwood County for yourself.'
if old_copy in s:
    s=s.replace(old_copy,new_copy,1)
    print('polished beta thank-you copy')
elif new_copy not in s:
    raise SystemExit('expected beta thank-you copy not found')

p.write_text(s,encoding='utf-8')
