#!/usr/bin/env python

from pydantic import BaseModel
import runloop

@runloop.function
def hello(name: str) -> str:
    return f"Hello {name}!"


@runloop.latch
class WaitForHumanApproval(BaseModel):
        human_name: str


@runloop.function
def wait_for_approval(scheduler: runloop.Scheduler) -> WaitForHumanApproval:
    awaitable_latch = scheduler.create_latch(
        "my_latch", ApiFulfillment(type=WaitForHumanApproval)
    )

    latch_fulfillment = awaitable_latch.await_result()
    return latch_fulfillment.result
