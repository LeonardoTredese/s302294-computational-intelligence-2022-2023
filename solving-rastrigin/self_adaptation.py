import logging
from problems import sphere, rastrigin 
import numpy as np

SEED = 42

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

class SelfAdaptive:
    def __init__(self, initial_point: np.ndarray, sigma: np.ndarray, seed=None, step = 1):
        self.generator = np.random.default_rng(seed)
        self.v = initial_point
        self.shape = initial_point.shape
        self.sigma = sigma
        self.step = step        

    def tweak(self):
        tau = 1 / (self.step ** .5)
        seed = self.generator.integers(2 ** 10)
        sigma = self.sigma * np.exp(tau * self.generator.normal(size = self.shape))
        value = self.generator.normal(loc=self.v, scale=self.sigma)
        return SelfAdaptive(value, sigma, seed=seed, step=self.step+1)
        
    @property
    def parameters(self) -> np.ndarray:
        return self.v


def one_lambda(x0, sigma0, lambda_, fitness, epochs, seed=None, strategy=','):
    one = SelfAdaptive(x0, sigma0, seed=seed)
    best = one
    population, hist = list(), list()
    for epoch in range(epochs):
        for _ in range(lambda_):
            new = one.tweak()
            population.append((fitness(new.parameters), new))
        if strategy in ['plus', '+']:
            one.step += 1
            population.append((fitness(one.parameters), one))
        fit, one = max(population)
        if fit > fitness(best.parameters):
            hist.append((one, epoch))
            best = one
        population.clear()
    return best, hist
            

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x0 = np.full(2, 100)
    sigma0 = np.full(2, 10)
    goal = np.zeros((1,2))
    best, hist = one_lambda(x0, sigma0, 1000, rastrigin, 10 ** 3, seed=SEED, strategy='+')
    print(np.linalg.norm(best.parameters - goal), rastrigin(best.parameters))
    values, epochs = zip(*hist) 
    pos = np.array(list(map(lambda x: x.parameters, values)))
    errors = np.linalg.norm(pos - goal, axis = 1)
    minus_rast = -rastrigin(pos.T)

    plt.semilogy(epochs, errors, 'b', marker='.', label='distance of x from solution')
    plt.semilogy(epochs, minus_rast, 'r', marker='*', label='- rastrigin(x)')
    plt.title('Fittest elements')
    plt.xlabel('epoch')
    plt.legend()
    plt.show()
    
