"""Builds the DCHL data pack the IKE (DCHL) app reads online.
python3 -I dchl_pack.py <DCHL data dir> <lead.json or -> <out dir>
Writes <out>/ike_dchl_pack.json.gz (season index, every box score, the seven STHS exports from the newest
snapshot, play-by-play leaders, last game day's stars, every club's strategy usage) and <out>/latest.json (what the pack holds)."""
import json,gzip,os,re,sys,glob
src,leadf,out=sys.argv[1:4]
idx=json.load(open(os.path.join(src,'IKE_DCHL_Season.json'),encoding='utf-8'))
snaps=sorted(d for d in glob.glob(os.path.join(src,'snapshots','day-*')) if os.path.exists(os.path.join(d,'STHSTeamStat.CSV')))
D=snaps[-1]
M={'teamStat':'STHSTeamStat.CSV','schedule':'STHSSchedule.CSV','playerStat':'STHSPlayerStat.CSV','playerInfo':'STHSPlayerInformation.CSV',
   'playerRoster':'STHSPlayerRoster.CSV','goalieStat':'STHSGoalieStat.CSV','goalieRoster':'STHSGoaliesRoster.CSV'}
slots={k:open(os.path.join(D,f),encoding='utf-8',errors='replace').read() for k,f in M.items() if os.path.exists(os.path.join(D,f))}
def strip(t):   # drop the site menu above the box score
    i=t.find('\nCreated - ')
    return t if i<0 else t[t.rfind('\n',0,i)+1:]
files={'IKE_DCHL_Season.json':json.dumps(idx,ensure_ascii=False)}
for g in idx['games']:
    f=os.path.join(src,g['file'])
    if os.path.exists(f): files[g['file']]=strip(open(f,encoding='utf-8',errors='replace').read())
# last game day's 3 stars
def team_of(t,name,g):
    for side in (g['visitor'],g['home']):
        m=re.search(r'(?:^|\n)'+re.escape(side)+r'\nPlayer Name\tPOS[^\n]*\n([\s\S]*?)(?=\n[^\n\t]+\nPlayer Name\tPOS|\n\n)',t)
        if m and re.search(r'(?:^|\n)'+re.escape(name)+r'\t',m.group(1)): return side
    gl=re.findall(r'\n([^\n]+?) \(([A-Z]{2,4})\), \d+ saves',t)
    for i,(n,a) in enumerate(gl):
        if n==name: return g['visitor'] if i==0 else g['home']
    return ''
last=idx['lastDaySynced']; stars=[]
for g in idx['games']:
    t=files.get(g['file'])
    if g['day']!=last or not t: continue
    m=re.search(r'\n3 Stars[^\n]*\n((?:\d - [^\n]+\n){1,3})',t)
    if not m: continue
    for l in m.group(1).strip().split('\n'):
        mm=re.match(r'(\d) - (.+?) \(([A-Z]{2,4})\)',l)
        if mm: stars.append({'n':{'1':'1st','2':'2nd','3':'3rd'}[mm.group(1)],'p':mm.group(2),'t':team_of(t,mm.group(2),g),'g':g['game']})

# team strategy usage: every club's Lines tab carries PHY-DF-OF per unit and the time each unit played
SEC={'5 vs 5 Forward':'EVF','5 vs 5 Defense':'EVD','Power Play Forward':'PPF','Power Play Defense':'PPD',
     'Penalty Kill 4 Players Forward':'PKF','Penalty Kill 4 Players Defense':'PKD'}
def _secs(t):
    p=t.split(':')
    return int(p[0])*60+int(p[1]) if len(p)==2 and p[0].isdigit() and p[1].isdigit() else 0
