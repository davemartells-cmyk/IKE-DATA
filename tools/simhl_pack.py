"""Builds the SIMHL data pack the Empire Edition reads online.
python3 -I simhl_pack.py <SIMHL data dir> <lead.json> <out dir>
Writes <out>/ike_simhl_pack.json.gz (index, every game sheet, team stats, schedule, player and goalie files,
play-by-play leaders, the league's own team table, goals and shots by period, every club's strategy usage and
the last game day's stars) and <out>/latest.json (what the pack holds)."""
import csv,io,re,json,gzip,os,sys,glob
src,leadf,out=sys.argv[1:4]
idx=json.load(open(os.path.join(src,'IKE_SIMHL_Season.json'),encoding='utf-8'))
snaps=sorted(d for d in glob.glob(os.path.join(src,'snapshots','day-*')) if os.path.exists(os.path.join(d,'SIMHL-ProTeamStats.txt')))
if not snaps:
    sys.stderr.write('\nSTOP — no SIMHL-ProTeamStats.txt in any snapshots/ day-* folder (the league team table: records, PP/PK, puck time).\nSupply the real STHS client export into the newest snapshot and re-run.\n\n'); sys.exit(2)
D=snaps[-1]; rd=lambda f:open(os.path.join(D,f),encoding='utf-8',errors='replace').read()
# Oct 28 guard: the pack must be built from the newest pull, and that pull must carry the league's team
# table WITH puck time. If not, stop and say exactly which file to pull again — never push zeros quietly.
# (--carry-puck lets a pull go out anyway, keeping the last real puck time from the pack in <out>.)
CARRY='--carry-puck' in sys.argv
newest=sorted(glob.glob(os.path.join(src,'snapshots','day-*')))[-1]
def _stop(msg):
    sys.stderr.write('\nSTOP — '+msg+'\nPull that file again into '+newest+' and re-run. To push the games anyway and keep the last real puck time, re-run with --carry-puck.\n\n'); sys.exit(2)
if os.path.normpath(newest)!=os.path.normpath(D) and not CARRY:
    _stop(os.path.basename(newest)+' has no SIMHL-ProTeamStats.txt (the league team table: records, PP/PK, puck time).')
# team stats in the tool's Team Stat layout
L=rd('SIMHL-ProTeamStats.txt').split('\n'); rec,st,mode={}, {},None
for l in L:
    c=l.rstrip('\r').split('\t')
    if c[0]=='Team' and len(c)>1 and c[1]=='GP': mode='rec';continue
    if c[0]=='Team' and len(c)>1 and c[1]=='GP1': mode='st';hdr=c;continue
    if mode and len(c)<10: mode=None;continue
    if mode=='rec':
        v=[int(x) for x in c[1:31]]; rec[c[0]]=dict(all=v[0:9],home=v[9:18],road=v[18:27])
    elif mode=='st':
        st[c[0]]={k:(float(x.strip().rstrip('%')) if x.strip() else 0.0) for k,x in zip(hdr[1:],c[1:])}
assert len(rec)==32 and len(st)==32, (len(rec),len(st))
# Oct 28 — empty-net goals, counted from each game's timed play-by-play: a goal scored while the OTHER
# club's goalie is pulled is an empty-net goal for the club that scored it (not the club that pulled).
EN={}
for g in idx['games']:
    f=os.path.join(src,g['file'])
    if not os.path.exists(f): continue
    t=open(f,encoding='utf-8',errors='replace').read(); i=t.find('Play-by-Play\n1st period')
    if i<0: continue
    j=t.find('Full Play-by-Play',i); seg=t[i:j if j>0 else len(t)]; pulled=None; sc={}
    for l in seg.split('\n'):
        if 'is pulled from the net' in l:
            m=re.search(r'- ([A-Z][A-Za-z .]+?), .*?is pulled from the net',l); pulled=m.group(1).strip() if m else None; continue
        m=re.search(r'Goal by .+? - (.+?) : (\d+) - (.+?) : (\d+)',l)
        if m:
            a,x,b,y=m.group(1).strip(),int(m.group(2)),m.group(3).strip(),int(m.group(4)); who=a if x>sc.get(a,0) else b; sc[a]=x; sc[b]=y
            if pulled and who!=pulled: EN[who]=EN.get(who,0)+1
            pulled=None
        if re.match(r'^\d\w\w period|^Overtime',l): pulled=None
