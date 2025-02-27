import numpy as np
from scipy.stats import norm
from dataclasses import dataclass
from typing import List


@dataclass
class Chains:
    lnl: np.ndarray
    samples: np.ndarray
    beta: np.ndarray


class LartillotGaussianModel:
    def __init__(self, d: int, v: float):
        self.d = d
        self.v = v

    @property
    def lnZ(self) -> float:
        v, d = self.v, self.d
        return np.log(np.power(2.0 * np.pi * (1.0 + v), -d / 2.0))

    def log_likelihood(self, theta: np.ndarray) -> float:
        v, d = self.v, self.d
        return -(d / 2) * np.log(2 * np.pi * v) - np.sum(
            theta ** 2, axis=1
        ) / (2 * v)

    def log_prior(self, theta: np.ndarray) -> float:
        return np.sum(norm.logpdf(theta, loc=0, scale=1), axis=1)

    def log_posterior(self, theta: np.ndarray) -> float:
        v, d = self.v, self.d
        sigma2 = v / (1 + v)  # Posterior variance
        return -(d / 2) * np.log(2 * np.pi * sigma2) - np.sum(
            theta ** 2, axis=1
        ) / (2 * sigma2)

    def simulate_posterior_samples(
            self, n: int, beta: float = 1.0
    ) -> np.ndarray:
        v, d = self.v, self.d
        mean = np.zeros(d)
        std = np.sqrt(v / (v + beta))
        return np.random.normal(loc=mean, scale=std, size=(n, d))

    def generate_lnl_chains(self, n: int, betas: np.ndarray) -> np.ndarray:
        lnl_chains = []
        for beta in betas:
            theta = self.simulate_posterior_samples(n, beta)
            lnl = self.log_likelihood(theta)
            lnl_chains.append(lnl)
        return np.array(lnl_chains)

    def generate_chains(self, n: int, betas: np.ndarray=None, nchains=None) -> Chains:
        if betas is None:
            betas = np.ones(nchains)

        samples, lnls = [], []
        for beta in betas:
            theta = self.simulate_posterior_samples(n, beta)
            lnl = self.log_likelihood(theta)
            samples.append(theta)
            lnls.append(lnl)
        return Chains(lnl=np.array(lnls), samples=np.array(samples), beta=betas)
