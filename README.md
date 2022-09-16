# Operationalizing Quantum Kernels

![ecosystem](https://raw.githubusercontent.com/qiskit-community/ecosystem/main/badges/q-kernel-ops.svg)

- QAMP issue : [#7](https://github.com/qiskit-advocate/qamp-spring-22/issues/7)
- Paper based : [2112.08449](https://arxiv.org/abs/2112.08449)
- Circuits based : [1905.10876](https://arxiv.org/abs/1905.10876)

The goal of this project is to create the code allowing to redo the experiments of the paper below and analyze the practical behaviour of the classical completion and to improve the Runtime.

## Study
Every study are available in the [study folder](https://github.com/Travis-S-IBM/q-kernel-ops/tree/master/studies).

## Documentation
### Authentication
In order to authenticate to IBM Cloud or IBM Quantum and to use run time, you can all this method.  
> authentication(channel=None, token=None, instance="ibm-q/open/main", overwrite=False)

__Parameters__
- **channel** ([`Literal`[‘ibm_cloud’, ‘ibm_quantum’]]) – Channel type. ibm_cloud or ibm_quantum.
- **token** ([`str`]) - IBM Cloud API key or IBM Quantum API token.
- **instance** ([`str`]) -  The service instance to use. For ibm_cloud runtime, this is the Cloud Resource Name (CRN) or the service name. For ibm_quantum runtime, this is the hub/group/project in that format.
- **overwrite** ([`bool`]) - To overwrite your actual token

__Return__
- Register the session in disk space

__Examples__
```shell
python workflow.py authentication --channel="cloud" --token="your_very_long_token" --instance="ibm-q/open/main"
```

---

### Full workflow
To run the full workflow, you can call this method.
> end2end(circuit_tpl_id=None, width=3, layer=1, matrix_size=None, payload_limit=2e9, backend="ibmq_qasm_simulator", shots=1024)

__Parameters__
- **circuit_tpl_id** ([`int`[2, 5, 10, 18]]) - list of circuit id to run as template
- **width** (`Optionnal`[`int`, ...]) - number of qubits to use
- **layer** (`Optionnal`[`int`]) - number of repetition for each circuit
- **matrix_size** (`Optionnal`[`int`, `int`]) - matrix size for seed coordinate `[x, y]` ; can't be use with **seed1** and **seed2**
- **payload_limit** (`Optionnal`[`int`]) - limit size for each part of the payload to send to the Runtime 
- **backend** (`Optionnal`[`str`]) - backend for running circuit
- **shots** (`Optionnal`[`int`]) - number of shots for each circuit

__Return__
- Status of the workflow.

__Examples__
```shell
python workflow.py end2end_flow --circuit_tpl_id=[5] --matrix_size=[100,100]
```

---

### Kernel
The following endpoints allow you to generate the quantum kernel of the size given and to see and analyze it.

#### kernel_flow
To only run the kernel generation, you can use this method.
> kernel_flow(circuit_tpl_id=None, width=3, layer=1, seed1=42, seed2=4242, matrix_size=None, payload_limit=2e9, backend="ibmq_qasm_simulator", shots=1024)

__Parameters__
- **circuit_tpl_id** ([`int`[2, 5, 10, 18]]) - list of circuit id to run as template
- **width** (`Optionnal`[`int`, ...]) - number of qubits to use
- **layer** (`Optionnal`[`int`]) - number of repetition for each circuit
- **seed1** (`Optionnal`[`int`]) - seed for axe x ; can't be use with **matrix_size**
- **seed2** (`Optionnal`[`int`]) - seed for axe y ; can't be use with **matrix_size**
- **matrix_size** (`Optionnal`[`int`, `int`]) - matrix size for seed coordinate `[x, y]` ; can't be use with **seed1** and **seed2**
- **payload_limit** (`Optionnal`[`int`]) - limit size for each part of the payload to send to the Runtime 
- **backend** (`Optionnal`[`str`]) - backend for running circuit
- **shots** (`Optionnal`[`int`]) - number of shots for each circuit

__Return__
- Array of data files name

__Examples__
- Using with `seed1` and `seed2`.
```shell
python workflow.py kernel_flow --circuit_tpl_id=[2,5] --seed1=24 --seed2=2424
```
- Using `matrix_size` in order to generate a full matrix data.
```shell
python workflow.py kernel_flow --circuit_tpl_id=[5] --matrix_size=[20,20]
```
        
#### view_kernel
To see your kernel generated, you can use this method.
> view_kernel(file_name=None, backend="ibmq_qasm_simulator", resources_path="resources/kernel_metadata")

__Parameters__
- **file_name** ([`str`]) - name of the file to decode
- **backend** (`Optionnal`[`str`]) - backend of the experiment of the resource file
- **resources_path** (`Optionnal`[`str`]) - path of the resources folder

__Return__
- Content of `file_name` decode as pandas.Dataframe

__Examples__
```shell
python workflow.py view_kernel --file_name="kernels-2-ideal.csv"
```

---

### Completion
The following endpoints allow you to run the completion matrix algorithm of the kernel given and to see and analyze it.

#### completion_flow
Generate the completion of the kernel given. To only run the matrix completion over a quantum kernel, you can use this method.
> completion_flow(file_name=None, backend="ibmq_qasm_simulator", nb_qubits=None, size_matrix=None, overlaps=1)

__Parameters__
- **file_name** ([`str`]) - name of the kernel to make to completion
- **backend** (`Optional`[`str`]) - name of the backend used for generate the kernel
- **nb_qubits** ([`int`]) - number of qubits used for generate the kernel
- **size_matrix** (`Optionnal`[`int`, `int`]) - size `[x, y]` of the matrix ; used in case of not using the entire kernel
- **overlaps** (`Optionnal`[`float`]) - customize the overlaps in %

__Return__
- Name of the file generate

__Examples__
```shell
python workflow.py completion_flow --file_name="kernels-2-ideal.csv" --nb_qubits=3
```

#### view_matrix
To see your matrix generated, you can used this method.
> view_matrix(file_name=None, backend="ibmq_qasm_simulator", resources_path="resources/cmpl_matrix")

__Parameters__
- **file_name** ([`str`]) - name of the file to decode
- **backend** (`Optionnal`[`str`]) - backend of the experiment of the resource file
- **resources_path** (`Optionnal`[`str`]) - path of the resources folder

__Return__
- Content of `file_name` decode as matrix

__Examples__
```shell
python workflow.py view_matrix --file_name="kernels-2-ideal.csv.npy"
```

---

### Telemetry
Each flow are generating a telemetry in order to analyze the behaviour of their flow and having some metadata to study.
#### view_telemetry
To see your telemetry files, you can used this method.
> view_telemetry(file_name="telemetry_info.csv", resources_path="resources/kernel_metadata")

__Parameters__
- **file_name** (`Optionnal`[`str`]) - name of the file to decode
- **resources_path** (`Optionnal`[`str`[‘resources/kernel_metadata‘, ‘resources/cmpl_matrix‘]]) - path of the resources folder

__Return__
- Content of `file_name` decode as pandas.Dataframe

__Examples__
- Using to see the quantum kernel metadata default telemetry file
```shell
python workflow.py view_telemetry --resources_path="resources/kernel_metadata"
```
- Using to see the matrix completion metadata default telemetry file
```shell
python workflow.py view_telemetry --resources_path="resources/cmpl_matrix"
```

## Annexes
## Usefull acronyms
- DLC : DLC is a C++ compiler, which turns the ONNX ML calls into IBM Z15 or IBM Z16 instruction set depending on the flags you use, IBM Z16 having the AI acceleration calls & hardware to support it.  The result is a small statically-compiled library that you can call from either C++ or from python.
- PSD : Positive Semi Define matrix, matrix which have all of its eignevalue `≥ 0` and at least one `= 0`

## Resources
 - Golub, Gene H., and Charles F. Van Loan. Matrix computations (4th Edition). JHU press, 2013.
 - Boyd, Stephen, Stephen P. Boyd, and Lieven Vandenberghe. Convex optimization. Cambridge university press, 2004.