# Oct 28 — puck time: SIMHL publishes no puck time. When the newest snapshot carries none, keep the real
# seconds already in the pack in <out> (and the day / game they run through) instead of writing zeros.
PZK=['PZ DF','PZ OF','PZ NT','PC DF','PC OF','PC NT']
PRK=['PuckTimeInZoneDF','PuckTimeInZoneOF','PuckTimeInZoneNT','PuckTimeControlinZoneDF','PuckTimeControlinZoneOF','PuckTimeControlinZoneNT']
has_puck=any(st[t].get(k,0) for t in st for k in PZK)
if not has_puck and not CARRY:
    _stop(os.path.basename(D)+'/SIMHL-ProTeamStats.txt has no puck time (PZ / PC columns are all 0) — the download came in incomplete.')
PUCK={}; _sd=int(re.sub(r'\D','',os.path.basename(D)) or 0)   # the snapshot the puck seconds come from
puck_thru=(_sd,max([g['game'] for g in idx['games'] if g.get('day',0)<=_sd] or [0]))
if not has_puck:
    puck_thru=(None,None); prev=os.path.join(out,'ike_simhl_pack.json.gz')
    if os.path.exists(prev):
        pp=json.loads(gzip.decompress(open(prev,'rb').read())); pm=pp.get('meta',{})
        puck_thru=(pm.get('puckTimeThroughDay',pm.get('day')),pm.get('puckTimeThroughGame',pm.get('game')))
        for r in pp.get('teampro',[]): PUCK[r['Name']]={'gp':r.get('PuckTimeGP',r.get('GP',0)),'v':[r.get(k,0) for k in PRK]}
def puck_sec(t,i): return round(st[t][PZK[i]]*60) if has_puck else (PUCK.get(t,{'v':[0]*6})['v'][i])
def puck_gp(t): return rec[t]['all'][0] if has_puck else PUCK.get(t,{'gp':0})['gp']
blk=lambda v:[v[0],v[1],v[2],0,v[3],v[4],v[5],v[6],v[7],v[8],v[7]-v[8]]
rows=[]
for t in sorted(rec):
    A=rec[t]['all'];S=st[t];pts=2*(A[1]+A[3]+A[5])+A[4]+A[6]
    n={'G':A[7],'P':pts,'PCT':round(pts/(2*A[0]),3) if A[0] else 0,'SHF':S['SHF'],'SHA':S['SHA'],'SHB':S['SHB'],'Pim':S['Pim'],'Hit':S['Hit'],
       'PPA':S['PPA'],'PPG':S['PPG'],'PP%':S['PP%'],'PKA':S['PKA'],'PK GA':S['PK GA'],'PK%':S['PK%'],'PK GF':S['PK GF'],
       'PZ DF':puck_sec(t,0)/60,'PC DF':puck_sec(t,3)/60,'PZ OF':puck_sec(t,1)/60,'PC OF':puck_sec(t,4)/60,'PZ NT':puck_sec(t,2)/60,'PC NT':puck_sec(t,5)/60,
       'FO% OZ':S['FO% OZ'],'FO% DZ':S['FO% DZ'],'FO% NT':S['FO% NT'],'SP1':S['SP1'],'SP2':S['SP2'],'SP3':S['SP3'],'SP4':S['SP4'],
       'G P1':S['GP1'],'G P2':S['GP2'],'G P3':S['GP3'],'G P4OT':S['GP4'],'HP GP':A[0],'PZ GP':puck_gp(t),'SO':S.get('SO',0),'EG':EN.get(t,0)}
    rows.append((t,rec[t],n))
names=list(rows[0][2].keys()); B=['GP','W','L','T','OTW','OTL','SOW','SOL','GF','GA','Diff']
o=io.StringIO();w=csv.writer(o,lineterminator='\n');w.writerow(['No','Name']+B*3+names)
for i,(t,r,n) in enumerate(rows,1): w.writerow([i,t]+blk(r['all'])+blk(r['home'])+blk(r['road'])+[n[k] for k in names])
av=lambda xs:round(sum(xs)/len(xs),2)
w.writerow(['','Average']+[av([blk(r[s])[j] for _,r,_ in rows]) for s in ('all','home','road') for j in range(11)]+[av([n[k] for *_,n in rows]) for k in names])
teamstat=o.getvalue()
# schedule
txt=rd('SIMHL-Schedule.txt')
pl={int(m.group(1)):(m.group(2),m.group(3)) for m in re.finditer(r'^(\d+)\t(.+?) \(\d+\) vs (.+?) \(\d+\)',txt,re.M)}
sr=list(csv.DictReader(io.StringIO(rd('SIMHL-ProSchedule.csv')))); num={}
for r in sr:
    g=int(r['Game Number'])
    if g in pl: num[r['Visitor Team']]=pl[g][0];num[r['Home Team']]=pl[g][1]
