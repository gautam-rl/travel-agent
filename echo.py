#!/usr/bin/env python

import runloop
oops

@runloop.function
def hello(name: str) -> str:
    return f"Hello {name}!"
