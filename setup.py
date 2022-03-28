"""Setup file for Operationalizing Quantum Kernels project."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fp:
    install_requires = fp.read()

setuptools.setup(
    name="q-kernel-ops",
    description="Operationalizing Quantum Kernels",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires='>=3.7'
)
