---
#title: 'State-Averaged Orbital-Optimized VQE: An electronic structure excite-state solver utilizing quantum computers'
title: 'State-Averaged Orbital-Optimized VQE: A quantum algorithm for the democratic description of ground and excited electronic states'
tags:
  - Python
  - chemistry
  - quantum
  - dynamics
  - hybrid
authors:
  - name: Martin Beseda
    orcid: 0000-0001-5792-2872
    corresponding: true
#    equal-contrib: true
    affiliation: "1, 3, 5" 
  - name: Silvie Illésová
    orcid: 0009-0002-5231-3714
#    equal-contrib: true
    affiliation: "1, 2, 3"
  - name: Saad Yalouz
    orcid: 0000-0002-8818-3379
    affiliation: 4
  - name: Bruno Senjean
    orcid: 0000-0003-1706-015X
#    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 1
affiliations:
 - name: ICGM, Université de Montpellier, CNRS, ENSCM, Montpellier, France
   index: 1
 - name: VSB - Technical University of Ostrava, 708 00 Ostrava, Czech Republic
   index: 2
 - name: IT4Innovations, VSB – Technical University of Ostrava, 17. listopadu 2172/15, 708 00 Ostrava-Poruba, Czech Republic
   index: 3
 - name: Laboratoire de Chimie Quantique, Institut de Chimie, CNRS/Université de Strasbourg, 4 rue Blaise Pascal, 67000 Strasbourg, France
   index: 4
 - name: Dipartimento di Ingegneria e Scienze dell'Informazione e Matematica, Università dell'Aquila, via Vetoio, I-67010 Coppito-L'Aquila, Italy
   index: 5
date: 16 June 2023
bibliography: paper.bib

## Optional fields if submitting to a AAS journal too, see this blog post:
## https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
#aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
#aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

The electronic structure problem is one of the main problems in modern theoretical chemistry. While there are many 
already-established methods both for the problem itself and its applications like semi-classical or quantum dynamics, 
it remains a computationally demanding task, effectively limiting the size of solved problems. Fortunately, it seems, 
that offloading some parts of the computation to *Quantum Processing Units (QPUs)* may offer significant speed-up, 
often referred to as *quantum supremacy* or *quantum advantage*. Together with the potential advantage, this approach 
simultaneously presents several problems, most notably naturally occurring quantum decoherence, hereafter denoted as 
*quantum noise* and lack of large-scale quantum computers, making it necessary to focus on Noisy-Intermediate Scale 
Quantum computers when developing algorithms aspiring to near-term applications. SA-OO-VQE package aims to answer both 
these problems with its hybrid quantum-classical conception based on a typical Variational Quantum Eigensolver approach,
as only a part of the algorithm utilizes offload to QPUs and the rest is performed on a classical computer, thus 
partially avoiding both quantum noise and the lack of *quantum bits (qubits)*. The SA-OO-VQE has the ability to treat 
degenerate (or quasi-degenerate) states on the same footing, thus avoiding known numerical optimization problems arising 
in state-specific approaches around avoided crossings or conical intersections.


# Statement of need

Recently, quantum chemistry is one of the main areas-of-interest in *Quantum Computing (QC)*[@reiher2017elucidating; 
@mcardle2020quantum; @bauer2020quantum]. That said, in many real-life applications, it is necessary to treat
both the ground and excited states accurately and on an equal footing. The problem is magnified when the 
Born-Oppenheimer approximation breaks down due to a strong coupling among degenerate or quasi-degenerate states, 
most notably the ground and the first excited state, for which the accurate description requires (computationally demanding) 
multi-configurational approaches. A good example of such a case is a photoisomerization mechanism of the 
rhodopsin chromophore, which progresses from the initial photoexcitation of the *cis* isomer over the relaxation in the first excited state 
towards a conical intersection, where the population is transferred back to the ground state of the *trans* isomer. To describe such 
a process thoroughly, one must compute not only relevant *potential energy surfaces (PESs)*, but also their gradients 
w.r.t. nuclear displacements, utilized further in molecular dynamics simulations. Finally, a description of the conical 
intersection can be done by obtaining *non-adiabatic couplings (NACs)*.