o=io.StringIO();w=csv.writer(o,lineterminator='\n');w.writerow(['Day','Game','Visitor Team','Visitor Score','Home Team','Home Score','OT','SO'])
for r in sr:
    v,h=num.get(r['Visitor Team'],r['Visitor Team']),num.get(r['Home Team'],r['Home Team']);vs=hs=ot=so=''
    if r['Play']=='True':
        vs,hs=r['Visitor Score'],r['Home Score'];so='SO' if r['Shutout']=='True' else '';ot='OT' if (r['Overtime']=='True' and not so) else ''
    w.writerow([r['Day'],r['Game Number'],v,vs,h,hs,ot,so])
schedule=o.getvalue()
files={'IKE_SIMHL_Season.json':json.dumps(idx,ensure_ascii=False)}
for g in idx['games']:
    f=os.path.join(src,g['file'])
    if os.path.exists(f): files[g['file']]=open(f,encoding='utf-8',errors='replace').read()

# ---- per game: who dressed for whom, zone faceoffs, goals and shots by period, strategy usage, stars ----
def roster(txt):
    out={}; L=txt.split('\n'); i=0
    while i<len(L):
        m=re.match(r'^Players Stats for (.+?)\s*$',L[i])
        if not m: i+=1; continue
        tm=m.group(1).strip(); i+=3
        while i<len(L) and L[i].strip():
            n=L[i][:25].strip()
            if n: out[n]=tm
            i+=1
    return out
def zone_fo(txt,teams):
    ro=roster(txt); s=txt; i=s.find('\nPlay-by-Play\n')
    if i>=0:
        s=s[i:]; j=s.find('\nFull Play-by-Play\n')
        if j>0: s=s[:j]
    out={t:{'OZ':[0,0],'NZ':[0,0],'DZ':[0,0]} for t in teams}
    for m in re.finditer(r'- (.+?) wins face-off versus (.+?) in (.+?) zone\.',s):
        tw,tl,z=ro.get(m.group(1).strip()),ro.get(m.group(2).strip()),m.group(3).strip()
        if tw not in out or tl not in out or tw==tl: continue
        if z=='neutral': zw=zl='NZ'
        elif z==tw: zw,zl='DZ','OZ'
        elif z==tl: zw,zl='OZ','DZ'
        else: continue
        out[tw][zw][0]+=1; out[tw][zw][1]+=1; out[tl][zl][1]+=1
    return out
def period_tables(txt,teams):
    out={}
    for kind in ('Goals','Shots'):
        m=re.search(r'\n\t?'+kind+r'\n\t([^\n]+)\n([^\n]+)\n([^\n]+)',txt)
        if not m: continue
        hdr=[h.strip() for h in m.group(1).split('\t')]
        for line in (m.group(2),m.group(3)):
            c=line.split('\t'); tm=c[0].strip()
            if tm not in teams: continue
            v=[0,0,0,0]
            for h,x in zip(hdr,c[1:]):
                try: n=int(x.strip())
                except ValueError: continue
                if h in ('1','2','3'): v[int(h)-1]+=n
                elif h.startswith('OT') or h=='4': v[3]+=n
            out.setdefault(tm,{})[kind]=v
    return out
SEC={'5 vs 5 Forward':'EVF','5 vs 5 Defense':'EVD','PowerPlay Forward':'PPF','PowerPlay Defense':'PPD',
     'Penalty Kill 4 Players Forward':'PKF','Penalty Kill 4 Players Defense':'PKD'}
