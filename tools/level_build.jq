{
  repo: $me[0].did,
  collection: "app.bsky.feed.post",
  record: {
    "$type": "app.bsky.feed.post",
    createdAt: $t,
    text: ($cap | gsub("^\\n+|\\n+$"; "")),
    reply: {
      root: {uri: $p[0].uri, cid: $p[0].cid},
      parent: {uri: $p[0].uri, cid: $p[0].cid}
    },
    embed: {
      "$type": "app.bsky.embed.video",
      video: $blob[0].blob,
      alt: ($alt | gsub("^\\n+|\\n+$"; ""))
    }
  }
}
| if (.repo | type) == "string" then . else error("repo not string") end
| if .repo == $me[0].did then . else error("repo mismatch") end
| if (.record.text | length) <= 300 then . else error("cap over 300") end
| if (.record.embed.video.ref["$link"] | type) == "string" then . else error("no blob link") end
| if .record.reply.parent.uri == $p[0].uri then . else error("parent uri") end
