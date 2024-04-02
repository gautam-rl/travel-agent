#!/usr/bin/env python

import runloop

@runloop.function
def hello(name: str) -> str:
    return f"Hello {name}!"