TOI={'Normal Forward':'EVF','Normal Defense':'EVD','PP Forward':'PPF','PP Defense':'PPD','PK Forward':'PKF','PK Defense':'PKD'}
def unit_systems(txt,teams):
    L=txt.split('\n'); out={}
    for i in range(len(L)-1):
        tm=L[i].strip()
        if tm not in teams or L[i+1].strip()!='5 vs 5 Forward': continue
        codes={}; cur=None
        for j in range(i+1,len(L)):
            s=L[j].strip()
            if s in SEC: cur=SEC[s]; continue
            if s.startswith('Penalty Kill - 3') or s.startswith('4 vs 4') or s.startswith('Last Minutes') or s=='Goaltenders': cur=None
            if s=='Goaltenders' or (s in teams and j>i+1): break
            if cur:
                m=re.match(r'^\s*(\d+)\s+.*?\s(\d+)\s+(\d+)\s+(\d+)\s*$',L[j])
                if m and 'Phy' not in L[j]: codes.setdefault(cur,{})[int(m.group(1))]='%s-%s-%s'%(m.group(2),m.group(3),m.group(4))
        k=txt.find('% Time on Ice - '+tm)
        if k<0: continue
        cur=None
        for l in txt[k:].split('\n')[2:]:
            s=l.strip()
            if s.startswith('Total') or s.startswith('% Time on Ice'): break
            if s in TOI: cur=TOI[s]; continue
            if not re.match(r'^\d+ - ',s): cur=None if not s else cur; continue
            if not cur: continue
            p=[x.strip() for x in s.split(' - ')]
            if len(p)<4: continue
            mm=re.match(r'^(\d+):(\d+)$',p[3])
            if not mm: continue
            sec=int(mm.group(1))*60+int(mm.group(2)); code=codes.get(cur,{}).get(int(p[0]))
            if sec<=0 or not code: continue
            d=out.setdefault(tm,{}).setdefault(cur,{}); d[code]=d.get(code,0)+sec
    return out
def _add(dst,src):
    for u,m in src.items():
        d=dst.setdefault(u,{})
        for k,v in m.items(): d[k]=d.get(k,0)+v
FO={}; TEAMX={}; sys_season={}; sys_last={}; sys_gp={}; per_team=[]
for g in sorted(idx['games'],key=lambda x:x['game']):
    t=files.get(g['file'])
    if not t: continue
    tms={g.get('visitor'),g.get('home')}
    if None in tms: continue
    for tm,z in zone_fo(t,tms).items():
        d=FO.setdefault(tm,{'OZ':[0,0],'NZ':[0,0],'DZ':[0,0]})
        for k in z: d[k][0]+=z[k][0]; d[k][1]+=z[k][1]
    pt=period_tables(t,tms)
    if len(pt)==2:
        a,b=g['visitor'],g['home']
        for us,them in ((a,b),(b,a)):
            d=TEAMX.setdefault(us,{'gp':0,'gf':[0]*4,'ga':[0]*4,'sf':[0]*4,'sa':[0]*4}); d['gp']+=1
            for i in range(4):
                d['gf'][i]+=pt[us].get('Goals',[0]*4)[i]; d['ga'][i]+=pt[them].get('Goals',[0]*4)[i]
                d['sf'][i]+=pt[us].get('Shots',[0]*4)[i]; d['sa'][i]+=pt[them].get('Shots',[0]*4)[i]
    for tm,m in unit_systems(t,tms).items():
        _add(sys_season.setdefault(tm,{}),m); sys_gp[tm]=sys_gp.get(tm,0)+1; per_team.append((tm,m))
recent={}
for tm,m in reversed(per_team):
    if len(recent.setdefault(tm,[]))<10: recent[tm].append(m)
for tm,L10 in recent.items():
    for m in L10: _add(sys_last.setdefault(tm,{}),m)
