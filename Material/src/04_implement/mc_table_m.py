import numpy as np
from mc.mc import monte_carlo_lsm_barrier

if __name__ == "__main__":
  S0 = 44
  K = 40
  T = 1
  r = 0.06
  sigma = 0.2
  H = 39.6

  np.random.seed(42)
  
  N = 50
  M_values = [1000, 5000, 10000, 50000, 100000]
  prices = []
  std_errors = []
  for M in M_values:
    price, std = monte_carlo_lsm_barrier(S0, K, H, T, r, sigma, isCall=False, delta=0, iterations=M, steps=N)
    prices.append(price)
    std_errors.append(std / np.sqrt(M))
    
  print("M\tStd Error")
  for i, M in enumerate(M_values):
    print(f"{M}\t{std_errors[i]:.6f}")
