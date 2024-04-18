#!/usr/bin/env python

import runloop

@runloop.function
def hello(name: str) -> str:
    return f"Hello {name}!"


@runloop.function
def wait_until_released(scheduler: runloop.Scheduler) -> WaitForHumanApproval:
    awaitable_latch = scheduler.create_latch(
        "my_latch", ApiFulfillment(type=WaitForHumanApproval)
    )

    latch_fulfillment = awaitable_latch.await_result()
    return latch_fulfillment.result
