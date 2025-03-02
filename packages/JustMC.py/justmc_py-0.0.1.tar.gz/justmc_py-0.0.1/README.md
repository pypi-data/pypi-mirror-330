# JustMC.py
JustMC template library in Python.

## Installation
The package can be found on PYPI at [JustMC.py](https://pypi.org/project/JustMC.py/). To install, open terminal
and type in:
```shell
python3 -m pip --upgrade JustMC.py
```
This will install the package.

## Quick Start
The package can be used under the namespace `jmc`. Here's an example program that generate code that counts to 10:
```python
from jmc import *

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
```

## Features
- Templates
- Code Blocks
- Arguments
- Modules