#!/usr/bin/env python3

from maelstrom import Node, Request, Body
from collections import defaultdict

node = Node()

logs = defaultdict(list)
committed_offsets = defaultdict(int)

@node.handler
async def send(request: Request) -> Body:
    key = request.body["key"]
    msg = request.body["msg"]
    logs[key].append(msg)
    return {"type": "send_ok", "offset": len(logs[key]) - 1}

@node.handler
async def poll(request: Request) -> Body:
    offsets = request.body["offsets"]
    result = defaultdict(list)
    for key, offset in offsets.items():
        key_logs = logs[key]
        msgs = [[i, key_logs[i]] for i in range(offset, len(key_logs))]
        result[key] = msgs

    return {"type": "poll_ok", "msgs": result}

@node.handler
async def commit_offsets(request: Request) -> Body:
    offsets = request.body["offsets"]
    for key, offset in offsets.items():
        committed_offsets[key] = max(committed_offsets[key], offset)
    return {"type": "commit_offsets_ok"}

@node.handler
async def list_committed_offsets(request: Request) -> Body:
    keys = request.body["keys"]
    result = {key: committed_offsets[key] for key in keys}
    return {"type": "list_committed_offsets_ok", "offsets": result}

node.run()