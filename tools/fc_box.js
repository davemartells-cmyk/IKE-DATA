// Forecasting data straight from each game sheet's box score: every row is a game played (the league's GP count).
// Returns {c:{player:[[club,gp,g,a],...]}, r:{player:[[day,club,g,a],...last 10, oldest first]}}
module.exports=function(games,textOf){
  const FC={}, esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  const POS=/^(?:C|LW|RW|D)(?:\/(?:C|LW|RW|D))*$/;
  for(const g of games){ const t=textOf(g); if(!t) continue; const clubs=[g.visitor,g.home];
    for(const club of clubs){ let rows=[];
      // DCHL layout: "<Club>\nPlayer Name\tPOS\tG\tA..." (header sometimes broken over lines), tab rows
      const m=new RegExp('\\n'+esc(club)+'\\r?\\nPlayer Name').exec(t);
      if(m){ const other=clubs.filter(c=>c!==club).map(c=>new RegExp('\\n'+esc(c)+'\\r?\\nPlayer Name').exec(t.slice(m.index+5))).filter(Boolean).map(x=>x.index+m.index+5);
        const end=other.length?Math.min(...other):t.length, sec=t.slice(m.index+1,end);
        sec.split(/\r?\n/).forEach(l=>{ const c=l.split('\t'); if(c.length>=5&&c[0].trim()&&POS.test(c[1].trim())&&/^\d+$/.test(c[2])&&/^\d+$/.test(c[3])) rows.push([c[0].trim(),+c[2],+c[3]]); }); }
      else { // SIMHL layout: "Players Stats for <Club>" then fixed-width rows up to a blank line
        const k=t.indexOf('Players Stats for '+club+'\n'); if(k<0) continue;
        const sec=t.slice(k).split(/\r?\n/).slice(3);
        for(const l of sec){ if(!l.trim()) break; const x=/^(.+?)\s{2,}(\d+)\s+(\d+)\s+(\d+)\s+-?\d+\s/.exec(l); if(x) rows.push([x[1].trim(),+x[2],+x[3]]); } }
      rows.forEach(([n,G,A])=>{ (FC[n]=FC[n]||[]).push([g.game,g.day,club,G,A]); }); } }
  const out={c:{},r:{}};
  Object.keys(FC).forEach(n=>{ const L=FC[n].sort((a,b)=>a[0]-b[0]), by={}, order=[];
    L.forEach(x=>{ if(!by[x[2]]){ by[x[2]]=[x[2],0,0,0]; order.push(x[2]); } const b=by[x[2]]; b[1]++; b[2]+=x[3]; b[3]+=x[4]; });
    out.c[n]=order.map(c=>by[c]); out.r[n]=L.slice(-10).map(x=>[x[1],x[2],x[3],x[4]]); });
  return out;
};
