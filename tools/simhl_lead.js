// Play-by-play leaderboard totals for every SIMHL player, counted by the Empire tool's own game reader.
// node simhl_lead.js <empire_engine.html> <SIMHL data dir> <out.json>
const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
(async()=>{
 const [html,dir,out]=process.argv.slice(2);
 const idx=JSON.parse(fs.readFileSync(path.join(dir,'IKE_SIMHL_Season.json'),'utf8'));
 const files=[['SIMHL/IKE_SIMHL_Season.json',fs.readFileSync(path.join(dir,'IKE_SIMHL_Season.json'),'utf8')]];
 for(const g of idx.games){ const f=path.join(dir,g.file); if(fs.existsSync(f)) files.push(['SIMHL/'+g.file,fs.readFileSync(f,'utf8')]); }
 /* league day of every sheet, keyed by its title and Created line (the reader keeps both on each game) */
 const DAY={}; for(const [pth,txt] of files){ const m=/^([^\n]+)\r?\nCreated - ([^\n]+)/m.exec(txt); if(!m) continue; const g=idx.games.find(x=>'SIMHL/'+x.file===pth); if(g) DAY[m[1].trim()+'|'+m[2].trim()]=g.day; }
 const b=await chromium.launch(); const p=await b.newPage();
 await p.addInitScript(()=>{ window.IKE_NO_ONLINE=true; window.IKE_NO_BUILTIN=true; });
 await p.goto('file://'+path.resolve(html),{timeout:120000}); await p.waitForFunction(()=>typeof ikeFolderPick==='function'&&document.getElementById('lfoldTeam'),null,{timeout:120000});
 await p.evaluate(async(files)=>{ const list=files.map(([pth,txt])=>{const f=new File([txt],pth.split('/').pop());Object.defineProperty(f,'webkitRelativePath',{value:pth});return f;});
   await ikeFolderPick({target:{files:list,value:''}}); },files);
 const teams=await p.evaluate(()=>[...document.getElementById('lfoldTeam').options].map(o=>o.value));
 const res=await p.evaluate(async([teams,DAY])=>{
   const F=[['int','fpbpInterceptions'],['cmp','fpbpCompleted'],['pas','fpbpPasses'],['dfl','dfl'],['post','post'],['sa','sa'],['take','take'],['give','give'],['blk','blk'],['dump','fpbpDumpIns'],['hit','hg'],['g','g'],['a1','a1'],['a2','a2']];
   const SP={}, SP10={}, LOG={};
   const A={}, G={}, CL={};
   const FC={}; /* Oct 23 Forecasting: every game a player dressed in, with his club, league day, goals and assists */
   const H=[['g','g'],['a1','a1'],['a2','a2'],['hit','hg'],['blk','blk'],['take','take'],['give','give'],['sa','sa'],['sog','sog'],['pm','pm'],['pim','pim'],['fw','fw'],['fl','fl'],['int','fpbpInterceptions'],['cmp','fpbpCompleted'],['pas','fpbpPasses']];
   for(const club of teams){ await ikeFolderTeam(club);
     /* Oct 23: every club's points by P-D-O system (season and last 10) and its scoring log, read from its own game sheets */
     try{ const codes=(window.SYS21||[]).map(s=>s.code), keep=window.DB, ts=r=>Date.parse(String(r.created||'').replace(/ at /,' '))||0;
       const agg=(list)=>{ const o={}; window.DB=list; try{ codes.forEach(c=>{ const R=window.ikeSysAgg(c).A, T=R.TOTAL; if(T.gp) o[c]=[T.gp,T.pts,R.HOME.pts,R.AWAY.pts,T.evg,T.ppg,T.shg,T.eva,T.ppa,T.sha]; }); } finally { window.DB=keep; } return o; };
       if(window.ikeSysAgg){ SP[club]=agg(keep.slice()); SP10[club]=agg(keep.slice().sort((a,b)=>ts(a)-ts(b)).slice(-10)); }
       LOG[club]=[]; keep.forEach(r=>{ const P=r.players||{}, L=(r.systems&&r.systems.lines)||{}, D=(r.systems&&r.systems.pairs)||{}, t=String(r.title||'').split(' vs '), opp=t[0]===club?t[1]:t[0];
         (r.goals||[]).forEach(go=>{ const p=P[go.scorer]||{}, code=(p.lineNumber&&L[p.lineNumber])||(p.pairNumber&&D[p.pairNumber])||'';
           LOG[club].push([ts(r),opp||'',r.road?1:0,go.per||0,go.clk||go.t||'',go.str||(go.tag==='PP'?'PP':go.tag==='SH'?'PK':'EV'),go.scorer||'',go.a1||'',go.a2||'',code,DAY[String(r.title||'').trim()+'|'+String(r.created||'').trim()]||0]); }); }); }catch(e){ console.error('sysp',club,e); }
     for(const r of DB){ const pb=!!(r.fullPbp&&r.fullPbp.found), P=r.players||{};
       const t=Date.parse(String(r.created||'').replace(/ at /,' '))||0; (CL[club]=CL[club]||[]).push(t);
       { const dy=DAY[String(r.title||'').trim()+'|'+String(r.created||'').trim()]||0, GG={}, AA={}; (r.goals||[]).forEach(x=>{ if(x.scorer) GG[x.scorer]=(GG[x.scorer]||0)+1; [x.a1,x.a2].forEach(q=>{ if(q) AA[q]=(AA[q]||0)+1; }); });
         for(const n in P){ if(!n||n==='null') continue; (FC[n]=FC[n]||[]).push([t,dy,club,GG[n]||0,AA[n]||0]); } }
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
   /* Forecasting: per-club totals [club,gp,g,a] and his own 10 most recent games, any club, oldest first [day,club,g,a] */
   const fc={c:{},r:{}}; Object.keys(FC).forEach(n=>{ const g=FC[n].slice().sort((a,b)=>(a[0]-b[0])||(a[1]-b[1])), by={};
     g.forEach(x=>{ const b=by[x[2]]||(by[x[2]]=[x[2],0,0,0,x[0]]); b[1]++; b[2]+=x[3]; b[3]+=x[4]; b[4]=x[0]; });
     fc.c[n]=Object.values(by).sort((a,b)=>a[4]-b[4]).map(b=>b.slice(0,4)); fc.r[n]=g.slice(-10).map(x=>[x[1],x[2],x[3],x[4]]); });
   return {cols:cols,p:o,l10:l10,st:st,fc:fc,sysp:{cols:['gp','pts','h','r','evg','ppg','shg','eva','ppa','sha'],season:SP,last10:SP10},log:{cols:['t','opp','road','per','clk','str','g','a1','a2','sys','day'],c:LOG}}; },[teams,DAY]);
 /* Forecasting split and last 10 come from the box-score rows themselves, so GP matches the league's count */
 const FT={}; for(const [pth,txt] of files) FT[pth]=txt;
 res.fc=require('./fc_box.js')(idx.games,g=>FT['SIMHL/'+g.file]);
 res.game=idx.lastGameSynced; res.day=idx.lastDaySynced;
 fs.writeFileSync(out,JSON.stringify(res)); console.log('players',Object.keys(res.p).length,'clubs',teams.length); await b.close();
})();
