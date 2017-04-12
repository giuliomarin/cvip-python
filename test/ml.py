import numpy as np

# Fitting probability distributions

# Maximum likelihood learning of normal distribution
# Estimates mean and variance
def mlnormal(x):
    mu = np.mean(x)
    var = np.mean((x - mu) ** 2)
    return mu, var

# main
if __name__ == "__main__":
    x = np.asarray([-1., -1., -1., -0.3, -0.2, 0., 0.15, 0.3])
    print mlnormal(x)