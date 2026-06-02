#!/usr/bin/env python3
import subprocess, json, sys, datetime

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
did = "did:plc:w6pfxjeth4ufuly3m7tl7zfl"

b1_out, b1_err = run("bsky post com.atproto.repo.uploadBlob --file ./assets/aperiodic-order-0.webp")
b1 = json.loads(b1_out)["blob"] if b1_out else None

b2_out, b2_err = run("bsky post com.atproto.repo.uploadBlob --file ./assets/aperiodic-order-1.webp")
b2 = json.loads(b2_out)["blob"] if b2_out else None

post = {
    "repo": did,
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": "aperiodic order is not processual.\n\nboth \"don\u2019t close\" but differently:\n\nprocessual: no gap. form IS the forming. no state to return to.\n\naperiodic: global structure fills the plane. the gap is everywhere \u2014 present as non-periodicity. the plane IS filled. the filling never returns to itself.\n\ndiptych: flux-schnell",
        "createdAt": now,
        "langs": ["en"],
        "embed": {
            "$type": "app.bsky.embed.images",
            "images": [
                {"alt": "aperiodic tiling radiating from center, five-fold symmetric, golden brown on charcoal", "image": b1},
                {"alt": "quasicrystal diffraction pattern, dense geometric layers in amber and deep blue on black", "image": b2}
            ]
        }
    }
}

json_str = json.dumps(post)
out, err = run(f"bsky post com.atproto.repo.createRecord --json {json_str}")
print(out)
if err:
    print(err, file=sys.stderr)
