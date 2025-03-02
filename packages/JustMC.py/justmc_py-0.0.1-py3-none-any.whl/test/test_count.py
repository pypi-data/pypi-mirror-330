from src.jmc import *

index_variable = Variable("index")

template = Template(
    Event("player_join"),
    [
        Block(
            "repeat_multi_times",
            [
                Argument("variable", index_variable),
                Argument("amount", Number(10))
            ],
            [
                Block(
                    "player_send_message",
                    [
                        Argument("messages", PluralArgument([
                            index_variable
                        ]))
                    ]
                )
            ]
        )
    ]
)

module = Module([template])
url = module.upload()
print(f"Do \"/module loadUrl force {url}\" to load the program.")