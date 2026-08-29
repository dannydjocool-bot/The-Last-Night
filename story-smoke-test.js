const fs=require("fs");
const vm=require("vm");

const html=fs.readFileSync("index.html","utf8");
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes=new Map();
function node(){
  return {
    style:{},innerHTML:"",textContent:"",value:"",disabled:false,offsetWidth:220,offsetHeight:180,
    classList:{add(){},remove(){},toggle(){},contains(){return false;}},
    addEventListener(){},focus(){},setAttribute(){},getAttribute(){return null;},appendChild(){},remove(){},
    getBoundingClientRect(){return {left:0,top:0,width:220,height:180};}
  };
}
const document={
  body:node(),
  getElementById(id){if(!nodes.has(id))nodes.set(id,node());return nodes.get(id);},
  querySelectorAll(){return [];},addEventListener(){},createElement(){return node();}
};
const storage=new Map();
const localStorage={getItem:k=>storage.has(k)?storage.get(k):null,setItem:(k,v)=>storage.set(k,String(v)),removeItem:k=>storage.delete(k)};
const context={console,document,localStorage,setTimeout:fn=>{fn();return 1;},clearTimeout(){},Date,Math,JSON,Set,Infinity,window:null,location:{reload(){throw new Error("Unexpected reload");}}};
context.window=context;context.innerWidth=1400;context.innerHeight=900;context.addEventListener=()=>{};
vm.createContext(context);
vm.runInContext(script,context);

function run(code){return vm.runInContext(code,context);}
function assert(value,message){if(!value)throw new Error(message);}
const base=`({ps:[{name:"Tester",dead:false,actions:0,loc:"motel"}],active:0,night:10,clues:10,foundClues:new Set(),discovered:new Set(["motel"]),wardenDefeated:false,hollowDefeated:false,bloodkeeperDefeated:false,sentinelDefeated:false,rootEntered:false,rootDefeated:false,storyItems:[],creatures:[],extraPockets:[],extraPocketMax:10,ammo:{pistol:0,shotgun:0,smg:0,rifle:0},log:[],outcome:null,completedAt:null})`;
run(`G=${base};combat=null;currentSaveSlot=null;`);

assert(run(`spawnStoryBoss("prison")&&G.creatures[0].name==="The Warden"`),"Warden was not guaranteed at Prison");
run(`G.creatures=[];G.wardenDefeated=true;`);
assert(run(`spawnStoryBoss("hollow")&&G.creatures[0].name==="The Hollow"`),"Hollow was not guaranteed at The Hollow");
run(`G.creatures=[];G.hollowDefeated=true;G.storyItems.push("Warden-Hollow Relic");`);
assert(run(`spawnStoryBoss("slaughterhouse")&&G.creatures[0].name==="The Bloodkeeper"`),"Bloodkeeper was not guaranteed at Slaughterhouse");
run(`G.creatures=[];G.bloodkeeperDefeated=true;G.storyItems.push("Bloodkeeper Relic");`);
assert(run(`spawnStoryBoss("asylum")&&G.creatures[0].name==="The Blackwood Sentinel"`),"Sentinel was not guaranteed at Asylum");
run(`G.creatures=[];G.sentinelDefeated=true;G.storyItems.push("Sentinel Relic");`);
assert(run(`spawnStoryBoss("root")&&G.creatures[0].name==="The Root of Blackwood"`),"Root was not guaranteed after relics");

run(`G.creatures=[];G.rootDefeated=true;currentSaveSlot=2;completeRun("victory");`);
assert(run(`G.outcome==="victory"`),"Victory ending did not complete");
assert(storage.has("theLastNightSaveSlot2"),"Completed victory was not preserved in the active slot");
assert(JSON.parse(storage.get("theLastNightSaveSlot2")).outcome==="victory","Saved completion status is missing");

run(`G=${base};G.night=30;combat=null;currentSaveSlot=null;render=()=>{};endNight();`);
assert(run(`G.night===31&&G.outcome===null`),"The unlimited run incorrectly ended after Night 30");

assert(run(`S.every(s=>s.hp===({Common:25,Uncommon:30,Rare:35,Epic:40,Legendary:45,"G.O.A.T":50}[s.rarity]))`),"Survivor HP does not match the rarity scale");
run(`G=${base};combat={name:"Test Creature",provoked:false,attacksSinceCounter:0,testCounters:0};creatureAttack=c=>c.testCounters++;registerCombatAttack();`);
assert(run(`combat.testCounters===0&&combat.attacksSinceCounter===1`),"Creature countered before the second attack");
run(`registerCombatAttack();`);
assert(run(`combat.testCounters===1&&combat.attacksSinceCounter===0`),"Creature did not counter after the second attack");

