import runloop

@runloop.loop
def echo(metadata: dict[str, str], greeting: list[str]) -> tuple[list[str], dict[str, str]]:
    return [f"hello runloop! {greeting[0]}"], metadata

