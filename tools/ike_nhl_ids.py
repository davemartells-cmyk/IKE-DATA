"""IKE NHL IDs: one shared list (E:\\IKE\\Data\\IKE_NHL_IDs.json) of each real player's NHL ID and sweater
number, used for the Depth Chart photos (https://cdn.nhle.com/photos/mugs/<id>.jpg). Same player, same ID,
in every league.

  python3 -I ike_nhl_ids.py missing <IKE_NHL_IDs.json> <DCHL snapshot dir>
      Prints the JavaScript to run in the Claude browser pane on https://api-web.nhle.com/ (javascript_tool),
      or NONE when every DCHL pro-roster player already has an ID.
  python3 -I ike_nhl_ids.py update <IKE_NHL_IDs.json> <DCHL snapshot dir> <out.json> [<browser result file>]
      Writes the updated list: IDs from the league file first, then the browser lookup for the rest.
      The result file is the tool-results file the browser step saved (or the JSON it printed).
A player the lookup can't place keeps no ID and shows initials. Fix a wrong match by editing its id by hand
(set "src":"manual" so it is never replaced).
"""
import json, os, re, sys, time

def load(p):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return {'players': {}}

def roster(snap):
    d = json.load(open(os.path.join(snap, 'DCHL-PlayerRoster.json'), encoding='utf-8'))
    g = json.load(open(os.path.join(snap, 'DCHL-GoalerRoster.json'), encoding='utf-8'))
    return d + g

def clean(n): return re.sub(r'\s*\(R\)\s*$', '', n or '').strip()
def grp(x): return 'G' if x.get('PosG') == 'True' else 'D' if x.get('PosD') == 'True' else 'F'
def is_pro(x): return bool(x.get('TeamName')) and x['TeamName'] == x.get('ProTeamName')

def need(ids, snap):
    P = ids.get('players', {}); out = []
    for x in roster(snap):
        if not is_pro(x): continue
        n = clean(x['Name']); r = P.get(n)
        if x.get('NHLID') or (r and r.get('id')): continue   # has an ID; a missing number is fine
        if r and r.get('src') == 'manual': continue
        out.append({'n': n, 'pos': grp(x), 'id': str(x['NHLID']) if x.get('NHLID') else (r or {}).get('id')})
    return out

JS = r'''const NEED=%s;
const norm=s=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z]/g,'');
const OUT={}; let i=0;
async function one(p){ for(let k=0;k<3;k++){ try{ const j=await (await fetch('https://search.d3.nhle.com/api/v1/search/player?culture=en-us&limit=20&q='+encodeURIComponent(p.n))).json();
  OUT[p.n]=j.filter(x=>norm(x.name)===norm(p.n)).map(x=>[x.playerId,x.positionCode,x.sweaterNumber??null,x.active,x.lastSeasonId||null]); return; }catch(e){ await new Promise(r=>setTimeout(r,500)); } } }
async function w(){ while(i<NEED.length) await one(NEED[i++]); }
await Promise.all([w(),w(),w(),w(),w(),w()]);
JSON.stringify({first:OUT, pad:'x'.repeat(300000)})'''

def okpos(gp, pc): return pc == 'G' if gp == 'G' else pc == 'D' if gp == 'D' else pc in ('C', 'L', 'R')
def pick(ms, gp, want=None):
    if want: ms = [m for m in ms if str(m[0]) == str(want)]
    if len(ms) == 1: return ms[0]
    ms = [m for m in ms if okpos(gp, m[1])]
    ms.sort(key=lambda m: (bool(m[3]), m[4] or ''), reverse=True)
    return ms[0] if ms else None

def read_result(path):
    t = open(path, encoding='utf-8').read().strip()
    try:
        a = json.loads(t)
        if isinstance(a, list) and a and isinstance(a[0], dict) and 'text' in a[0]: t = a[0]['text']
        elif isinstance(a, dict): return a
    except Exception: pass
    t = t[t.index('"') if t.startswith('"') else 0:]
    if t.startswith('"'): t = json.loads(t[:t.rindex('"') + 1])
    return json.loads(t)

def update(ids, snap, res):
    P = dict(ids.get('players', {})); first = (res or {}).get('first', {})
    for x in roster(snap):
        n = clean(x['Name']); r = dict(P.get(n) or {})
        if r.get('src') == 'manual': continue
        if x.get('NHLID'): r['id'] = str(x['NHLID']); r['src'] = 'league'
        m = pick(first.get(n) or [], grp(x), r.get('id')) if n in first else None
        if m and not r.get('id'): r['id'] = str(m[0]); r['src'] = 'lookup'
        if x.get('Jersey'): r['num'] = x['Jersey']
        elif m and m[2] and str(m[0]) == str(r.get('id')) and not r.get('num'): r['num'] = m[2]
        if r.get('id'): P[n] = r
    return {'about': ids.get('about', 'NHL IDs and sweater numbers, shared by DCHL and SIMHL.'),
            'updated': time.strftime('%Y-%m-%d'), 'players': dict(sorted(P.items()))}

if __name__ == '__main__':
    mode, idf, snap = sys.argv[1:4]
    ids = load(idf)
    if mode == 'missing':
        nd = need(ids, snap)
        print(JS % json.dumps(nd, ensure_ascii=False, separators=(',', ':')) if nd else 'NONE')
    elif mode == 'update':
        res = read_result(sys.argv[5]) if len(sys.argv) > 5 else None
        out = update(ids, snap, res)
        json.dump(out, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        pro = [x for x in roster(snap) if is_pro(x)]
        have = sum(1 for x in pro if (out['players'].get(clean(x['Name'])) or {}).get('id'))
        print('players', len(out['players']), '· pro roster with an NHL ID', have, 'of', len(pro))
