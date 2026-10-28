// IKE daily pull helpers. Paste into the Claude browser pane (javascript_tool) on a page of the league site.
// DCHL: run on https://dchl.sths.ca/... (must be signed in for box scores).
// SIMHL: run on https://nhl.simhl.net/File/2026-RegularSeason/...
window.gz = async function(txt){ const cs=new Blob([txt]).stream().pipeThrough(new CompressionStream('gzip')); const buf=new Uint8Array(await new Response(cs).arrayBuffer()); let s=''; for(let i=0;i<buf.length;i+=0x8000) s+=String.fromCharCode.apply(null,buf.subarray(i,i+0x8000)); return btoa(s); };
window.frameText = async function(url, showTabs){ const f=document.createElement('iframe'); f.style.cssText='position:absolute;left:-9999px;width:1400px;height:900px'; document.body.appendChild(f); await new Promise(r=>{f.onload=r; f.src=url;}); const d=f.contentDocument; if(showTabs) d.querySelectorAll('.tabmain').forEach(e=>e.style.display='block'); const txt=d.body.innerText, title=d.title; f.remove(); return {txt,title}; };

// ---- DCHL: the seven STHS table exports, shaped to the exact columns the IKE DCHL build reads ----
window.csvFrom = async function(url, hidden){ const f=document.createElement('iframe'); f.style.cssText='position:absolute;left:-99999px;width:4000px;height:900px'; document.body.appendChild(f); await new Promise(r=>{f.onload=r; f.src=url;}); const w=f.contentWindow; let t=null; for(let i=0;i<60;i++){ t=[...f.contentDocument.querySelectorAll('table')].find(x=>x.config&&x.config.widgetOptions&&('output_saveFileName' in x.config.widgetOptions)); if(t) break; await new Promise(r=>setTimeout(r,200)); } if(!t){f.remove(); throw new Error('no export table on '+url);} const wo=t.config.widgetOptions; wo.output_hiddenColumns=!!hidden; let data=null; wo.output_callback=function(c,d){ data=d; return false; }; w.jQuery(t).trigger('outputTable'); for(let i=0;i<80&&data===null;i++) await new Promise(r=>setTimeout(r,100)); const name=wo.output_saveFileName; f.remove(); if(data===null) throw new Error('export failed on '+url); return {name,csv:data}; };
window.csvRows = function(text){ const rows=[]; let row=[],f='',q=false; for(let i=0;i<text.length;i++){ const c=text[i]; if(q){ if(c=='"'){ if(text[i+1]=='"'){f+='"';i++;} else q=false; } else f+=c; } else if(c=='"') q=true; else if(c==','){row.push(f);f='';} else if(c=='\n'||c=='\r'){ if(c=='\r'&&text[i+1]=='\n') i++; row.push(f); rows.push(row); row=[]; f=''; } else f+=c; } if(f!==''||row.length){row.push(f);rows.push(row);} return rows; };
window.csvCell = function(v){ v=String(v==null?'':v); return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v; };
window.csvShape = function(text, want){ const rows=csvRows(text); const h=rows[0].map(x=>String(x).trim()); const used={}; const idx=want.map(w=>{ const from=used[w]||0; for(let i=from;i<h.length;i++){ if(h[i]===w){ used[w]=i+1; return i; } } return -1; }); return rows.filter(r=>r.length>1||String(r[0]).trim()!=='').map((r,ri)=> ri===0? want.map(csvCell).join(',') : idx.map(i=> i<0?'':csvCell(r[i])).join(',')).join('\n'); };
window.DCHL_EXPORTS = [
 {file:'STHSTeamStat.CSV', url:'/TeamsStat.php', hidden:true, cols:'#,Team,GP,W,L,T,OTW,OTL,SOW,SOL,GF,GA,Diff,GP,W,L,T,OTW,OTL,SOW,SOL,GF,GA,Diff,GP,W,L,T,OTW,OTL,SOW,SOL,GF,GA,Diff,P,PCT,G,A,TP,SO,EG,GP1,GP2,GP3,GP4,SHF,SH1,SP2,SP3,SP4,SHA,SHB,Pim,Hit,PPA,PPG,PP%,PKA,PK GA,PK%,PK GF,W OF FO,T OF FO,OF FO%,W DF FO,T DF FO,DF FO%,W NT FO,T NT FO,NT FO%,PZ DF,PZ OF,PZ NT,PC DF,PC OF,PC NT'},
 {file:'STHSSchedule.CSV', url:'/Schedule.php', hidden:false, cols:'Day,Game,Visitor Team,Score,Home Team,Score,OT,SO,RI,Link'},
 {file:'STHSPlayerStat.CSV', url:'/PlayersStat.php', hidden:true, cols:'#,Player Name,Team Name,POS,GP,G,A,P,+/-,PIM,PIM5,HIT,HTT,SHT,OSB,OSM,SHT%,SB,MP,AMG,PPG,PPA,PPP,PPS,PPM,PKG,PKA,PKP,PKS,PKM,GW,GT,FO%,FOT,EG,HT,P/20,PSG,PSS,FW,FL,FT,S1,S2,S3'},
 {file:'STHSPlayerInformation.CSV', url:'/PlayersInfo.php', hidden:false, cols:'Player Name,Team Name,POS,Age,Birthday,Rookie,Weight,Height,No Trade,Available For Trade,Acquired By,Last Trade Date,Contract,Contract Signature Date,Current Salary,Salary Remaining,Salary Cap,Salary Cap Remaining,Link'},
 {file:'STHSPlayerRoster.CSV', url:'/PlayersRoster.php', hidden:false, cols:'Player Name,Team Name,C,L,R,D,CK,FG,DI,SK,ST,EN,DU,PH,FO,PA,SC,DF,PS,EX,LD,PO,MO,OV,Age,Contract,Salary,Link'},
 {file:'STHSGoalieStat.CSV', url:'/GoaliesStat.php', hidden:false, cols:'#,Goalie Name,Team Name,GP,W,L,OTL,PCT,GAA,MP,PIM,SO,GA,SA,SAR,A,EG,PS %,PSA'},
 {file:'STHSGoaliesRoster.CSV', url:'/GoaliesRoster.php', hidden:false, cols:'Goalie Name,Team Name,SK,DU,EN,SZ,AG,RB,SC,HS,RT,PH,PS,EX,LD,PO,MO,OV,Age,Contract,Salary,Link'}
];

