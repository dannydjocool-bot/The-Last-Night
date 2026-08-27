/* The Last Night — shared runtime state and random helpers. */

let G=null;
let combat=null;
const d6=()=>1+Math.floor(Math.random()*6);
const rnd=a=>a[Math.floor(Math.random()*a.length)];
