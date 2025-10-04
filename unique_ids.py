#!/usr/bin/env python3

from maelstrom import Node, Body, Request
import uuid

node = Node()
def generate_id() -> str:
    return str(uuid.uuid4())

@node.handler
async def generate(request: Request):
    return {
        "type": "generate_ok",
        "id": generate_id()
    }

node.run()