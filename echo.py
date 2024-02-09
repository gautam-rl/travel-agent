#!/usr/bin/env python

import runloop

@runloop.loop
def echo(metadata: dict[str, str], greeting: list[str]) -> tuple[list[str], dict[str, str]]:
    return [f"Hello runloop!!! {greeting[0]}"], metadata