window.IKE = {
  league: location.host.indexOf('dchl')>=0 ? 'DCHL' : 'SIMHL',
  // played game numbers
  played: async function(){
    if(IKE.league==='DCHL'){ const s=await fetch('/API.php?SchedulePro').then(r=>r.json()); return s.filter(x=>x.Play=="True").map(x=>+x.GameNumber).sort((a,b)=>a-b); }
    const t=await fetch('SIMHL-Schedule.html').then(r=>r.text()); return [...new Set([...t.matchAll(/href="SIMHL-(\d+)\.html"/g)].map(m=>+m[1]))].sort((a,b)=>a-b);
  },
  game: async function(n){ const url = IKE.league==='DCHL' ? '/Boxscore.php?Game='+n : 'SIMHL-'+n+'.html'; const r=await frameText(url, IKE.league==='DCHL'); return {n, title:r.title, len:r.txt.length, gz:await gz(r.txt)}; },
  // games newer than `after`, at most `max` per call -> JSON string
  games: async function(after, max){ max=max||30; const list=(await IKE.played()).filter(n=>n>after).slice(0,max); if(!list.length) return 'NONE'; const out=[]; let i=0; async function w(){ while(i<list.length){ const n=list[i++]; let r; for(let k=0;k<3;k++){ try{ r=await IKE.game(n); if(r.len>3000) break; }catch(e){ r={n,err:String(e)}; } } out.push(r);} } await Promise.all([w(),w(),w(),w()]); out.sort((a,b)=>a.n-b.n); out.push(IKE.pad()); return JSON.stringify(out); },
  // snapshot: builds IKE.CH chunks (<=180K chars each); return them with IKE.chunk(i)
  snapshot: async function(){ const S={};
    if(IKE.league==='DCHL'){ const q={PlayerRoster:'PlayerRoster',GoalerRoster:'GoalerRoster',PlayerInfo:'PlayerInfo',PlayerStatPro:'PlayerStatPro&MinGP=0',GoalerStatPro:'GoalerStatPro&MinGP=0',StandingPro:'StandingPro',TeamStatPro:'TeamStatPro',SchedulePro:'SchedulePro',Transaction:'Transaction',CoachesPro:'CoachesPro',Waiver:'Waiver'};
      for(const [k,v] of Object.entries(q)) S[k]=await gz(await fetch('/API.php?'+v).then(r=>r.text()));
      for(const x of DCHL_EXPORTS){ const r=await csvFrom(x.url,x.hidden); S['CSV:'+x.file]=await gz(csvShape(r.csv, x.cols.split(','))); }
      const L=[]; for(let t=1;t<=30;t++) L.push((await fetch('/API.php?TeamProLines&Team='+t).then(r=>r.text())).trim().replace(/^\[|\]$/g,'')); S.TeamProLines=await gz('['+L.join(',')+']');
    } else { for(const f of ['SIMHL-Players.csv','SIMHL-Goalies.csv','SIMHL-Coaches.csv','SIMHL-ProSchedule.csv']) S['CSV:'+f]=await gz(await fetch(f).then(r=>r.text()));
      for(const p of ['ProTeamRoster','ProTeamLines','ProTeamPlayersInfo','ProStanding','Schedule','ProTeamScoring','ProTeamStats','TeamInjurySuspension','Coaches','Transactions','TeamsAndGMInfo']) S['SIMHL-'+p]=await gz((await frameText('SIMHL-'+p+'.html',false)).txt); }
    IKE.CH=[]; const SZ=180000; for(const [k,v] of Object.entries(S)){ const tot=Math.ceil(v.length/SZ)||1; for(let i=0;i<tot;i++) IKE.CH.push({n:k,i,tot,d:v.slice(i*SZ,(i+1)*SZ)}); }
    return IKE.CH.map((c,i)=>i+':'+c.n+'#'+c.i+'/'+c.tot+' '+Math.round(c.d.length/1024)+'KB').join(' | '); },
  chunk: function(idxs){ return JSON.stringify(idxs.map(i=>IKE.CH[i]).concat([IKE.pad()])); },
  // filler so every result is large enough to be saved as a file by the tool (ignored by ike_ingest.py)
  pad: function(){ return {n:-1, pad:'x'.repeat(300000)}; }
};
// save a result as a file through the browser's normal download (for a browser outside Claude: IKE.save('dchl_games_946.json', await IKE.games(945,9)))
IKE.save = function(name, text){ const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([text],{type:'application/json'})); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove();},5000); return 'saved '+name+' ('+Math.round(text.length/1024)+' KB)'; };
IKE.chunkAll = function(){ return IKE.chunk(IKE.CH.map((_,i)=>i)); };
'IKE helpers loaded for '+IKE.league;
