#!/usr/bin/env python3

from maelstrom import Node, Body, Request

node = Node()

committed = {}
seen = set()

@node.handler
async def txn(request: Request):
    txns = request.body["txn"]
    res = []
    broadcasts = []
    buffer = {}
    for t, key, value in txns:
        if (t, key, value) in seen:
            continue
        
        seen.add((t, key, value))
        if t == "r":
            if key in buffer:
               value = buffer[key]
            elif key in committed:
               value = committed[key]
            else:
                value = None
        elif t == "w":
            buffer[key] = value
            broadcasts.append([t, key, value])
        res.append([t, key, value])

    committed.update(buffer)

    for node_id in node.node_ids:
        if node_id != node.node_id:
            await node.rpc(
                node_id,
                Body(
                    type="replicate",
                    txn=broadcasts
                )
            )


    return {
        "type": "txn_ok",
        "txn": res
    }

@node.handler
async def replicate(request: Request):
    txns = request.body["txn"]
    broadcasts = []
    for t, key, value in txns:
        if (t, key, value) in seen: continue
        seen.add((t, key, value))
        if t == "w":
            committed[key] = value
            broadcasts.append([t, key, value])

    for node_id in node.node_ids:
        if node_id != node.node_id:
            await node.rpc(
                node_id,
                Body(
                    type="replicate",
                    txn=broadcasts
                )
            )

    return {
        "type": "replicate_ok"
    }

node.run()