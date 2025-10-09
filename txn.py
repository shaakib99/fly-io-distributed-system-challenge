#!/usr/bin/env python3

from maelstrom import Node, Body, Request

node = Node()

result = {}

@node.handler
async def txn(request: Request):
    txns = request.body["txn"]
    res = []
    for t, key, value in txns:
        if t == "r":
            if key in result:
               value = result[key]
            else:
                value = None
        elif t == "w":
            result[key] = value

        res.append([t, key, value])


    return {
        "type": "txn_ok",
        "txn": res
    }

node.run()