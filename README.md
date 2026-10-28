# IKE-DATA

League data the I.K.E apps read online, so the phone is current without redeploying the app.

- `SIMHL/latest.json`: what the SIMHL pack holds (day, last game, pull date).
- `SIMHL/ike_simhl_pack.json.gz`: every SIMHL game sheet, team stats, schedule, player and goalie files, and the play-by-play leaders.

Updated by the nightly 8 pm pull:
1. `node tools/simhl_lead.js tools/empire_engine.html <E:\IKE\Data\SIMHL copy> lead.json` counts the play-by-play leaders with the Empire tool's own game reader.
2. `python3 -I tools/simhl_pack.py <E:\IKE\Data\SIMHL copy> lead.json SIMHL` builds the pack.
   It stops (exit 2) if the newest pull's `SIMHL-ProTeamStats.txt` is missing or has no puck time, and names the file to pull again. Only after checking, `--carry-puck` pushes the games anyway and keeps the last real puck time.
3. Commit and push.

The DCHL pack (`tools/dchl_pack.py`) has the same check: it stops (exit 2) if the newest pull is missing any of the seven STHS exports or its `STHSTeamStat.CSV` has no puck time, and names the file; `--force` builds anyway.

## Pulling DCHL / SIMHL games from a browser

`tools/ike_pull.js` (paste into the console of a signed-in league page) and `tools/ike_ingest.py` (turns the saved results into `games/`, `snapshots/day-NNN/` and `IKE_<LEAGUE>_Season.json`). Game files are the box score page's text with every tab shown, captured by the script, not saved HTML. DCHL needs a browser signed in at https://dchl.sths.ca/Login.php; no password goes in any script.

    r = await IKE.games(<lastGameSynced>, 30); r === 'NONE' ? 'nothing new' : IKE.save('dchl_games_<n>.json', r)
    await IKE.snapshot(); IKE.save('dchl_snap_day<NNN>.json', IKE.chunkAll())
    python3 -I tools/ike_ingest.py DCHL <IKE_DCHL_Season.json> <empty out> --games dchl_games_<n>.json --snap dchl_snap_day<NNN>.json
