#!/usr/bin/env python3

from maelstrom import Node, Body, Request
from collections import defaultdict

node = Node()

node_message_map = defaultdict(list)

@node.handler
async def broadcast(request: Request):
    message = request.body["message"]
    node_message_map[node.node_id].append(message)
    return {"type": "broadcast_ok"}

@node.handler
async def read(request: Request):
    return {"type": "read_ok", "messages": node_message_map[node.node_id]}

@node.handler
async def topology(request: Request):
    return {"type": "topology_ok"}

node.run()