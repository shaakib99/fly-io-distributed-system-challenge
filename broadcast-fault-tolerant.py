#!/usr/bin/env python3
from maelstrom import Node, Request
from collections import defaultdict

node = Node()
node_messages = set()

@node.handler
async def topology(req: Request):
    return {"type": "topology_ok"}

@node.handler
async def broadcast(req: Request):
    msg = req.body["message"]
    if msg not in node_messages:
        node_messages.add(msg)
        for n in node.node_ids:
            if n != node.node_id:
                node.spawn(node._send(Request(node.node_id, n, {
                    "type": "gossip",
                    "message": msg,
                })))
    return {"type": "broadcast_ok"}

@node.handler
async def gossip(req: Request):
    msg = req.body["message"]
    if msg not in node_messages:
        node_messages.add(msg)
        for n in node.node_ids:
            if n != req.src:
                node.spawn(node._send(Request(node.node_id, n, {
                    "type": "gossip",
                    "message": msg,
                })))
    return {"type": "gossip_ok"}

@node.handler
async def read(req: Request):
    return {"type": "read_ok", "messages": list(node_messages)}

node.run()
