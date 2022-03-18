# Operationalizing Quantum Kernels

QAMP issue : [#7](https://github.com/qiskit-advocate/qamp-spring-22/issues/7)

Paper based : [link to arxiv](https://arxiv.org/abs/2112.08449)

## Usefull acronyms
- DLC : DLC is a C++ compiler, which turns the ONNX ML calls into IBM Z15 or IBM Z16 instruction set depending on the flags you use, IBM Z16 having the AI acceleration calls & hardware to support it.  The result is a small statically-compiled library that you can call from either C++ or from python.
- PSD : Positive Semi Define matrix, matrix which have all of its eignevalue `≥ 0` and at least one `= 0`


## Resources
 - Golub, Gene H., and Charles F. Van Loan. Matrix computations (4th Edition). JHU press, 2013.
 - Boyd, Stephen, Stephen P. Boyd, and Lieven Vandenberghe. Convex optimization. Cambridge university press, 2004.
