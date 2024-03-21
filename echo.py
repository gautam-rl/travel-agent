#!/usr/bin/env python

import runloop

@runloop.function
def func_multi_arg_echo(name: str) -> str:
    return f"Hello {name}!"
