const fs=require("fs");
const vm=require("vm");

const html=fs.readFileSync("index.html","utf8");
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes=new Map();
function node(){
  return {
    style:{},innerHTML:"",textContent:"",value:"",disabled:false,offsetWidth:220,offsetHeight:180,
    classList:{add(){},remove(){},toggle(){},contains(){return false;}},
    addEventListener(){},focus(){},setAttribute(){},getAttribute(){return null;},
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

console.log("Story smoke test passed: bosses, victory, unlimited nights, rarity HP, counterattacks, and completed saves.");

