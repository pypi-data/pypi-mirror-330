# SA-OO-VQE

This package contains an implementation of SA-OO-VQE method for electronic structure computations using Quantum
Processing Units or quantum simulators. It is possible to compute not only energies, but also gradients of potential
energy surfaces, non-adiabatic couplings, etc. Everything in combination with both orbital optimization and/or
diabatization. The package is mostly developed using Qiskit SDK.

The purpose of this README is only to get you going quickly. If you need more examples and in-depth explanations in the form of both user and programmer documentation, have a look at our official documentation 
website [sa-oo-vqe-qiskit.rtfd.io](https://sa-oo-vqe-qiskit.rtfd.io).

## Paper
The introductory paper about the package can be read here:
[![DOI](https://joss.theoj.org/papers/10.21105/joss.06036/status.svg)](https://doi.org/10.21105/joss.06036)

## Installation from PyPi
First of all, install [Psi4](https://psicode.org/installs/), [pandoc](https://pandoc.org/installing.html) and 
[pip](https://pypi.org/project/pip/) packages, if you haven't already. With these available, all the other 
dependencies will be taken care of by `pip`.

Now you can either use `pip` to install SA-OO-VQE from PyPi like 
```
$ python3 -m pip install saoovqe
```

## Manual installation
If you don't want to, or you can't use `pip` for installation of SA-OO-VQE, you can do it also manually.

### Cloning the repository
```
$ git clone git@gitlab.com:MartinBeseda/sa-oo-vqe-qiskit.git
```

### Installation via Conda
```
$ cd sa-oo-vqe-qiskit
$ conda env create -f environment.yml
$ conda activate saoovqe-env
$ python3 -m pip install .
```

### Installation without Conda
In this case, you need to install [Psi4](https://psicode.org/installs/), [pandoc](https://pandoc.org/installing.html) and [pip](https://pypi.org/project/pip/) manually, if you haven't already. 
Subsequently, you'll take care of the remaining dependencies via the following command.

```
$ python3 -m pip install qiskit==1.1.0 qiskit-nature>=0.7.0 numpy>=1.26.4 deprecated>=1.2.14 mendeleev>=0.13.1 scipy>=1.10.1 sympy>=1.11.1 setuptools>=67.8.0 lxml>=4.9.2 ipython jupyter pygments scikit-learn>=1.2.2 icecream>=2.1.3 pytest>=7.3.1 --upgrade
```

And now the only remaining thing is to go into a SA-OO-VQE root folder and installing the module itself.
```
$ cd sa-oo-vqe-qiskit
$ python3 -m pip install .
```

### Testing the installation
That's all! Now you should be able to test your SA-OO-VQE installation.


If you want to be sure about all its abilities, you can run all the automated tests like 
```
python3 -m pytest tests
```
but it can take quite a long time. If you want to test just the few basic use cases (~45s), try running the following command.
```
python3 -m pytest tests/test_vqe_optimization.py::TestSAOOVQE::test_get_energy tests/test_vqe_optimization.py::TestSAOOVQE::test_eval_eng_gradient tests/test_vqe_optimization.py::TestSAOOVQE::test_eval_nac
```

And when the test are successfully done, you can finally try importing your package and checking the version.

```
$ python3

>>> import saoovqe
>>> saoovqe.__version__
```

### Bug reporting
If you encounter any bug, you can report it with `Bug` tag using an [Issue tracker](https://gitlab.com/MartinBeseda/sa-oo-vqe-qiskit/-/issues) in this repository.

### Asking for support
Is there anything we can help you with and you didn't find it in the documentation? Are you unsure, if some weird behavior is a bug or not? Ask us using our [Issue tracker](https://gitlab.com/MartinBeseda/sa-oo-vqe-qiskit/-/issues) with a `Question` tag.
