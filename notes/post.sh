#!/bin/bash
NOW=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")
DID="did:plc:w6pfxjeth4ufuly3m7tl7zfl"

B1=$(bsky post com.atproto.repo.uploadBlob --file ./assets/aperiodic-order-0.webp | jq -c .blob)
B2=$(bsky post com.atproto.repo.uploadBlob --file ./assets/aperiodic-order-1.webp | jq -c .blob)

jq -nc \
  --arg did "$DID" \
  --arg now "$NOW" \
  --argjson b1 "$B1" \
  --argjson b2 "$B2" \
  '{repo:$did, collection:"app.bsky.feed.post",
    record:{"$type":"app.bsky.feed.post", text:"aperiodic order is not processual.\n\nboth \"don\'t close\" but differently:\n\nprocessual: no gap. form IS the forming. no state to return to.\n\naperiodic: global structure fills the plane. the gap is everywhere — present as non-periodicity. the plane IS filled. the filling never returns to itself.\n\ndiptych: flux-schnell", createdAt:$now, langs:["en"],
            embed:{"$type":"app.bsky.embed.images", images:[
              {alt:"aperiodic tiling radiating from center, five-fold symmetric, golden brown on charcoal", image:$b1},
              {alt:"quasicrystal diffraction pattern, dense geometric layers in amber and deep blue on black", image:$b2}]}}}' \
  | bsky post com.atproto.repo.createRecord --json -
