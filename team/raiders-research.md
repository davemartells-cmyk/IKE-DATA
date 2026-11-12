# Prince Albert Raiders (SWHL sim) — research notes (Dave, Claude, Ike)

How this works: everyone reads this file before answering and adds to it, newest entry at the bottom of the Log.
"Our team" = Dave's sim Prince Albert Raiders on swhl.sths.ca. "Raiders" = the real-life WHL team. Real players sit on different sim teams.
We rank our players by real-world scouting (Elite Prospects, draft boards, scouting reports, real WHL production) — not the sim OV rating.

## Request for Ike — Nov 11 (from Dave, via Claude)
These seven are on our sim roster. All are young (16–17-ish) and have shown little real WHL production so far. Dave wants a deeper look at each one before deciding whether to use them as trade pieces to move up for players with more upside.

| Player | Sim pos | Real WHL team (as last seen) | Real 2026-27 so far |
|---|---|---|---|
| Kash Andresen | RW | confirm current team | ~3 pts |
| Zane Torre | RW | Kamloops Blazers | 13 GP, 2-1-3 |
| Tristan Mitchell-McElhone | C | Saskatoon Blades | ~1 pt |
| Cash Arcand-Vandale | RW | Red Deer Rebels | ~2 pts |
| Dermot Johnston | D | Prince George Cougars | ~2 pts |
| Kaden Allan | D | Saskatoon Blades | 0 pts |
| Cameron Dillard | D | Red Deer Rebels | ~1 pt |

For each player, please find:
1. Elite Prospects profile: birth date, height/weight, shoots, and his EP rating/ranking if shown.
2. Draft history: WHL Prospects Draft round/pick, and NHL draft year he becomes eligible.
3. Any scouting report or prospect ranking (EP, NHL Central Scouting, Neutral Zone, team/media articles).
4. His real role this season: games played, ice time / line, power play or PK use, injuries, healthy scratches.
5. Trend: is he getting better (last 5–10 games vs. start of season)?
6. Your read: KEEP (real upside) or TRADE CHIP (low upside, sell while he has value) — one line why.

Reply in the Log below. Dave will pass the results to the research team.

## Request for Ike — Nov 11, League Three app build (from Dave, via Claude)
Claude is building the League Three (SWHL) I.K.E app from Dave's folder E:\IKE\Data\League3. The folder has the Nov 1 League One build, player and goalie ratings, player/goalie/team stats, player info, schedule, and the forward and defence chart PDFs. Three things the build needs are yours to send. Please add each one to the Log below as a table.

1. MUST-KEEP LIST — our sim Raiders players who are not to be traded. One row per player: Player | Pos. These get a star in the player pool.
2. TRADE-TARGET LIST — the players we are going after. One row per player: Player | Pos | Current sim team | Elite Prospects rating | Draft status (NHL draft year eligible, or round/pick/team if drafted) | One-line note. These go in their own scouting tool.
3. ELITE PROSPECTS DATA for the Scouting Report — for every player on our sim Raiders roster first, then the rest of the league as you get to them: Player | Elite Prospects rating | Draft status | Elite Prospects link. Spell names exactly as on swhl.sths.ca so they match the league files.

Also confirm one thing from the league site: the stat files in Dave's folder show every team at 18–19 games played (our team 7-10-0-1). Which season are those totals — last season, or something else? The regular season starts Nov 12.

## Request for Ike — Nov 11 evening, League Three app is built (from Claude)
The League Three I.K.E app is built: IKE_League3_Nov12.html, in Dave's folder E:\IKE\Data\League3. Your must-keep list (19), trade-target list (12) and Elite Prospects table (our 31) are all in it as you posted them. Four things would finish it. Answer each in the Log below.

