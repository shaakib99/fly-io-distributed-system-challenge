#!/usr/bin/env python3

from maelstrom import Node, Request, Body
from collections import defaultdict

node = Node()

logs = defaultdict(list)
committed_offset = defaultdict(int)
offset_counter = defaultdict(int)

@node.handler
async def send(req: Request) -> Body:
    msg = req.body['msg']
    key = req.body['key']

    # Forward all sends to leader
    if node.node_id != node.node_ids[0]:
        return await node.rpc(node.node_ids[0], req.body)

    # Leader path
    offset = offset_counter[key]
    offset_counter[key] += 1
    entry = (offset, msg)
    logs[key].append(entry)

    # replicate
    for nid in node.node_ids:
        if nid != node.node_id:
            await node.rpc(nid, {"type": "append", "key": key, "offset": offset, "msg": msg})

    return {"type": "send_ok", "offset": offset}


@node.handler
async def poll(request: Request) -> Body:
    offsets = request.body['offsets']
    messages = {}

    for key, offset in offsets.items():
        key_logs = logs[key]
        msgs = [[off, msg] for off, msg in key_logs if off >= offset]
        messages[key] = msgs

    return {'type': 'poll_ok', 'msgs': messages}

@node.handler
async def commit_offsets(request: Request) -> Body:
    offsets = request.body['offsets']
    for key, offset in offsets.items():
        committed_offset[key] = max(committed_offset[key], offset)  
    return {'type': 'commit_offsets_ok'}

@node.handler
async def list_committed_offsets(request: Request) -> Body:
    return {'type': 'list_committed_offsets_ok', 'offsets': committed_offset}

@node.handler
async def append(req: Request) -> Body:
    key = req.body["key"]
    offset = req.body["offset"]
    msg = req.body["msg"]
    logs[key].append((offset, msg))
    return {"type": "append_ok"}

node.run()