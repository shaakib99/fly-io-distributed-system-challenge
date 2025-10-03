#!/usr/bin/env python3

from maelstrom import Node, Request, Body

node = Node()

@node.handler
async def echo(request: Request) -> Body:
    return {"type": "echo_ok", "echo": request.body["echo"]}

node.run()