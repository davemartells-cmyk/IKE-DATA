// Play-by-play leaderboard totals for every SIMHL player, counted by the Empire tool's own game reader.
// node simhl_lead.js <empire_engine.html> <SIMHL data dir> <out.json>
const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
(async()=>{
 const [html,dir,out]=process.argv.slice(2);
 const idx=JSON.parse(fs.readFileSync(path.join(dir,'IKE_SIMHL_Season.json'),'utf8'));
 const files=[['SIMHL/IKE_SIMHL_Season.json',fs.readFileSync(path.join(dir,'IKE_SIMHL_Season.json'),'utf8')]];
 for(const g of idx.games){ const f=path.join(dir,g.file); if(fs.existsSync(f)) files.push(['SIMHL/'+g.file,fs.readFileSync(f,'utf8')]); }
 const b=await chromium.launch(); const p=await b.newPage();
 await p.addInitScript(()=>{ window.IKE_NO_ONLINE=true; window.IKE_NO_BUILTIN=true; });
 await p.goto('file://'+path.resolve(html),{timeout:120000}); await p.waitForFunction(()=>typeof ikeFolderPick==='function'&&document.getElementById('lfoldTeam'),null,{timeout:120000});
 await p.evaluate(async(files)=>{ const list=files.map(([pth,txt])=>{const f=new File([txt],pth.split('/').pop());Object.defineProperty(f,'webkitRelativePath',{value:pth});return f;});
   await ikeFolderPick({target:{files:list,value:''}}); },files);
 const teams=await p.evaluate(()=>[...document.getElementById('lfoldTeam').options].map(o=>o.value));
 const res=await p.evaluate(async(teams)=>{
   const F=[['int','fpbpInterceptions'],['cmp','fpbpCompleted'],['pas','fpbpPasses'],['dfl','dfl'],['post','post'],['sa','sa'],['take','take'],['give','give'],['blk','blk'],['dump','fpbpDumpIns'],['hit','hg'],['g','g'],['a1','a1'],['a2','a2']];
   const A={}, G={}, CL={};
   const H=[['g','g'],['a1','a1'],['a2','a2'],['hit','hg'],['blk','blk'],['take','take'],['give','give'],['sa','sa'],['sog','sog'],['pm','pm'],['pim','pim'],['fw','fw'],['fl','fl'],['int','fpbpInterceptions'],['cmp','fpbpCompleted'],['pas','fpbpPasses']];
   for(const club of teams){ await ikeFolderTeam(club);
     for(const r of DB){ const pb=!!(r.fullPbp&&r.fullPbp.found), P=r.players||{};
       const t=Date.parse(String(r.created||'').replace(/ at /,' '))||0; (CL[club]=CL[club]||[]).push(t);
       for(const n in P){ if(!n||n==='null') continue; const s=P[n]; (G[n]=G[n]||[]).push([t,club,pb?1:0].concat(H.map(([k,f])=>+(s[f]||0)))); }
       for(const n in P){ if(!n||n==='null') continue; const s=P[n];
         const a=A[n]||(A[n]={gp:0,pg:0,cl:[],ow:0,ol:0,nw:0,nl:0,dw:0,dl:0}); F.forEach(([k])=>{ if(a[k]==null) a[k]=0; });
         a.gp++; if(pb) a.pg++; if(a.cl.indexOf(club)<0) a.cl.push(club); F.forEach(([k,f])=>{ a[k]+=+(s[f]||0); }); }
       (r.ev||[]).forEach(e=>{ if(e.ty!=='Faceoff Win'&&e.ty!=='Faceoff Loss') return; if(!P[e.p]||!/^(OZ|NZ|DZ)$/.test(e.zone||'')) return;
         A[e.p][e.zone[0].toLowerCase()+(e.ty==='Faceoff Win'?'w':'l')]++; }); } }
   const cols=['gp','pg','cl'].concat(F.map(x=>x[0])).concat(['ow','ol','nw','nl','dw','dl']), o={};
   Object.keys(A).forEach(n=>{ const a=A[n]; o[n]=cols.map(c=>c==='cl'?a.cl.join('|'):a[c]); });
   /* last 10: each player's games inside his current club's last 10 game dates */
   const cut={}; Object.keys(CL).forEach(c=>{ const ts=CL[c].slice().sort((a,b)=>b-a); cut[c]=ts[Math.min(9,ts.length-1)]; });
   const l10={cols:['gp','pg'].concat(H.map(x=>x[0])),p:{}};
   Object.keys(G).forEach(n=>{ const g=G[n].slice().sort((a,b)=>a[0]-b[0]); const last=g[g.length-1]; const c=cut[last[1]];
     const sel=g.filter(x=>x[0]>=c).slice(-10); if(!sel.length) return;
     const sum=H.map((_,i)=>sel.reduce((s,x)=>s+x[3+i],0)); l10.p[n]=[sel.length,sel.reduce((s,x)=>s+x[2],0)].concat(sum); });
   /* cold streaks: games in a row, back from his latest game, without a goal (ng) and without a point (np) */
   const st={cols:['ng','np'],p:{}};
   Object.keys(G).forEach(n=>{ const g=G[n].slice().sort((a,b)=>a[0]-b[0]); let ng=0,np=0;
     for(let i=g.length-1;i>=0&&!(g[i][3]>0);i--) ng++;
     for(let i=g.length-1;i>=0&&!((g[i][3]+g[i][4]+g[i][5])>0);i--) np++;
     st.p[n]=[ng,np]; });
   return {cols:cols,p:o,l10:l10,st:st}; },teams);
 res.game=idx.lastGameSynced; res.day=idx.lastDaySynced;
 fs.writeFileSync(out,JSON.stringify(res)); console.log('players',Object.keys(res.p).length,'clubs',teams.length); await b.close();
})();