1. GAME SHEETS — the app has no box scores, so Matchups, Strategy, Advanced Stats, Game Log, Who's Hot and the IKE 4 player card are empty. Pull every played game from swhl.sths.ca (games 1–216 through Day 40, then each new day) the same way the League One pull works (tools/ike_pull.js, page text with every tab shown), and save them in this repo under SWHL/games/ with an IKE_SWHL_Season.json index. Say in the Log when the first batch is in and Claude will build the pack the app reads (SWHL/ike_swhl_pack.json.gz).
2. ELITE PROSPECTS, REST OF THE LEAGUE — same table as our roster (Player | Elite Prospects rating | Draft status | Elite Prospects link), names spelled as on swhl.sths.ca. Post it a club at a time if that is easier.
3. CONFERENCES AND DIVISIONS — the app uses the real WHL alignment (Eastern: East, Central; Western: B.C., U.S.). Check the league site's Standings page and post the sim league's alignment, club by club, if it is any different.
4. SEVEN-PLAYER DEEP-DIVE — still open from last night (Andresen, Torre, Dillard, Allan, Arcand-Vandale, Johnston, Mitchell-McElhone).

## Already settled (for context)
- Core, not for trade: Blake Fiddler (D, no-trade clause), Tomas Poletin, Blake Vanek, Blake Chorney.
- Young pieces just brought in to build around: Kale McCann (D), Chace Gregg (F), Logan Henry (C).

## Log
- Nov 11 — Claude: posted the request above for Ike.
- Nov 11 — Claude: posted the League Three app build request above for Ike (must-keep list, trade-target list, Elite Prospects data, stat-season check).
- Nov 11 — Raiders front office (League 3 desk): answers to both requests below. The seven-player deep-dive is IN PROGRESS (EP profile, draft history, scouting reports, real role, trend, KEEP / TRADE CHIP read for Andresen, Torre, Mitchell-McEllhone, Arcand-Vandale, Johnston, Allan, Dillard) — it posts as its own Log entry next.

**STAT-SEASON CHECK (from the league site):** the totals are the CURRENT sim season, in progress — not last season. Live site checked Nov 11: every team at 19 GP, our club 8-10-0-1. Dave's folder snapshot is the same season one game earlier (18 GP, 7-10-0-1). A completed WHL season runs 68 games, so 18–19 GP can only be a season under way.

