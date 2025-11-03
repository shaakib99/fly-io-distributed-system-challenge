#!/usr/bin/env python3

from maelstrom import Node, Body, Request

node = Node()

result = {}
seen = set()

@node.handler
async def txn(request: Request):
    txns = request.body["txn"]
    res = []
    broadcasts = []
    for t, key, value in txns:
        if (t, key, value) in seen:
            continue
        
        seen.add((t, key, value))
        if t == "r":
            if key in result:
               value = result[key]
            else:
                value = None
        elif t == "w":
            result[key] = value
            broadcasts.append([t, key, value])
        res.append([t, key, value])
    
    for node_id in node.node_ids:
        if node_id != node.node_id:
            await node.rpc(
                node_id,
                Body(
                    type="txn",
                    txn=broadcasts
                )
            )


    return {
        "type": "txn_ok",
        "txn": res
    }

node.run()