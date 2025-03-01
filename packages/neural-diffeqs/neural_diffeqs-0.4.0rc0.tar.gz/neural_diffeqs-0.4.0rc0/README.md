# ![neural-diffeqs](/docs/assets/neural-diffeqs.logo.svg)

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/neural_diffeqs.svg)](https://pypi.python.org/pypi/neural_diffeqs/)
[![PyPI version](https://badge.fury.io/py/neural_diffeqs.svg)](https://badge.fury.io/py/neural_diffeqs)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A PyTorch-based library for the instantiation of neural differential equations.

### Installation

Install from [**PYPI**](https://pypi.org/project/neural-diffeqs/):
```python
pip install neural_diffeqs
```

Alternatively, install the development version from GitHub:
```BASH
git clone https://github.com/mvinyard/neural-diffeqs.git; cd ./neural-diffeqs
pip install -e .
```

## To-do and/or potential directions:
* Integration of neural controlled differential equations ([neural CDEs](https://github.com/patrick-kidger/torchcde)).
* Build SDE-GANs
* Neural PDEs

## References
The library builds upon the foundational research and developments in the field. We acknowledge and express our gratitude to the authors of the following key works that have shaped our understanding of neural differential equations and their applications:
Patrick Kidger, James Foster, Xuechen Li, Harald Oberhauser, Terry Lyons

[[1](https://arxiv.org/abs/2102.03657)] Kidger, P., Foster, J., Li, X., Oberhauser, H., Lyons, T., (**2021**). Neural SDEs as Infinite-Dimensional GANs. *ICML*.

[[2](https://arxiv.org/abs/1806.07366)] Chen, R. T. Q., Rubanova, Y., Bettencourt, J., & Duvenaud, D. K. (**2018**). Neural Ordinary Differential Equations. *Adv Neural Inf Process Sys*.

[[3](https://arxiv.org/abs/1904.01681)] Dupont, E., Doucet, A., & Teh, Y. W. (**2019**). Augmented Neural ODEs. *Adv Neural Inf Process Sys*.

[[4](https://arxiv.org/abs/2202.02435)] Kidger, P. (**2022**) On Neural Differential Equations. arXiv:2202.02435

---
**Questions or suggestions**? Open an [issue](https://github.com/mvinyard/neural-diffeqs/issues/new) or send an email to [Michael Vinyard](mailto:mvinyard.ai@gmail.com).