assert(run(`combatActionCount({rarity:"Common"})===5&&combatActionCount({rarity:"G.O.A.T"})===10`),"Combat AP was not reduced by 5 across rarities");
assert(run(`nightActionCount({rarity:"Common"})===10&&nightActionCount({rarity:"G.O.A.T"})===15`),"Night AP was not reduced by 15 and scaled by rarity");
assert(run(`counterattackDamage({rarity:"Common"},4)===3&&counterattackDamage({rarity:"Rare"},4)===4`),"Low-rarity counterattack damage was not reduced by 35%");
run(`G=${base};G.ps[0].actions=5;G.creatures=[{name:"Roadblock",loc:"motel",hp:5}];combat=null;render=()=>{};move("gas");`);
assert(run(`G.ps[0].loc==="motel"&&G.ps[0].actions===5`),"A living creature did not block location travel");
assert(run(`hostileAtCurrentLocation(G.ps[0])===true&&canEndNight()===false`),"An unresolved creature did not lock non-combat night actions");

run(`G=${base};G.singlePlayer=true;G.ps=[{name:"Bearer",dead:false,hp:50,maxHp:50,baseMaxHp:50,shield:100,maxShield:100,knowledgeOfWisdom:true,actions:3,rarity:"Common",restsThisNight:0,maxSan:5,san:5,fear:0,items:[]}];`);
assert(run(`JSON.stringify(damageSurvivor(G.ps[0],35))===JSON.stringify({armorDamage:35,hpDamage:0})&&G.ps[0].shield===65&&G.ps[0].hp===50`),"Knowledge Armor did not absorb damage before HP");
run(`G.ps[0].shield=20;render=()=>{};recover();`);
assert(run(`G.ps[0].shield===100`),"Knowledge Armor did not regenerate when its bearer Rested");
assert(run(`ITEMS.every(i=>i[0]!=="Armor Plate")&&SINGLE_PLAYER_ITEMS.some(i=>i[0]==="Armor Plate")`),"Armor Plate was not restricted to Single Player loot");
assert(run(`S.filter(s=>s.isNew&&s.transform).length===2&&S.some(s=>s.name==="The Moonbound")&&S.some(s=>s.name==="The Ashen Saint")`),"The two transforming G.O.A.T survivors are missing");
run(`singleSetup={partySize:1,pool:drawSurvivors(5),selected:["x"],wisdom:"x",rollsUsed:1,maxRolls:3};renderSinglePlayerSetup=()=>{};rerollSingleCandidates();rerollSingleCandidates();rerollSingleCandidates();`);
assert(run(`singleSetup.rollsUsed===3&&singleSetup.pool.length===5&&singleSetup.selected.length===0&&singleSetup.wisdom===null`),"Single Player survivor rolls did not stop at three");
run(`let s=S.find(x=>x.name==="The Moonbound");G=${base};G.ps=[{name:s.name,originalName:s.name,image:s.image,normalImage:s.image,maxHp:s.hp,normalMaxHp:s.hp,baseMaxHp:s.hp,hp:s.hp,weapon:s.weapon,normalWeapon:s.weapon,weaponDamage:s.damage,normalWeaponDamage:s.damage,baseWeaponDamage:s.damage,weaponAbility:s.weaponAbility,normalWeaponAbility:s.weaponAbility,ability:s.ability,normalAbility:s.ability,transform:s.transform,transformKey:s.transformKey,transformed:false,maxShield:0,normalMaxShield:0,shield:0,dead:false}];render=()=>{};combat=null;toggleTransformation(0);`);
assert(run(`G.ps[0].transformed&&G.ps[0].name==="The Eclipse Beast"&&G.ps[0].maxHp===70&&G.ps[0].weaponDamage===13`),"The Moonbound transformation did not apply its improved form stats");
run(`toggleTransformation(0);`);
assert(run(`!G.ps[0].transformed&&G.ps[0].name==="The Moonbound"&&G.ps[0].maxHp===50&&G.ps[0].weaponDamage===8`),"The Moonbound could not freely revert");

