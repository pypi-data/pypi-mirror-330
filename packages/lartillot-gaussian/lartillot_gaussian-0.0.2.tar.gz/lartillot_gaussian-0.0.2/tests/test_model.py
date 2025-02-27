from lartillot_gaussian import LartillotGaussianModel
import numpy as np
import matplotlib.pyplot as plt
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def test_lartillot_model():
    model = LartillotGaussianModel(d=1, v=1)

    x = model.simulate_posterior_samples(1000)
    x = np.sort(x, axis=0)
    lnp = model.log_posterior(x)
    lnp_2 = model.log_prior(x) + model.log_likelihood(x) - model.lnZ
    np.testing.assert_allclose(
        lnp,
        lnp_2,
        rtol=1e-6,
        err_msg="Log-likelihood + Log-prior - lnZ does not match Log-posterior!",
    )
    assert x.shape == (1000, 1), "Samples should have the right shape"
    plt.figure(figsize=(3, 2.5))
    plt.hist(x, bins=30, histtype="step", color="tab:blue", density=True)
    plt.plot(x, np.exp(lnp), color="tab:red")
    plt.xlabel("x")
    plt.savefig(f"{HERE}/posterior_samples.png")

def test_chains():
    d, nchains, nsamp = 4, 2, 100
    model = LartillotGaussianModel(d=d, v=1)
    chains = model.generate_chains(nsamp, nchains=nchains)
    assert chains.lnl.shape == (nchains, nsamp), "lnl should have the right shape"
    assert chains.samples.shape == (nchains, nsamp, d), "samples should have the right shape"

    lnl_chains = model.generate_lnl_chains(4, np.array([0.1,0.4,0.9]))

def test_version():
    from lartillot_gaussian._version import __version__

    assert isinstance(__version__, str)
