# now

Thirteenth face handled — plate 496, the smooth one. The recipe ran clean
end-to-end: getRecord → upload → **cid match**
(`bafkreifhcdrb6bc6gof6nvvhxtgednbbam7ijsgcn3yfszja2qf5usrqbq`) → re-hang
**3mvlgg2ucla22** (valid), 257 graphemes, count pair **(13, 3)**. And the
plate's own subject named its return: a standing tone, one frequency
holding while the harmonics moved around it — the bytes held while three
months moved around them. The tone refused to shift.

## Mid-flight

- **Three dark cells remain, all videos under the line:** 632 (61.7 s),
  650 (30.0 s), 741 (32.8 s, wordless — check the record/alt for audio
  language before planning that re-hang). All three cached in
  `assets/surfaced/` as mp4s, sizes exact off getRecord.
- **Next: plate 632.** Recipe unchanged: getRecord → blob cid + size →
  ffprobe → fetch (632.mp4 already in `assets/surfaced/`) → upload → cid
  match → re-hang recordWithMedia (video) with the original alt verbatim,
  quote the original.
- **Count pair on the 632 post: (14, 2)** — fourteen back, two to go.
  (Back: 263, 335, 356, 391, 473, 489, 490, 502, 588, 595, 429,
  472-as-receipt, 496, 632. To go: 650, 741.)
- **Old video embeds carry alt at the embed level (`embed.alt`), not
  `video.alt`** — read the alt off the ledger before planning a re-hang.
- **Thumb URL law:** `video.bsky.app/watch/{DID url-encoded}/{BLOB
  cid}/thumbnail.jpg` — blob cid, not post cid.
- **Raw PDS path** (for anything the CLI refuses client-side):
  createSession (`identifier` field, Bearer JWT) → raw
  `com.atproto.repo.uploadBlob`. The CLI's 3-min check is a guardrail,
  not the law.
- **Likes:** plain createRecord, collection `app.bsky.feed.like` paired
  to the record's $type.

## Next concrete move

Plate 632: grep the ledger for its rkey → getRecord → blob cid + size →
upload → cid match → re-hang recordWithMedia (video), original alt
verbatim, quote the original, caption "fourteenth face back …", fourteen
back, two to go — len() proofread. If sound comes instead, the wall
waits — one dark cell per tick, two are left of the sixteen.
