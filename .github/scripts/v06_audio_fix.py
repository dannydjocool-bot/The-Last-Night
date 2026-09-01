from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

replacement = r'''function ensureHorrorAudio(){
  if(!audioEnabled())return null;
  const AudioCtor=window.AudioContext||window.webkitAudioContext;
  if(!AudioCtor)return null;
  if(!horrorAudio){
    const ctx=new AudioCtor(),master=ctx.createGain(),music=ctx.createGain(),ambience=ctx.createGain(),effects=ctx.createGain();
    master.connect(ctx.destination);music.connect(master);ambience.connect(master);effects.connect(master);

    // V0.6 cinematic horror score: no continuous bass/room-tone oscillators.
    // The old always-running low frequencies could resemble an idling engine.
    const scoreBus=ctx.createBiquadFilter();
    scoreBus.type="lowpass";scoreBus.frequency.value=1800;scoreBus.Q.value=.55;scoreBus.connect(music);

    const createReverb=()=>{
      const convolver=ctx.createConvolver(),length=Math.floor(ctx.sampleRate*2.8),impulse=ctx.createBuffer(2,length,ctx.sampleRate);
      for(let ch=0;ch<2;ch++){
        const data=impulse.getChannelData(ch);
        for(let i=0;i<length;i++)data[i]=(Math.random()*2-1)*Math.pow(1-i/length,2.6);
      }
      convolver.buffer=impulse;convolver.connect(scoreBus);return convolver;
    };
    const reverb=createReverb();

    const darkChords=[
      [110.00,130.81,164.81],
      [103.83,123.47,155.56],
      [116.54,138.59,174.61],
      [98.00,116.54,146.83]
    ];
    let chordStep=0;
    const playDarkChord=()=>{
      if(!audioEnabled()||ctx.state!=="running")return;
      const now=ctx.currentTime,notes=darkChords[chordStep++%darkChords.length];
      notes.forEach((freq,index)=>{
        const osc=ctx.createOscillator(),gain=ctx.createGain(),filter=ctx.createBiquadFilter();
        osc.type=index===0?"triangle":"sine";
        osc.frequency.setValueAtTime(freq,now);
        osc.detune.setValueAtTime(index===1?-7:index===2?9:0,now);
        filter.type="lowpass";filter.frequency.value=650+(index*180);filter.Q.value=.7;
        gain.gain.setValueAtTime(.0001,now);
        gain.gain.exponentialRampToValueAtTime(index===0?.032:.018,now+1.8);
        gain.gain.setValueAtTime(index===0?.032:.018,now+3.5);
        gain.gain.exponentialRampToValueAtTime(.0001,now+7.5);
        osc.connect(filter);filter.connect(gain);gain.connect(scoreBus);gain.connect(reverb);
        osc.start(now);osc.stop(now+7.7);
      });
    };

    const motif=[293.66,null,220.00,233.08,null,174.61,null,311.13,146.83,null];
    let motifStep=0;
    const playHorrorNote=()=>{
      if(!audioEnabled()||ctx.state!=="running")return;
      const freq=motif[motifStep++%motif.length];
      if(!freq)return;
      const now=ctx.currentTime,osc=ctx.createOscillator(),gain=ctx.createGain(),filter=ctx.createBiquadFilter();
      osc.type="sine";osc.frequency.setValueAtTime(freq,now);
      filter.type="bandpass";filter.frequency.value=1200;filter.Q.value=1.8;
      gain.gain.setValueAtTime(.0001,now);
      gain.gain.exponentialRampToValueAtTime(.018,now+.06);
      gain.gain.exponentialRampToValueAtTime(.0001,now+4.4);
      osc.connect(filter);filter.connect(gain);gain.connect(scoreBus);gain.connect(reverb);
      osc.start(now);osc.stop(now+4.5);
    };

    const heartbeat=()=>{
      if(!audioEnabled()||ctx.state!=="running")return;
      const pulse=(delay,level)=>{
        const now=ctx.currentTime+delay,osc=ctx.createOscillator(),gain=ctx.createGain();
        osc.type="sine";osc.frequency.setValueAtTime(62,now);osc.frequency.exponentialRampToValueAtTime(38,now+.22);
        gain.gain.setValueAtTime(.0001,now);gain.gain.exponentialRampToValueAtTime(level,now+.015);gain.gain.exponentialRampToValueAtTime(.0001,now+.28);
        osc.connect(gain);gain.connect(ambience);osc.start(now);osc.stop(now+.3);
      };
      pulse(0,.045);pulse(.34,.028);
    };

    const windSwell=()=>{
      if(!audioEnabled()||ctx.state!=="running")return;
      const duration=3.8,frames=Math.floor(ctx.sampleRate*duration),buffer=ctx.createBuffer(1,frames,ctx.sampleRate),data=buffer.getChannelData(0);
      for(let i=0;i<frames;i++)data[i]=(Math.random()*2-1);
      const source=ctx.createBufferSource(),filter=ctx.createBiquadFilter(),gain=ctx.createGain(),now=ctx.currentTime;
      source.buffer=buffer;filter.type="bandpass";filter.frequency.value=520;filter.Q.value=.55;
      gain.gain.setValueAtTime(.0001,now);gain.gain.exponentialRampToValueAtTime(.012,now+1.4);gain.gain.exponentialRampToValueAtTime(.0001,now+duration);
      source.connect(filter);filter.connect(gain);gain.connect(ambience);source.start(now);
    };

    playDarkChord();
    setTimeout(playHorrorNote,2600);
    const chordTimer=setInterval(playDarkChord,15500);
    const motifTimer=setInterval(playHorrorNote,6800);
    const heartbeatTimer=setInterval(()=>{if(Math.random()<.72)heartbeat();},11800);
    const windTimer=setInterval(()=>{if(Math.random()<.62)windSwell();},17300);

    horrorAudio={ctx,master,music,ambience,effects,scoreBus,reverb,chordTimer,motifTimer,heartbeatTimer,windTimer};
  }
  if(horrorAudio.ctx.state==="suspended")horrorAudio.ctx.resume();
  updateAudioMix();
  return horrorAudio;
}
function updateAudioMix(){'''

pattern = r'function ensureHorrorAudio\(\)\{.*?\n\}\nfunction updateAudioMix\(\)\{'
patched, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f'Expected to replace one audio block, replaced {count}')

patched = patched.replace('horrorAudio.master.gain.setTargetAtTime(audioEnabled()?.62:0,now,.08);', 'horrorAudio.master.gain.setTargetAtTime(audioEnabled()?.68:0,now,.08);')
patched = patched.replace('horrorAudio.music.gain.setTargetAtTime(audioLevel("music",25)/100*.28,now,.12);', 'horrorAudio.music.gain.setTargetAtTime(audioLevel("music",25)/100*.34,now,.12);')
patched = patched.replace('horrorAudio.ambience.gain.setTargetAtTime(audioLevel("ambience",30)/100*.11,now,.12);', 'horrorAudio.ambience.gain.setTargetAtTime(audioLevel("ambience",30)/100*.16,now,.12);')

path.write_text(patched, encoding='utf-8')
print('Patched V0.6 cinematic horror soundtrack')
