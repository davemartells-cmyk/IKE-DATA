"""Builds the SIMHL data pack the Empire Edition reads online.
python3 -I simhl_pack.py <SIMHL data dir> <lead.json> <out dir>
Writes <out>/ike_simhl_pack.json.gz (index, every game sheet, team stats, schedule, player and goalie files,
play-by-play leaders) and <out>/latest.json (what the pack holds)."""
import csv,io,re,json,gzip,os,sys,glob
src,leadf,out=sys.argv[1:4]
idx=json.load(open(os.path.join(src,'IKE_SIMHL_Season.json'),encoding='utf-8'))
snaps=sorted(d for d in glob.glob(os.path.join(src,'snapshots','day-*')) if os.path.exists(os.path.join(d,'SIMHL-ProTeamStats.txt')))
D=snaps[-1]; rd=lambda f:open(os.path.join(D,f),encoding='utf-8',errors='replace').read()
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
blk=lambda v:[v[0],v[1],v[2],0,v[3],v[4],v[5],v[6],v[7],v[8],v[7]-v[8]]
rows=[]
for t in sorted(rec):
    A=rec[t]['all'];S=st[t];pts=2*(A[1]+A[3]+A[5])+A[4]+A[6]
    n={'G':A[7],'P':pts,'PCT':round(pts/(2*A[0]),3) if A[0] else 0,'SHF':S['SHF'],'SHA':S['SHA'],'SHB':S['SHB'],'Pim':S['Pim'],'Hit':S['Hit'],
       'PPA':S['PPA'],'PPG':S['PPG'],'PP%':S['PP%'],'PKA':S['PKA'],'PK GA':S['PK GA'],'PK%':S['PK%'],'PK GF':S['PK GF'],
       'PZ DF':S['PZ DF'],'PC DF':S['PC DF'],'PZ OF':S['PZ OF'],'PC OF':S['PC OF'],'PZ NT':S['PZ NT'],'PC NT':S['PC NT'],
       'FO% OZ':S['FO% OZ'],'FO% DZ':S['FO% DZ'],'FO% NT':S['FO% NT'],'SP1':S['SP1'],'SP2':S['SP2'],'SP3':S['SP3'],'SP4':S['SP4'],
       'G P1':S['GP1'],'G P2':S['GP2'],'G P3':S['GP3'],'G P4OT':S['GP4'],'HP GP':A[0],'PZ GP':A[0]}
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
lead=json.load(open(leadf)) if leadf!='-' and os.path.exists(leadf) else None
meta={'league':'SIMHL','day':idx['lastDaySynced'],'game':idx['lastGameSynced'],'at':idx.get('syncedAt',''),'snapshot':os.path.basename(D),'games':len(files)-1}
pack={'meta':meta,'files':files,'slots':{'teamStat':teamstat,'schedule':schedule},
      'simhl':{'simhlSkaters':rd('SIMHL-Players.csv'),'simhlGoalies':rd('SIMHL-Goalies.csv')},'lead':lead}
os.makedirs(out,exist_ok=True)
open(os.path.join(out,'ike_simhl_pack.json.gz'),'wb').write(gzip.compress(json.dumps(pack,ensure_ascii=False,separators=(',',':')).encode(),9))
json.dump(meta,open(os.path.join(out,'latest.json'),'w'),indent=1)
print(json.dumps(meta))
