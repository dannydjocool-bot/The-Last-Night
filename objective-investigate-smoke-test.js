const fs=require('fs');
const vm=require('vm');

const html=fs.readFileSync('index.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes=new Map();
function node(){return {style:{},innerHTML:'',textContent:'',value:'',disabled:false,offsetWidth:220,offsetHeight:180,classList:{add(){},remove(){},toggle(){},contains(){return false;}},addEventListener(){},focus(){},setAttribute(){},getAttribute(){return null;},appendChild(){},remove(){},querySelector(){return null;},querySelectorAll(){return [];},getBoundingClientRect(){return {left:0,top:0,width:220,height:180}}};}
const document={body:node(),documentElement:node(),head:node(),readyState:'complete',getElementById(id){if(!nodes.has(id))nodes.set(id,node());return nodes.get(id);},querySelector(){return null;},querySelectorAll(){return [];},addEventListener(){},createElement(){return node();},createTextNode(){return node();}};
const storage=new Map();
const localStorage={getItem:k=>storage.has(k)?storage.get(k):null,setItem:(k,v)=>storage.set(k,String(v)),removeItem:k=>storage.delete(k)};
const context={console,document,localStorage,setTimeout:fn=>{fn();return 1;},clearTimeout(){},Date,Math,JSON,Set,Infinity,window:null,location:{reload(){}},navigator:{userAgent:'CI'},requestAnimationFrame:fn=>{fn();return 1;},cancelAnimationFrame(){},getComputedStyle(){return {};},matchMedia(){return {matches:false,addEventListener(){},removeEventListener(){}}}};
context.window=context;context.innerWidth=1400;context.innerHeight=900;context.addEventListener=()=>{};
vm.createContext(context);vm.runInContext(script,context);
function run(code){return vm.runInContext(code,context)}
function assert(v,msg){if(!v)throw new Error(msg)}

// Exact player flow: Objective 1 -> Police Station -> Investigate.
run(`render=()=>{};renderLog=()=>{};combat=null;G={ps:[{name:'Tester',dead:false,actions:10,loc:'station',freeInvestigateUsed:false}],active:0,night:1,clues:0,foundClues:new Set(),discovered:new Set(['motel','gas','forest','station']),wardenDefeated:false,hollowDefeated:false,bloodkeeperDefeated:false,sentinelDefeated:false,rootEntered:false,rootGateMinionsDefeated:[],rootGateUnlocked:false,rootFusionDefeated:false,rootDefeated:false,storyItems:[],creatures:[],extraPockets:[],extraPocketMax:30,flashlightUsedLocations:new Set(),ammo:{pistol:0,shotgun:0,smg:0,rifle:0},log:[]};updateStoryObjective();`);
assert(nodes.get('storyObjectiveText').innerHTML.includes('Objective 1'), 'Objective 1 was not shown before investigation');
assert(run(`investigate()===true`), 'Investigate did not report a successful objective investigation');
assert(run(`G.clues===1&&G.foundClues.has('station')`), 'Investigate did not advance clue state');
assert(nodes.get('storyObjectiveText').innerHTML.includes('Objective 2'), 'Story Objective did not advance to Objective 2');
assert(run(`G.ps[0].freeInvestigateUsed===true&&G.ps[0].actions===10`), 'Free first investigation did not remain free');

// Wrong location must not waste the free Investigate or AP.
run(`G.ps[0].loc='motel';G.ps[0].freeInvestigateUsed=false;G.ps[0].actions=10;`);
assert(run(`investigate()===false`), 'Wrong-location Investigate incorrectly advanced');
assert(run(`G.clues===1&&G.ps[0].freeInvestigateUsed===false&&G.ps[0].actions===10`), 'Failed Investigate consumed progress/AP');

// Old/stale save metadata should reconcile to ordered clue progress.
run(`G.foundClues=new Set(['station']);G.clues=0;G.ps[0].loc='station';updateStoryObjective();investigate();`);
assert(run(`G.clues===1`), 'Stale save clue count was not repaired');
assert(nodes.get('storyObjectiveText').innerHTML.includes('Objective 2'), 'Stale save objective did not repair to Objective 2');

console.log('Objective Investigate smoke test passed.');