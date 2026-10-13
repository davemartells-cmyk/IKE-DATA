# IKE-DATA

League data the I.K.E apps read online, so the phone is current without redeploying the app.

- `SIMHL/latest.json`: what the SIMHL pack holds (day, last game, pull date).
- `SIMHL/ike_simhl_pack.json.gz`: every SIMHL game sheet, team stats, schedule, player and goalie files, and the play-by-play leaders.

Updated by the nightly 8 pm pull:
1. `node tools/simhl_lead.js tools/empire_engine.html <E:\IKE\Data\SIMHL copy> lead.json` counts the play-by-play leaders with the Empire tool's own game reader.
2. `python3 -I tools/simhl_pack.py <E:\IKE\Data\SIMHL copy> lead.json SIMHL` builds the pack.
3. Commit and push.