Formally, the approaches describing PES topology, topography, and non-adiabatic couplings require Hamiltonian 
diagonalization, which represents the most significant bottleneck. Considering classical methods like State-Averaged
Multi-Configurational Self-Consistent Field[@helgaker2013molecular], only small complete active spaces have to be used
for the large computational overhead inherently present. However, such an approximation brings missing dynamical 
correlation treatment, inducing the need to recover it ex-post, usually via some of the quasi-degenerate perturbation 
techniques[@granovsky2011extended; @park2019analytical]. On the other hand, QC brings the possibility of large complete
active spaces back, thus retaining a substantial part of the dynamical correlation. Moreover, the dynamical correlation can
be also retrieved a posteriori utilizing QPUs only at the expense of more measurements, with no additional demands on
hardware infrastructure[@takeshita2020increasing].

*State-Averaged Orbital-Optimization Variational Quantum Eigensolver (SA-OO-VQE)* method addresses the above-mentioned 
problems and provides a way to compute both PES gradients and NACs analytically[@yalouz2021state; 
@yalouz2022analytical;@omiya2022analytical]. Authored by Yalouz *et al.*, there is an exemplary implementation focusing on
the pedagogical aspect and relying on matrix-vector multiplications rather than actual measurements, avoiding 
the utilization of real QC infrastructure. Our implementation differs in a way that it aims to be a production-ready 
solver utilizing both QCs and classical computing infrastructure efficiently, being able to run with
different backgrounds, utilizing the Qiskit toolbox interface. The whole code is written in Python3, with YAML scripts 
enabling its fast installation and usage.

The results are illustrated on the molecule of formaldimine, which can be seen in \autoref{fig:formaldimine}.
Their comparison with the ones obtained via Molcas[@li2023openmolcas] implementation of 
Complete Active-Space Self-Consistent Field[@malmqvist1989casscf] are shown in 
\autoref{fig:energies},\autoref{fig:grad0} and \autoref{fig:nac}. All the computations were computed with 3 active 
orbitals containing 4 electrons and with _STO-3G_ basis set.

![Molecule of formaldimine being described with bending and dihedral angles denoted $\alpha$ and $\phi$, 
respectively.
\label{fig:formaldimine}](formaldimine.svg){ width=80% }

![Comparison of potential energy depending on bending angle $\alpha$ in formaldimine molecule with dihedral angle 
$\phi = 90^\circ$.
\label{fig:energies}](energies.svg){ width=80% }

![Comparison of ground-state gradients with bending angle $\alpha = 130^\circ$ and dihedral angle $\phi = 90^\circ$
in formaldimine molecule.
\label{fig:grad0}](grad_0_1d.svg){ width=80% }

![Comparison of total non-adiabatic couplings on bending angle $\alpha = 130^\circ$ and dihedral angle $\phi = 90^\circ$
in formaldimine molecule.
\label{fig:nac}](total_nac_1d_.svg){ width=80% }

# Features
With SA-OO-VQE you can obtain the following quantities:

* Potential energy surfaces
* Circuit (or Ansatz) gradients
* Orbital gradients
* Gradients of potential energy surfaces
* Non-adiabatic couplings

Also, for numerical optimization, you can use any of the optimizers supported by Qiskit[^1] and our own implementation of

* Particle Swarm Optimization

[^1]: https://qiskit.org/documentation/stubs/qiskit.algorithms.optimizers.html

# Getting Started
The package is prepared with a priority of being very simple to use and the concise documentation can be found at 
[sa-oo-vqe-qiskit.rtfd.io](https://sa-oo-vqe-qiskit.rtfd.io). To simplify the installation part, we recommend
utilizing the Conda management system[^2] together with the prepared `environment.yml` file.

At first, users should clone the repository.

```
git clone git@gitlab.com:MartinBeseda/sa-oo-vqe-qiskit.git
```

And install all the dependencies.

```
$ cd sa-oo-vqe-qiskit
$ conda env create -f environment.yml
$ conda activate saoovqe-env
$ python3 -m pip install .
```

These commands run in a terminal that will download and install all the necessary packages. The package availability can be 
tested afterward simply by importing the package and looking at its version.

```
$ python3

>>> import saoovqe
>>> saoovqe.__version__
```

Finally, usage examples are located both in the _examples_ folder and in the documentation.

[^2]: https://docs.conda.io/en/latest/

# Acknowledgements
This work/project was publicly funded through ANR (the French National Research Agency) under 
the "Investissements d’avenir" program with the reference ANR-16-IDEX-0006. This work was also
supported by the Ministry of Education, Youth and Sports of the Czech Republic through 
the e-INFRA CZ (ID:90254).

# References