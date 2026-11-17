# WHL team logos — League 3 app

Downloaded 2026-11-16 from Dave's table (sent 13:08 EST, Nov 16, 2026, in the
Prince Albert Raiders — Front Office chat) plus the three rows cut off when
that message arrived truncated.

## Files — all 23 WHL teams, verified real PNGs

| File | Source URL | Notes |
| --- | --- | --- |
| Brandon_Wheat_Kings.png | https://assets.leaguestat.com/whl/logos/201.jpg | Source is JPEG; converted to true PNG |
| Calgary_Hitmen.png | https://assets.leaguestat.com/whl/logos/202.png | |
| Edmonton_Oil_Kings.png | https://assets.leaguestat.com/whl/logos/228.png | |
| Everett_Silvertips.png | https://assets.leaguestat.com/whl/logos/226.png | |
| Kamloops_Blazers.png | https://assets.leaguestat.com/whl/logos/203.png | |
| Kelowna_Rockets.png | https://assets.leaguestat.com/whl/logos/204.jpg | Source is JPEG; converted to true PNG |
| Lethbridge_Hurricanes.png | https://assets.leaguestat.com/whl/logos/205.png | |
| Medicine_Hat_Tigers.png | https://assets.leaguestat.com/whl/logos/206.png | |
| Moose_Jaw_Warriors.png | https://assets.leaguestat.com/whl/logos/207.png | 497x464 |
| Penticton_Vees.png | https://assets.leaguestat.com/whl/logos/277_295.jpg | Source is JPEG; converted to true PNG |
| Portland_Winterhawks.png | https://assets.leaguestat.com/whl/logos/208.png | |
| Prince_Albert_Raiders.png | https://assets.leaguestat.com/whl/logos/209.png | |
| Prince_George_Cougars.png | https://assets.leaguestat.com/whl/logos/210.png | 500x377 |
| Red_Deer_Rebels.png | https://assets.leaguestat.com/whl/logos/211.png | |
| Regina_Pats.png | https://assets.leaguestat.com/whl/logos/212.png | |
| Saskatoon_Blades.png | https://assets.leaguestat.com/whl/logos/213.jpg | Source is JPEG; converted to true PNG |
| Seattle_Thunderbirds.png | https://assets.leaguestat.com/whl/logos/214.png | |
| Spokane_Chiefs.png | https://assets.leaguestat.com/whl/logos/215.png | |
| Swift_Current_Broncos.png | https://assets.leaguestat.com/whl/logos/216.png | |
| Tri-City_Americans.png | https://assets.leaguestat.com/whl/logos/217.png | |
| Vancouver_Giants.png | https://assets.leaguestat.com/whl/logos/223.png | Dave's row truncated at "whl/lo" — ID 223 confirmed from chl.ca/whl/whl-teams-directory (HomeID 223, VAN); image reads VANCOUVER GIANTS |
| Victoria_Royals.png | https://assets.leaguestat.com/whl/logos/227.png | Row missing from Dave's truncated message — ID 227 confirmed from chl.ca directory (HomeID/VisitorID 227, VIC); lion-head mark |
| Wenatchee_Wild.png | https://assets.leaguestat.com/whl/logos/222.png | Row missing from Dave's truncated message — ID 222 confirmed from chl.ca directory (VisitorID 222, WEN); image reads WENATCHEE WILD |

All 20 of Dave's complete rows returned HTTP 200 and valid images; the 3
recovered rows were verified the same way and by reading the images.
Most are 500x500 RGBA PNGs.

## Not yet done — baking into the app

The League 3 finished app
(`~/workspace/swhl/app/finish/IKE_League3_FINISHED_GAMES_2026-11-12_before-detail-v2.html`)
currently shows placeholder shield SVGs: its `FC_LG` map holds base64 SVG
shields with the abbreviation text (BDN, CGY, …), and `logo()` /
`tc4Logo()` build `data:image/svg+xml;base64,` URLs from it. These PNGs
are NOT baked in yet — doing that needs the `FC_LG` values swapped for
base64 PNGs and the `data:image/svg+xml` prefix changed to
`data:image/png` at the logo call sites. Nothing in the app was edited
here, and nothing was posted or published.
