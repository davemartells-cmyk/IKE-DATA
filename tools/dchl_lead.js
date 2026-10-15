// Play-by-play leaderboard totals for every DCHL player, counted by the IKE (DCHL) app's own game reader.
// node dchl_lead.js <dchl_engine.html> <DCHL data dir> <out.json>
const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
(async()=>{
 const [html,dir,out]=process.argv.slice(2);
 const idx=JSON.parse(fs.readFileSync(path.join(dir,'IKE_DCHL_Season.json'),'utf8'));
 const files=[['DCHL/IKE_DCHL_Season.json',fs.readFileSync(path.join(dir,'IKE_DCHL_Season.json'),'utf8')]];
 for(const g of idx.games){ const f=path.join(dir,g.file); if(fs.existsSync(f)) files.push(['DCHL/'+g.file,fs.readFileSync(f,'utf8')]); }
 const b=await chromium.launch(); const p=await b.newPage();
 await p.addInitScript(()=>{ window.IKE_NO_ONLINE=true; window.IKE_NO_BUILTIN=true; });
 await p.goto('file://'+path.resolve(html),{timeout:120000}); await p.waitForFunction(()=>typeof ikeFolderPick==='function'&&document.getElementById('lfoldTeam'),null,{timeout:120000});
 await p.evaluate(async(files)=>{ const list=files.map(([pth,txt])=>{const f=new File([txt],pth.split('/').pop());Object.defineProperty(f,'webkitRelativePath',{value:pth});return f;});
   await ikeFolderPick({target:{files:list,value:''}}); },files);
 const teams=await p.evaluate(()=>[...document.getElementById('lfoldTeam').options].map(o=>o.value));
 const res=await p.evaluate(async(teams)=>{
   const F=[['int','fpbpInterceptions'],['cmp','fpbpCompleted'],['pas','fpbpPasses'],['dfl','dfl'],['post','post'],['sa','sa'],['take','take'],['give','give'],['blk','blk'],['dump','fpbpDumpIns'],['hit','hg'],['g','g'],['a1','a1'],['a2','a2']];
   const A={};
   for(const club of teams){ await ikeFolderTeam(club);
     for(const r of DB){ const pb=!!(r.fullPbp&&r.fullPbp.found), P=r.players||{};
       for(const n in P){ if(!n||n==='null') continue; const s=P[n];
         const a=A[n]||(A[n]={gp:0,pg:0,cl:[],ow:0,ol:0,nw:0,nl:0,dw:0,dl:0}); F.forEach(([k])=>{ if(a[k]==null) a[k]=0; });
         a.gp++; if(pb) a.pg++; if(a.cl.indexOf(club)<0) a.cl.push(club); F.forEach(([k,f])=>{ a[k]+=+(s[f]||0); }); }
       (r.ev||[]).forEach(e=>{ if(e.ty!=='Faceoff Win'&&e.ty!=='Faceoff Loss') return; if(!P[e.p]||!/^(OZ|NZ|DZ)$/.test(e.zone||'')) return;
         A[e.p][e.zone[0].toLowerCase()+(e.ty==='Faceoff Win'?'w':'l')]++; }); } }
   const cols=['gp','pg','cl'].concat(F.map(x=>x[0])).concat(['ow','ol','nw','nl','dw','dl']), o={};
   Object.keys(A).forEach(n=>{ const a=A[n]; o[n]=cols.map(c=>c==='cl'?a.cl.join('|'):a[c]); });
   return {cols:cols,p:o}; },teams);
 res.game=idx.lastGameSynced; res.day=idx.lastDaySynced;
 fs.writeFileSync(out,JSON.stringify(res)); console.log('players',Object.keys(res.p).length,'clubs',teams.length); await b.close();
})();
