# Lartillot Gaussian model

![PyPI](https://img.shields.io/pypi/v/lartillot_gaussian)


The multidimensional Gaussian model from [Lartillot et al '06] is useful for testing Bayesian applications.

The model is parameterised by a vector $\theta = (\theta_1, \theta_2, \ldots, \theta_d)$ of dimension $d$. 
The prior on $\theta$ is a product of independent normals with a null mean and unit variance. 
The likelihood function is given by 
$$\mathcal{L}(\theta, v) =  {(2\pi v)^{-d/2}} \prod_{i = 1}^d \text{exp}\bigg[\frac{-\theta_i^2}{2v}\bigg],$$
where $v$ is the common variance for all $d$ dimensions. 

The joint posterior is given by $d$ products of $\mathcal{N}(0, v/(1+v))$. Finally, the evidence is given by
$$    \mathcal{Z} = (2\pi v)^{-d/2} \left(\frac{v}{1 + v} \right)^{d/2}=\left(2\pi(1+v)\right)^{-d/2}\ . $$


[Lartillot et al '06]: https://academic.oup.com/sysbio/article-abstract/55/2/195/1620800?redirectedFrom=fulltext


This codebase provides a simple implementation of the Lartillot Gaussian model in Python.

```bash
pip install lartillot_gaussian
```


```python

from lartillot_gaussian import LartillotGaussianModel
import numpy as np

model = LartillotGaussianModel(d=10, v=1.0)
theta = np.array([[0]])
print(model.lnz)

```