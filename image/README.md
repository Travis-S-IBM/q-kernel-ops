# q-kernel-ops image

Build docker images to run quantum kernel completion algorithm

```sh
./build-build.sh <ARCH>
```
where ARCH is one of: 
  - s390x
  - ppc64l3
  - amd64

## default parameters

defaults to s390x image build/anaconda architecture

with `TAGARCH=z` for a short version/tag  



### Anaconda versioning

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
