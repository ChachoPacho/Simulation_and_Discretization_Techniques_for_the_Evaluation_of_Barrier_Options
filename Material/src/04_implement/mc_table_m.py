import numpy as np
import time
from mc.mc import monte_carlo_lsm_barrier

if __name__ == "__main__":
  S0 = 44
  K = 40
  T = 1
  r = 0.06
  sigma = 0.2
  H = 39.6

  np.random.seed(42)
  
  N = 252
  M_values = [1000, 5000, 10000, 50000, 100000]
  prices = []
  std_errors = []
  times = []
  for M in M_values:
    start = time.perf_counter()                                                                                         
    price, std = monte_carlo_lsm_barrier(S0, K, H, T, r, sigma, isCall=False, isUp=False, isIn=False, delta=0, iterations=M, steps=N)
    end = time.perf_counter()
    prices.append(price)
    std_errors.append(std / np.sqrt(M))
    times.append(end-start)
    
  print("M\tStd Error")
  for i, M in enumerate(M_values):
    print(f"{M}\t{std_errors[i]:.6f}\t{times[i]:.6f}")