def unit_systems(txt,teams):
    L=txt.split('\n'); out={}
    for i in range(1,len(L)):
        if L[i].strip()!='5 vs 5 Forward' or L[i-1].strip() not in teams: continue
        tm=L[i-1].strip(); cur=None; hdr=None; seen=0
        for j in range(i,len(L)):
            t=L[j].strip()
            if t=='5 vs 5 Forward':
                seen+=1
                if seen>1: break
            if t in SEC: cur=SEC[t]; hdr=None; continue
            if t.startswith('Penalty Kill 3') or t.startswith('4 vs 4') or t.startswith('Last Minutes'): cur=None; continue
            if t=='Time' and cur is None: break
            c=L[j].split('\t')
            if cur and c[0].strip()=='Line #': hdr=[x.strip() for x in c]; continue
            if cur and hdr and c[0].strip().isdigit() and 'PHY' in hdr and 'Time Play' in hdr:
                ip=hdr.index('PHY')
                try: code='-'.join(str(int(c[k].strip())) for k in (ip,ip+1,ip+2)); s=_secs(c[hdr.index('Time Play')].strip())
                except (ValueError,IndexError): continue
                if s<=0: continue
                d=out.setdefault(tm,{}).setdefault(cur,{}); d[code]=d.get(code,0)+s
    return out
def _add(dst,src):
    for u,m in src.items():
        d=dst.setdefault(u,{})
        for k,v in m.items(): d[k]=d.get(k,0)+v
sys_season={}; sys_last={}; sys_gp={}; per_team=[]
for g in sorted(idx['games'],key=lambda x:x['game']):
    t=files.get(g['file'])
    if not t: continue
    us=unit_systems(t,{g['visitor'],g['home']})
    for tm,m in us.items():
        _add(sys_season.setdefault(tm,{}),m); sys_gp[tm]=sys_gp.get(tm,0)+1; per_team.append((tm,m))
recent={}
for tm,m in reversed(per_team):
    if len(recent.setdefault(tm,[]))<10: recent[tm].append(m)
for tm,L10 in recent.items():
    for m in L10: _add(sys_last.setdefault(tm,{}),m)
SYSP={'gp':sys_gp,'season':sys_season,'last10':sys_last}

# goals and shots by period, for and against, from every box score's period table
def period_tables(txt,teams):
    out={}
    for kind in ('Goals','Shots'):
        m=re.search(r'\n'+kind+r'\n\t([^\n]+)\n([^\n]+)\n([^\n]+)',txt)
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
TEAMX={}
for g in idx['games']:
    t=files.get(g['file'])
    if not t: continue
    pt=period_tables(t,{g['visitor'],g['home']})
    if len(pt)!=2: continue
    a,b=g['visitor'],g['home']
    for us,them in ((a,b),(b,a)):
        d=TEAMX.setdefault(us,{'gp':0,'gf':[0]*4,'ga':[0]*4,'sf':[0]*4,'sa':[0]*4}); d['gp']+=1
        for i in range(4):
            d['gf'][i]+=pt[us].get('Goals',[0]*4)[i]; d['ga'][i]+=pt[them].get('Goals',[0]*4)[i]
            d['sf'][i]+=pt[us].get('Shots',[0]*4)[i]; d['sa'][i]+=pt[them].get('Shots',[0]*4)[i]
# the league's own team table (TeamStatPro): records, puck time and zone faceoffs as the league keeps them
TEAMPRO=None
tp=os.path.join(D,'DCHL-TeamStatPro.json')
if os.path.exists(tp):
    try: TEAMPRO=[r for r in json.load(open(tp,encoding='utf-8')) if r.get('Name')]
    except Exception: TEAMPRO=None
lead=json.load(open(leadf)) if leadf!='-' and os.path.exists(leadf) else None
meta={'league':'DCHL','day':idx['lastDaySynced'],'game':idx['lastGameSynced'],'at':idx.get('syncedAt',''),'snapshot':os.path.basename(D),'games':len(files)-1}
pack={'meta':meta,'files':files,'slots':slots,'lead':lead,'stars':{'day':last,'list':stars},'sys':SYSP,'teamx':TEAMX,'teampro':TEAMPRO}
os.makedirs(out,exist_ok=True)
open(os.path.join(out,'ike_dchl_pack.json.gz'),'wb').write(gzip.compress(json.dumps(pack,ensure_ascii=False,separators=(',',':')).encode(),9))
json.dump(meta,open(os.path.join(out,'latest.json'),'w'),indent=1)
print(json.dumps(meta))
