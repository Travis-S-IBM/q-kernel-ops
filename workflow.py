"""Entrypoint for CLI
Available commands:
1. Register the session in disk space
```shell
python workflow.py authentication --channel="cloud" --token="your_very_long_token" --instance="ibm-q/open/main"
```
2. Run only the kernel flow with seed1 and seed2.
```shell
python workflow.py kernel_flow --circuit_tpl_id=[2,5]
```
3. Run only the kernel flow with in order to generate a full matrix data.
```shell
python workflow.py kernel_flow --circuit_tpl_id=[5] --matrix_size=[1,1]
:warning: You can't use the option --seed1 and --seed2 if you use --matrix_size
```
4. Run only the completion flow with in order to generate a full matrix data.
```shell
python workflow.py kernel_flow --file_name="kernels-2-ideal.csv" --nb_qubits=3
:warning: You can't use the option --seed1 and --seed2 if you use --matrix_size
```
5. To decode and access the data from metadata kernel files
```
python workflow.py view_kernel --file_name="kernels-2-ideal.csv"
```
6. To decode and access the data from the telemetry file
```
python workflow.py view_telemetry
```
7. To decode and access the data from completion matrix files
```
python workflow.py view_matrix --file_name="kernels-2-ideal.csv.npy"
```
8. To sync data files with another folder
```
python workflow.py sync_data
```
"""
import fire

from src import Workflow


if __name__ == "__main__":
    fire.Fire(Workflow)