**MUST-KEEP LIST** (Dave's list as confirmed Nov 10; sim positions):

| Player | Pos |
|---|---|
| Blake Fiddler | D |
| Blake Chorney | LW |
| Asher Gingras | C |
| Cruz Pavao | RW |
| Cash Arcand-Vandale | RW |
| Kale McCann | D |
| Chace Gregg | LW |
| Kaden Allan | D |
| Marek Sklenicka | G |
| Urijah Moosetail | G |
| Gavin Lesiuk | LW |
| Dermot Johnston | D |
| Marcus Laraque | RW |
| Zane Torre | RW |
| Cameron Dillard | D |
| Tristan Mitchell-McEllhone | C |
| Grady Pichette | D |
| Peyton Shore | G |
| Logan Henry | C |

Reconciliation flags for Dave/Claude — this desk's records differ from "Already settled" above:
- Tomas Poletin is NOT untouchable in the front-office record — he is a premium trade asset with a standing price (an elite 16/17-year-old at PO 90+ plus additional value, or a 2028/29 1st-round pick plus a premium young prospect). GMs have bid; none has met it.
- Blake Vanek is on the TRADING BLOCK (Dave's Nov 10 list), not core.
- Cruz Pavao: Dave entered a deal with Victoria on Nov 11 (Calder Hamilton + Tripp Fischer coming back; Pavao + a 2029 3rd + our 2028 5th going out). Pending site confirmation — if it lands, Pavao leaves this list and Hamilton (D, 17) joins the young core.

**TRADE-TARGET LIST** — sim side complete. The Elite Prospects rating and Draft status columns are being pulled with the Scouting Report data (next Log entry) and are marked pending rather than guessed:

| Player | Pos | Current sim team | Elite Prospects rating | Draft status | One-line note |
|---|---|---|---|---|---|
| Christopher Kokkoris | D | Lethbridge | EP pull pending | EP pull pending | PO 90, healthy scratch; a piece in the built Poletin ask to Zachary |
| Owen Archer | D | Lethbridge | EP pull pending | EP pull pending | PO 84, scratch; Zachary is open to moving him — ball with us |
| Brook Haile | D | Kamloops | EP pull pending | EP pull pending | PO 84; in Dave's live counter (Coupland + Dillard for Jim + Haile) |
| Cruz Jim | D | Kamloops | EP pull pending | EP pull pending | PO 87; same counter |
| Kalen Miles | C | Penticton | EP pull pending | EP pull pending | PO 88; offer decision open with Dave |
| Eli McKamey | RW | Swift Current | EP pull pending | EP pull pending | PO 80; in our live offer to Jared Down |
| Roan Greschuk | D | Tri-City | EP pull pending | EP pull pending | PO 84, scratch; Quick wants a high pick back |
| Mathis Preston | RW | Vancouver | EP pull pending | EP pull pending | PO 86; parked — needs the Tri-City 2028 2nd freed from the Swift Current offer |
| Landon Dupont | D | Regina | EP pull pending | EP pull pending | PO 94 — wish-list headliner |
| Kayden Stroeder | C | Red Deer | EP pull pending | EP pull pending | PO 91 — wish list |
| Jaxon Jacobson | C | Spokane | EP pull pending | EP pull pending | PO 88; crown-jewel price |
| Cruz Nicolay | D | Spokane | EP pull pending | EP pull pending | PO 82, scratch; Spokane held — Dave handles Shaun personally |

The full tour board (wish list PO 90+ ×18, working tier PO 80–85 ×39, gap class PO 86–89) is on file at the front office and can be posted if the build wants all of it.

**ELITE PROSPECTS DATA for the Scouting Report:** IN PROGRESS — our roster first (31 players, names spelled as on swhl.sths.ca), then the targets, then the rest of the league. Posts as its own Log entry next.
- Nov 11 — Raiders front office: ELITE PROSPECTS DATA for the Scouting Report — OUR ROSTER (all 31, names spelled as on swhl.sths.ca). Full detail (DOB, height/weight, shoots, WHL draft, real 2026-27 team and line for each player) is in the front-office pull if the build wants more columns.

| Player | Elite Prospects rating | Draft status | Elite Prospects link |
|---|---|---|---|
| Tomas Poletin | #130 (EP, 2025 NHL Draft) | NHL drafted — 2025, Round 4, #106, New York Islanders | https://www.eliteprospects.com/player/888488/tomas-poletin |
| Aaron Obobaifo | none shown | 2025 NHL Draft eligible, undrafted | https://www.eliteprospects.com/player/689896/aaron-obobaifo |
| Nathan Brown | none shown (EP draft report exists, no numeric ranking) | 2026 NHL Draft eligible, undrafted | https://www.eliteprospects.com/player/724534/nathan-brown |
| Kyle McDonough | none shown | Undrafted (first eligible 2025) | https://www.eliteprospects.com/player/799972/kyle-mcdonough |
| Asher Gingras | none shown | 2027 NHL Draft eligible | https://www.eliteprospects.com/player/701518/asher-gingras |
| Logan Henry | none shown | 2028 NHL Draft eligible | https://www.eliteprospects.com/player/976841/logan-henry |
| Tristan Mitchell-McEllhone | none shown | 2026 NHL Draft eligible | https://www.eliteprospects.com/player/883576/tristan-mitchell-mcellhone |
| Blake Chorney | none shown | 2027 NHL Draft eligible | https://www.eliteprospects.com/player/960847/blake-chorney |
| Chace Gregg | none shown | 2028 NHL Draft eligible | https://www.eliteprospects.com/player/1043115/chace-gregg |
| Gavin Lesiuk | none shown (EP draft report exists, no numeric ranking) | 2026 NHL Draft eligible, undrafted | https://www.eliteprospects.com/player/628114/gavin-lesiuk |
| Caleb Matthews | none shown | 2025 NHL Draft eligible, undrafted | https://www.eliteprospects.com/player/801840/caleb-matthews |
| Hunter Wilm | none shown | 2027 NHL Draft eligible | https://www.eliteprospects.com/player/701411/hunter-wilm |
| Cruz Pavao | none shown (EP draft report exists, no numeric ranking) | 2026 NHL Draft eligible, undrafted | https://www.eliteprospects.com/player/879129/cruz-pavao |
| Cash Arcand-Vandale | none shown | 2027 NHL Draft eligible | https://www.eliteprospects.com/player/701398/cash-arcand-vandale |
| Marcus Laraque | none shown | 2027 NHL Draft eligible | https://www.eliteprospects.com/player/924593/marcus-laraque |
| Zane Torre | none shown | 2026 NHL Draft eligible | https://www.eliteprospects.com/player/888314/zane-torre |
| Ty Coupland | none shown | 2025 NHL Draft eligible, undrafted | https://www.eliteprospects.com/player/576981/ty-coupland |
| Kash Andresen | none shown | 2025 NHL Draft eligible, undrafted | https://www.eliteprospects.com/player/577061/kash-andresen |
| Blake Vanek | none shown (by EP itself) | NHL drafted — 2025, Round 3, #93, Ottawa Senators | https://www.eliteprospects.com/player/805740/blake-vanek |
| Blake Fiddler | #23 (EP, 2025 NHL Draft) | NHL drafted — 2025, Round 2, #36, Seattle Kraken | https://www.eliteprospects.com/player/577017/blake-fiddler |
| Brandon Mickelson | none shown | 2025 NHL Draft eligible, undrafted | https://www.eliteprospects.com/player/856908/brandon-mickelson |
| Hubert Clarke | none shown | 2026 NHL Draft eligible | https://www.eliteprospects.com/player/805657/hubert-clarke |
| Grady Pichette | none shown | 2027 NHL Draft eligible | https://www.eliteprospects.com/player/879898/grady-pichette |
| Kale McCann | none shown | 2028 NHL Draft eligible | https://www.eliteprospects.com/player/965719/kale-mccann |
| Dermot Johnston | none shown | 2026 NHL Draft eligible | https://www.eliteprospects.com/player/881368/dermot-johnston |
| Kaden Allan | none shown | 2026 NHL Draft eligible | https://www.eliteprospects.com/player/890156/kaden-allan |
| Cameron Dillard | none shown | 2026 NHL Draft eligible | https://www.eliteprospects.com/player/830374/cameron-dillard |
| Dylan Ronald | none shown | 2025 NHL Draft eligible, undrafted | https://www.eliteprospects.com/player/725709/dylan-ronald |
| Marek Sklenicka | none shown (EP draft report exists, no numeric ranking) | NHL drafted — 2026, Round 4, #120, Philadelphia Flyers | https://www.eliteprospects.com/player/918049/marek-sklenicka |
| Uriah Moosetail | none shown | 2027 NHL Draft eligible | https://www.eliteprospects.com/player/701524/urijah-moosetail |
| Peyton Shore | none shown | 2026 NHL Draft eligible | https://www.eliteprospects.com/player/890146/peyton-shore |

Notes: EP only publishes numeric draft rankings for top prospects — only Poletin (#130) and Fiddler (#23) carry one, so "none shown" is the honest entry for the rest, not a zero. Four roster players are already NHL-drafted: Poletin, Fiddler, Vanek, Sklenicka. Spellings as on EP differ in two cases (EP: "Marek Sklenička", "Urijah Moosetail", "Cash Arcand Vandale" without the hyphen). One soft spot: Kaden Allan's EP profile crawl predates his 2026-27 stats, so his EP line is unverified (chl.ca showed Saskatoon, 6 GP, 0 PTS). Next from this desk: the trade-target EP columns, then the rest of the league.
- Nov 11 — Raiders front office: TRADE-TARGET LIST, EP columns completed (this table supersedes the "EP pull pending" version above). Full detail is in the front-office pull EP_Targets_Pull_2026-11-11.md.

| Player | Pos | Current sim team | Elite Prospects rating | Draft status | One-line note |
|---|---|---|---|---|---|
| Christopher Kokkoris | D | Lethbridge | none shown | 2028 NHL eligible (WHL 2025, R1 #8, Edmonton) | PO 90 in the sim, healthy scratch; a piece in the built Poletin ask to Zachary. Real life: 6'6" D, Edmonton, 10 GP, 2 PTS |
| Owen Archer | D | Lethbridge | none shown | 2028 NHL eligible (WHL 2025, R2 #32, Red Deer) | PO 84, scratch; Zachary is open to moving him — ball with us. Real life: Drumheller (AJHL), 16 GP |
| Brook Haile | D | Kamloops | none shown | 2028 NHL eligible (WHL 2025, R1 #21, Seattle) | PO 84; in Dave's live counter (Coupland + Dillard for Jim + Haile) |
| Cruz Jim | D | Kamloops | none shown | 2028 NHL eligible (WHL 2025, R1 #12, Brandon) | PO 87; same counter. Real life: Brandon, 13 GP, 4 PTS |
| Kalen Miles | C | Penticton | none shown | 2028 NHL eligible (WHL 2025, R1 #10, Wenatchee) | PO 88; offer decision open with Dave. Real life: Wenatchee, 16 GP, 5 PTS |
| Eli McKamey | RW | Swift Current | none shown | 2027 NHL eligible (WHL 2024, R2 #35, Victoria) | PO 80; in our live offer to Jared Down. Real life: Tri-City, 18 GP, 15 PTS — matches his GM's billing |
| Roan Greschuk | D | Tri-City | none shown | 2028 NHL eligible (WHL 2025, R1 #19, Victoria) | PO 84, scratch; Quick wants a high pick back. Real life: Drumheller (AJHL), 14 GP |
| Mathis Preston | RW | Vancouver | #33 (EP, 2026 NHL Draft) | NHL drafted — 2026, Round 2, #50, Anaheim Ducks | PO 86; parked — needs the Tri-City 2028 2nd freed from the Swift Current offer. Real life: Vancouver, 18 GP, 26 PTS — his real stock is high |
| Landon Dupont | D | Regina | none shown (projected #1 for 2027 by other outlets — not an EP ranking) | 2027 NHL eligible (WHL 2024, R1 #1 overall, Everett — exceptional status) | PO 94 — wish-list headliner. Real life: University of Michigan (NCAA), 8 GP, 8 PTS |
| Kayden Stroeder | C | Red Deer | none shown | 2027 NHL eligible (WHL 2024, R1 #5, Edmonton) | PO 91 — wish list. Real life: Edmonton, 15 GP, 18 PTS |
| Jaxon Jacobson | C | Spokane | none shown | 2027 NHL eligible (WHL 2023, R1 #5, Brandon) | PO 88; crown-jewel price. Real life: Brandon captain, 19 GP, 19 PTS |
| Cruz Nicolay | D | Spokane | none shown | 2028 NHL eligible (WHL 2025, R2 #27, Regina) | PO 82, scratch; Spokane held — Dave handles Shaun personally. EP shows no 2026-27 stat line for him yet |

One gap, stated plainly: direct EP profile links are verified for Preston (https://www.eliteprospects.com/player/628115/mathis-preston); for the other 11, EP's search blocked the pull tool, so the office file links each player's EP team page rather than guessing profile URLs. The vitals, draft data and stat lines above all come from EP pages. Still to come from this desk: the seven-player deep-dive (reads being assembled) and the league-wide EP pass.
- Nov 11 — Claude: League Three app built (IKE_League3_Nov12.html). Posted the evening request above for Ike: game sheets, league-wide Elite Prospects, division alignment check, seven-player deep-dive.
