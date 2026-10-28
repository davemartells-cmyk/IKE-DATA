"""IKE ingest: turn saved browser results into league files.
Input files: Claude tool-result files, or the plain JSON string that IKE.games() / IKE.chunk() returned, saved as a .json file.
usage: python3 -I ike_ingest.py LEAGUE MANIFEST_IN OUTDIR [--games f1 f2 ...] [--snap f1 f2 ...]
 - LEAGUE: DCHL or SIMHL
 - MANIFEST_IN: current IKE_<LEAGUE>_Season.json (staged copy)
 - OUTDIR: empty folder; gets games/, snapshots/day-NNN/, IKE_<LEAGUE>_Season.json, then zip it and unzip into E:\\IKE\\Data\\<LEAGUE>
"""
import sys,os,json,gzip,base64,re
def load(p):
    raw=json.load(open(p,encoding='utf-8'))
    if raw and isinstance(raw[0],dict) and 'n' in raw[0]:
        return raw  # plain JSON saved straight from the browser (the string IKE.games()/IKE.chunk() returned)
    t=raw[0]['text']
    if 'truncated: content too large' in t: raise SystemExit('TRUNCATED result: '+p+' -> re-pull with smaller batches')
    return json.loads(json.loads(t[:t.rfind('"')+1]))
def dec(b): return gzip.decompress(base64.b64decode(b)).decode('utf-8')
args=sys.argv[1:]; L,man_in,out=args[0],args[1],args[2]
games,snaps,mode=[],[],None
for a in args[3:]:
    if a=='--games': mode=games; continue
    if a=='--snap': mode=snaps; continue
    mode.append(a)
man=json.load(open(man_in)); os.makedirs(os.path.join(out,'games'),exist_ok=True)
pad=4 if L=='DCHL' else 3
new=[];bad=[]
for p in games:
    for g in load(p):
        if g.get('n')==-1: continue
        if 'gz' not in g: bad.append(g['n']); continue
        t=dec(g['gz'])
        if len(t)!=g['len'] or len(t)<3000: bad.append(g['n']); continue
        fn='%s_game_%0*d.txt'%(L,pad,g['n']); open(os.path.join(out,'games',fn),'w',encoding='utf-8').write(t)
        new.append((g['n'],t,fn))
data={}
if snaps:
    ch={}
    for p in snaps:
        for c in load(p):
            if c.get('n')==-1: continue
            ch.setdefault(c['n'],{})[c['i']]=(c['tot'],c['d'])
    for n,parts in ch.items():
        tot=list(parts.values())[0][0]
        if len(parts)!=tot: bad.append('snapshot:'+n); continue
        data[n]=dec(''.join(parts[i][1] for i in range(tot)))
# schedule -> day/teams/scores
sched={}
if L=='DCHL' and 'SchedulePro' in data:
    for x in json.loads(data['SchedulePro']):
        if x['Play']=='True': sched[int(x['GameNumber'])]=dict(day=int(x['Day']),visitor=x['VisitorTeamName'],vs=int(x['VisitorScore']),home=x['HomeTeamName'],hs=int(x['HomeScore']),ot=x['Overtime']=='True',so=x['Shootout']=='True')
if L=='SIMHL' and 'SIMHL-Schedule' in data:
    day=0
    for line in data['SIMHL-Schedule'].split('\n'):
        m=re.match(r'Day (\d+)',line)
        if m: day=int(m.group(1)); continue
        m=re.match(r'(\d+)\t(.+?) \((\d+)\) vs (.+?) \((\d+)\)(.*)',line)
        if m: sched[int(m.group(1))]=dict(day=day,visitor=m.group(2),vs=int(m.group(3)),home=m.group(4),hs=int(m.group(5)),extra=m.group(6).strip(' -'))
known={g['game'] for g in man['games']}
for n,t,fn in new:
    rec=dict(game=n,**sched.get(n,{}),fullPBP='on ice for' in t,file='games/'+fn)
    man['games']=[g for g in man['games'] if g['game']!=n]+[rec]
man['games'].sort(key=lambda g:g['game'])
if data:
    day=max([v['day'] for v in sched.values()] or [man['lastDaySynced']])
    sd=os.path.join(out,'snapshots','day-%03d'%day); os.makedirs(sd,exist_ok=True)
    for k,v in data.items():
        if k.startswith('CSV:'):
            open(os.path.join(sd,k[4:]),'w',encoding='utf-8',newline='').write(v); continue
        ext='json' if L=='DCHL' else 'txt'; name=('DCHL-%s'%k) if L=='DCHL' else k
        open(os.path.join(sd,name+'.'+ext),'w',encoding='utf-8').write(v)
    man['lastDaySynced']=day
    if 'snapshots/day-%03d'%day not in man['snapshots']: man['snapshots'].append('snapshots/day-%03d'%day)
if man['games']: man['lastGameSynced']=max(g['game'] for g in man['games'])
import datetime; man['syncedAt']=datetime.date.today().isoformat()
json.dump(man,open(os.path.join(out,'IKE_%s_Season.json'%L),'w'),indent=1)
print('new games',[n for n,_,_ in new],'bad',bad,'snapshot',list(data),'lastGame',man['lastGameSynced'],'lastDay',man['lastDaySynced'])
