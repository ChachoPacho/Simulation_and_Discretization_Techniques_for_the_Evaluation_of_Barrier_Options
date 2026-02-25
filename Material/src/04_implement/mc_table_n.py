import numpy as np
from mc.mc import monte_carlo_lsm_barrier

if __name__ == "__main__":
    print("\nCaso 1: American Down-and-Out Put")
    print("-" * 70)
    S0_1 = 100
    K_1 = 100
    H_1 = 80
    T_1 = 1
    r_1 = 0.05
    sigma_1 = 0.25
    M_1 = 50000
    N_1 = 100
    
    print(f"Parámetros: S0={S0_1}, K={K_1}, H={H_1}, T={T_1}, r={r_1}, sigma={sigma_1}")
    print(f"Simulaciones: M={M_1}, Pasos: N={N_1}")
    
    price_1, std_1 = monte_carlo_lsm_barrier(
        S0_1, K_1, H_1, T_1, r_1, sigma_1,
        delta=0,
        iterations=M_1,
        steps=N_1,
        isCall=False,  # Put
        isUp=False,    # Down
        isIn=False     # Out
    )
    
    std_error_1 = std_1 / np.sqrt(M_1)
    ci_lower_1 = price_1 - 1.96 * std_error_1
    ci_upper_1 = price_1 + 1.96 * std_error_1
    
    print(f"\nResultados:")
    print(f"  Precio estimado: {price_1:.4f}")
    print(f"  Error estándar:  {std_error_1:.4f}")
    print(f"  IC 95%: [{ci_lower_1:.4f}, {ci_upper_1:.4f}]")
    print(f"  Ancho del IC: {ci_upper_1 - ci_lower_1:.4f}")
    
    print("\nCaso 2: American Up-and-In Call")
    print("-" * 70)
    
    S0_2 = 100
    K_2 = 100
    H_2 = 120
    T_2 = 1
    r_2 = 0.05
    sigma_2 = 0.30
    M_2 = 50000
    N_2 = 100
    
    print(f"Parámetros: S0={S0_2}, K={K_2}, H={H_2}, T={T_2}, r={r_2}, sigma={sigma_2}")
    print(f"Simulaciones: M={M_2}, Pasos: N={N_2}")
    
    price_2, std_2 = monte_carlo_lsm_barrier(
        S0_2, K_2, H_2, T_2, r_2, sigma_2,
        delta=0,
        iterations=M_2,
        steps=N_2,
        isCall=True,   # Call
        isUp=True,     # Up
        isIn=True      # In
    )
    
    std_error_2 = std_2 / np.sqrt(M_2)
    ci_lower_2 = price_2 - 1.96 * std_error_2
    ci_upper_2 = price_2 + 1.96 * std_error_2
    
    print(f"\nResultados:")
    print(f"  Precio estimado: {price_2:.4f}")
    print(f"  Error estándar:  {std_error_2:.4f}")
    print(f"  IC 95%: [{ci_lower_2:.4f}, {ci_upper_2:.4f}]")
    print(f"  Ancho del IC: {ci_upper_2 - ci_lower_2:.4f}")
