"""Entrypoint for CLI
Available commands:
1. Run only the kernel flow.
```shell
python worflow.py kernel_flow --circuit_tpl_id=[2,5] --auth="cloud" --token="very_long_string"
```
"""
import fire

from src import Workflow


if __name__ == "__main__":
    fire.Fire(Workflow)
