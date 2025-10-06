#!/usr/bin/env python3

from maelstrom import Node, Request, Body
import asyncio

node = Node()

counter = 0

@node.handler
async def add(request: Request) -> Body:
    global counter
    value = request.body["delta"]
    counter += value
    for n in node.node_ids:
        if n != node.node_id:
            node.spawn(node._send(Request(
                node.node_id,
                n,
                {
                    "type": "add",
                    "delta": value,
                },
            )))
    return {"type": "add_ok"}

@node.handler
async def read(request: Request) -> Body:
    return {"type": "read_ok", "value": counter}

node.run()