assert(run(`S.filter(s=>s.recruitOnly).length===7`),"The seven flashlight-only survivors are missing");
assert(run(`Array.from({length:30},()=>drawSurvivors(5)).flat().every(s=>!s.recruitOnly)`),"A flashlight-only recruit appeared in a starting draw");
assert(run(`['Pistol','Shotgun','MP5','AK-47','Hunting Knife','Fire Axe'].every(name=>ITEM_META[name].image==='weapon-items.png'&&ITEM_META[name].spritePosition)`),"Weapon inventory artwork is not mapped");
assert(run(`[...ITEMS,...SINGLE_PLAYER_ITEMS].every(raw=>{let item=objItem(raw);return item.image&&item.spritePosition&&item.spriteSize&&ITEM_META[item.name].description})`),"Every obtainable item must have artwork and an Item Codex description");
assert(fs.existsSync("item-atlas.png")&&fs.existsSync("weapon-items.png"),"An inventory art atlas is missing");
assert(!html.includes("The party's shared Night Pack. Weapons, tools, medicine, and supplies stored here are available to every survivor."),"The removed Main Pack note is still displayed");
assert(html.includes("🎒 Obtainable Items")&&html.includes("Blackwood Obtainable Item Codex"),"The Obtainable Items menu codex is missing");
assert(run(`L.length===36&&L.every(entry=>LOCATION_AREAS[entry[0]]&&LOCATION_AREAS[entry[0]].length===2)&&new Set(L.map(entry=>locationArt(entry[0]).image+'|'+locationArt(entry[0]).position)).size===36`),"Every location needs distinct art and two atmospheric Flashlight choices");
assert(fs.existsSync("locations-normal.png")&&fs.existsSync("locations-danger.png")&&fs.existsSync("locations-deadly.png"),"A location artwork atlas is missing");
assert(run(`let flashlight=objItem(ITEMS.find(i=>i[0]==='Flashlight'));flashlight.maxDurability===undefined&&flashlight.durability===undefined`),"The permanent Flashlight still has breakable durability");
run(`localStorage.removeItem(LOCATION_CODEX_KEY);G=${base};G.flashlightUsedLocations=new Set();unlockLocationCodex('motel');`);
assert(run(`readLocationCodexUnlocks().has('motel')&&JSON.parse(localStorage.getItem(LOCATION_CODEX_KEY)).includes('motel')`),"A completed Flashlight sweep did not persist its Location Codex unlock");
run(`localStorage.removeItem(LOCATION_CODEX_KEY);G=null;`);
assert(run(`let unlocked=readLocationCodexUnlocks();unlocked.size===1&&unlocked.has('motel')`),"Riverside Motel was not the only default Location Codex unlock");
assert(run(`L.every(entry=>LOCATION_DESCRIPTIONS[entry[0]]&&LOCATION_DESCRIPTIONS[entry[0]].length>80)`),"Every unlocked location needs a full field description");
run(`G=${base};G.flashlightUsedLocations=new Set(['gas']);localStorage.setItem('theLastNightSaveSlot1',JSON.stringify({G:{flashlightUsedLocations:new Set(['station'])}},saveReplacer));`);
assert(run(`let combinedUnlocks=readLocationCodexUnlocks();combinedUnlocks.has('motel')&&combinedUnlocks.has('gas')&&combinedUnlocks.has('station')`),"Location Codex did not combine permanent, active-run, and saved-run discoveries");
assert(html.includes("🗺️ Locations")&&html.includes("Blackwood Location Records"),"The Main Menu Locations codex is missing");
assert(!html.includes("alert("),"A native browser alert remains instead of the themed warning system");
assert(run(`let settings=settingsHtml();settings.includes('Atmospheric Audio')&&settings.includes('audio_music')&&settings.includes('audio_ambience')&&settings.includes('audio_effects')`),"Separate atmospheric audio controls are missing");
assert(html.includes('id="nightTransition"')&&html.includes('id="combatIntro"')&&html.includes('id="combatFxLayer"'),"The cinematic night or combat presentation layers are missing");
assert(run(`typeof showNightTransition==='function'&&typeof showCombatIntro==='function'&&typeof combatFx==='function'&&typeof horrorTone==='function'`),"An immersion presentation controller is missing");
run(`G=${base};G.extraPocketMax=30;G.flashlightUsedLocations=new Set();G.ps=[{name:'Tester',originalName:'Tester',dead:false,loc:'motel'}];G.pendingRecruit='The Paramedic';render=()=>{};closeFlashlightOverlay=()=>{};acceptFlashlightRecruit(-1);`);
assert(run(`G.ps.length===2&&G.ps[1].name==='The Paramedic'&&G.ps[1].hp===Math.ceil(G.ps[1].maxHp*.3)`),"Wounded flashlight recruit did not join at 30% HP");
assert(run(`!availableFlashlightRecruits().some(s=>s.name==='The Paramedic')`),"An active recruit remained eligible as a duplicate");
run(`G=${base};G.extraPocketMax=30;G.flashlightUsedLocations=new Set();G.ps=[{name:'Tester',originalName:'Tester',dead:false,loc:'motel'}];let oldRandom=Math.random;Math.random=()=>.5;resolveEnragedFlashlightEncounter();Math.random=oldRandom;`);
assert(run(`G.creatures.length===2&&G.creatures.every(c=>c.enraged&&c.firstStrike&&c.hp===Math.ceil(CRE.find(x=>x.name===c.name).hp*1.2)&&c.atk===Math.ceil(CRE.find(x=>x.name===c.name).atk*1.3))`),"Flashlight creatures were not created with enraged stats and first strike");

run(`G=${base};G.ps=[{name:"A",dead:false,hp:10,maxHp:25,actions:2,rarity:"Common"},{name:"B",dead:false,hp:12,maxHp:30,actions:4,rarity:"Uncommon"},{name:"C",dead:false,hp:20,maxHp:35,actions:8,rarity:"Rare"}];postCombatRewardOpen=true;render=()=>{};claimCombatReward("heal");`);
assert(run(`G.ps[0].hp===15&&G.ps[1].hp===17&&G.ps[2].hp===25`),"Three-survivor injury recovery was not applied to the full party");
run(`postCombatRewardOpen=true;claimCombatReward("actions");`);
assert(run(`G.ps[0].actions===3&&G.ps[1].actions===5&&G.ps[2].actions===9`),"Three-survivor AP recovery was not applied to the full party");

console.log("Story smoke test passed: story, saves, combat locks, three-roll setup, transformations, 30-slot Main Pack, complete item art and codex, flashlight recruits, and enraged encounters.");
