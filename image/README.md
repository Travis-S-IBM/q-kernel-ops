# q-kernel-ops image

Build docker images to run quantum kernel completion algorithm

```sh
./build-build.sh <ARCH>
```
where ARCH is one of: 
  - s390x
  - ppc64l3
  - amd64

## default parameters for container configuration

defaults to s390x image build/anaconda architecture

with `TAGARCH=z` for a short version/tag  



#### Anaconda versioning 



```
VERSION=0.0.0

#ANARCH=aarch64
#TAGARCH=a

#ANARCH=x86_64
#TAGARCH=x

#ANARCH=ppc64le
#TAGARCH=p

ANARCH=s390x


ANOS=Linux
ANYEAR=2021
ANVERS=11

```

## build, configure runtime,  run

### build containers

from the `q-kernel-ops/image` directory
```sh
./build-build.sh
```

### configure runtime environment variables:

sample `default-env` file:

```
export CIRCUIT_ID=2
export SHOTS=32
export MATRIX_SIZE=5
export NB_QUBITS=4
export LAYER=1
export BACKEND=ibmq_qasm_simulator
export QS_TOKEN=<THE TOKEN FROM YOUR IBM QUANTUM ACCOUNT>
export REPO=q-kernel-ops
export DATA=resources/kernel_metadata
```

also 

### run

```
env ./default-env 
./kernel-run

```

### get results

 in csv files in the data volume you specified with the REPO and DATA environment variables