SYSP={'gp':sys_gp,'season':sys_season,'last10':sys_last}
# the league's own team table, in the field names the app reads (puck time in seconds)
TEAMPRO=[]
for tm in sorted(rec):
    A,Hm,S=rec[tm]['all'],rec[tm]['home'],st[tm]; z=FO.get(tm,{'OZ':[0,0],'NZ':[0,0],'DZ':[0,0]})
    TEAMPRO.append({'Name':tm,'GP':A[0],'W':A[1],'L':A[2],'OTW':A[3],'OTL':A[4],'SOW':A[5],'SOL':A[6],'Points':2*(A[1]+A[3]+A[5])+A[4]+A[6],'GF':A[7],'GA':A[8],
      'HomeGP':Hm[0],'HomeW':Hm[1],'HomeL':Hm[2],'HomeOTW':Hm[3],'HomeOTL':Hm[4],'HomeSOW':Hm[5],'HomeSOL':Hm[6],'HomeGF':Hm[7],'HomeGA':Hm[8],
      'PPAttemp':S['PPA'],'PPGoal':S['PPG'],'PKAttemp':S['PKA'],'PKGoalGA':S['PK GA'],'PKGoalGF':S['PK GF'],'ShotsFor':S['SHF'],'ShotsAga':S['SHA'],'ShotsBlock':S['SHB'],
      'PuckTimeInZoneDF':puck_sec(tm,0),'PuckTimeInZoneOF':puck_sec(tm,1),'PuckTimeInZoneNT':puck_sec(tm,2),
      'PuckTimeControlinZoneDF':puck_sec(tm,3),'PuckTimeControlinZoneOF':puck_sec(tm,4),'PuckTimeControlinZoneNT':puck_sec(tm,5),'PuckTimeGP':puck_gp(tm),
      'Shutouts':S.get('SO',0),'EmptyNetGoal':float(EN.get(tm,0)),'Pim':S['Pim'],'Hits':S['Hit'],
      'FaceOffWonDefensifZone':z['DZ'][0],'FaceOffTotalDefensifZone':z['DZ'][1],'FaceOffWonOffensifZone':z['OZ'][0],'FaceOffTotalOffensifZone':z['OZ'][1],
      'FaceOffWonNeutralZone':z['NZ'][0],'FaceOffTotalNeutralZone':z['NZ'][1]})
# last game day's 3 stars
last=idx['lastDaySynced']; stars=[]
for g in idx['games']:
    t=files.get(g['file'])
    if g.get('day')!=last or not t: continue
    m=re.search(r'\n3 Stars[^\n]*\n((?:\d - [^\n]+\n){1,3})',t)
    if not m: continue
    ro=roster(t); gl={}
    for mm in re.finditer(r'\n([^\n(]+?) \(([A-Z-]{2,4})\), \d+ saves',t): gl[mm.group(1).strip()]=len(gl)
    for l in m.group(1).strip().split('\n'):
        mm=re.match(r'(\d) - (.+?) \(([A-Z-]{2,4})\)',l)
        if not mm: continue
        n=mm.group(2).strip(); tm=ro.get(n) or ({0:g['visitor'],1:g['home']}.get(gl.get(n)) if n in gl else '')
        stars.append({'n':{'1':'1st','2':'2nd','3':'3rd'}[mm.group(1)],'p':n,'t':tm or '','g':g['game']})
lead=json.load(open(leadf)) if leadf!='-' and os.path.exists(leadf) else None
# Oct 24: NHL ID + sweater number per player for the Depth Chart photos — the shared IKE_NHL_IDs.json
# (in the data folder or the folder above it); SIMHL's own files carry neither
NHL={}
for f in (os.path.join(src,'IKE_NHL_IDs.json'),os.path.join(src,'..','IKE_NHL_IDs.json')):
    if os.path.exists(f):
        try:
            for k,v in json.load(open(f,encoding='utf-8')).get('players',{}).items():
                if v.get('id'): NHL[re.sub(r'\s*\(R\)\s*$','',k)]=[str(v['id']),v.get('num')]
        except Exception: pass
        break
meta={'league':'SIMHL','day':idx['lastDaySynced'],'game':idx['lastGameSynced'],'at':idx.get('syncedAt',''),'snapshot':os.path.basename(D),'games':len(files)-1,'rev':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'puckTimeThroughDay':puck_thru[0],'puckTimeThroughGame':puck_thru[1]}
pack={'meta':meta,'files':files,'slots':{'teamStat':teamstat,'schedule':schedule},
      'simhl':{'simhlSkaters':rd('SIMHL-Players.csv'),'simhlGoalies':rd('SIMHL-Goalies.csv')},'lead':lead,
      'sys':SYSP,'teamx':TEAMX,'teampro':TEAMPRO,'stars':{'day':last,'list':stars},'nhl':NHL}
os.makedirs(out,exist_ok=True)
open(os.path.join(out,'ike_simhl_pack.json.gz'),'wb').write(gzip.compress(json.dumps(pack,ensure_ascii=False,separators=(',',':')).encode(),9))
json.dump(meta,open(os.path.join(out,'latest.json'),'w'),indent=1)
print(json.dumps(meta))
