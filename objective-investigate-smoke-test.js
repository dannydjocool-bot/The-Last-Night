const fs=require('fs');
const vm=require('vm');

const html=fs.readFileSync('index.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes=new Map();
function node(){return {style:{},innerHTML:'',textContent:'',value:'',disabled:false,offsetWidth:220,offsetHeight:180,classList:{add(){},remove(){},toggle(){},contains(){return false;}},addEventListener(){},focus(){},setAttribute(){},getAttribute(){return null;},appendChild(){},remove(){},querySelector(){return null;},querySelectorAll(){return [];},getBoundingClientRect(){return {left:0,top:0,width:220,height:180}}};}
const document={body:node(),documentElement:node(),head:node(),readyState:'complete',getElementById(id){if(!nodes.has(id))nodes.set(id,node());return nodes.get(id);},querySelector(){return null;},querySelectorAll(){return [];},addEventListener(){},createElement(){return node();},createTextNode(){return node();}};
const storage=new Map();
const localStorage={getItem:k=>storage.has(k)?storage.get(k):null,setItem:(k,v)=>storage.set(k,String(v)),removeItem:k=>storage.delete(k)};
const context={console,document,localStorage,setTimeout:fn=>{fn();return 1;},clearTimeout(){},Date,Math:Object.create(Math),JSON,Set,Infinity,window:null,location:{reload(){}},navigator:{userAgent:'CI'},requestAnimationFrame:fn=>{fn();return 1;},cancelAnimationFrame(){},getComputedStyle(){return {};},matchMedia(){return {matches:false,addEventListener(){},removeEventListener(){}}}};
context.Math.random=Math.random;
context.window=context;context.innerWidth=1400;context.innerHeight=900;context.addEventListener=()=>{};
vm.createContext(context);vm.runInContext(script,context);
function run(code){return vm.runInContext(code,context)}
function assert(v,msg){if(!v)throw new Error(msg)}

function freshGame(loc='station'){
  run(`render=()=>{};renderLog=()=>{};combat=null;G={ps:[{name:'Tester',dead:false,actions:10,loc:'${loc}',freeInvestigateUsed:false,items:[]}],active:0,night:1,clues:0,foundClues:new Set(),discovered:new Set(['motel','gas','forest','station']),wardenDefeated:false,hollowDefeated:false,bloodkeeperDefeated:false,sentinelDefeated:false,rootEntered:false,rootGateMinionsDefeated:[],rootGateUnlocked:false,rootFusionDefeated:false,rootDefeated:false,storyItems:[],creatures:[],extraPockets:[],extraPocketMax:30,flashlightUsedLocations:new Set(),ammo:{pistol:0,shotgun:0,smg:0,rifle:0},log:[]};updateStoryObjective();`);
}

assert(html.includes('onclick="window.performObjectiveInvestigate()"'), 'Rendered Investigate button is not wired to the dedicated handler');
assert(run(`typeof window.performObjectiveInvestigate==='function'`), 'Dedicated Investigate handler is not available on window');

// Search must NEVER advance story clues, even on its best roll.
freshGame('station');
run(`let oldRandom=Math.random;Math.random=()=>0.999999;search();Math.random=oldRandom;`);
assert(run(`G.clues===0&&!G.foundClues.has('station')`), 'Search incorrectly advanced a story objective');
assert(nodes.get('storyObjectiveText').innerHTML.includes('Objective 1'), 'Search incorrectly changed the Story Objective');

// Exact visible-button flow: Objective 1 -> Police Station -> button handler.
freshGame('station');
assert(nodes.get('storyObjectiveText').innerHTML.includes('Objective 1'), 'Objective 1 was not shown before investigation');
assert(run(`window.performObjectiveInvestigate()===true`), 'Visible Investigate button handler did not report success');
assert(run(`G.clues===1&&G.foundClues.has('station')`), 'Visible Investigate button handler did not advance clue state');
assert(nodes.get('storyObjectiveText').innerHTML.includes('Objective 2'), 'Story Objective did not advance to Objective 2');
assert(run(`G.ps[0].freeInvestigateUsed===true&&G.ps[0].actions===10`), 'Free first investigation did not remain free');
const storyLog=run(`G.log.join(' ')`);
assert(storyLog.includes('STORY CLUE FOUND'), 'Investigate did not show the discovered story clue');
assert(storyLog.includes('NEXT LEAD:'), 'Investigate did not show the next story lead');
assert(!storyLog.includes('Objective advanced:'), 'Developer-style numeric objective feedback leaked into player log');

// Wrong location must not waste the free Investigate or AP.
run(`G.ps[0].loc='motel';G.ps[0].freeInvestigateUsed=false;G.ps[0].actions=10;`);
assert(run(`window.performObjectiveInvestigate()===false`), 'Wrong-location button press incorrectly advanced');
assert(run(`G.clues===1&&G.ps[0].freeInvestigateUsed===false&&G.ps[0].actions===10`), 'Failed Investigate consumed progress/AP');

// Compatibility alias must still work for old internal calls.
assert(run(`typeof investigate==='function'`), 'Investigate compatibility alias is missing');

console.log('Visible Investigate button/Search authority and immersive story feedback test passed.');