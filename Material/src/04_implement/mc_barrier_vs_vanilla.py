import numpy as np
import sys
sys.path.insert(0, '..')

from mc.mc import monte_carlo_lsm_barrier

if __name__ == "__main__":
    S0 = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.25
    M = 50000
    N = 100
    
    print(f"\nParámetros: S0={S0}, K={K}, T={T}, r={r}, sigma={sigma}")
    print(f"Simulaciones: M={M}, Pasos: N={N}")
    
    print("\n" + "-" * 70)
    print("Caso 1: American Put Vanilla (simulada con H=0.01, down-out)")
    print("-" * 70)
    
    H_vanilla = 0.01  # Barrera imposible de tocar
    price_vanilla, std_vanilla = monte_carlo_lsm_barrier(
        S0, K, H_vanilla, T, r, sigma,
        delta=0,
        iterations=M,
        steps=N,
        isCall=False,  # Put
        isUp=False,    # Down
        isIn=False     # Out (knock-out con barrera muy baja = vanilla)
    )
    
    std_error_vanilla = std_vanilla / np.sqrt(M)
    ci_lower_vanilla = price_vanilla - 1.96 * std_error_vanilla
    ci_upper_vanilla = price_vanilla + 1.96 * std_error_vanilla
    
    print(f"Precio estimado: {price_vanilla:.4f}")
    print(f"Error estándar:  {std_error_vanilla:.4f}")
    print(f"IC 95%: [{ci_lower_vanilla:.4f}, {ci_upper_vanilla:.4f}]")
    
    print("\nCaso 2: American Down-and-Out Put con H=50 (lejana)")
    print("-" * 70)
    
    H_far = 50  # Barrera lejana pero no imposible
    price_far, std_far = monte_carlo_lsm_barrier(
        S0, K, H_far, T, r, sigma,
        delta=0,
        iterations=M,
        steps=N,
        isCall=False,  # Put
        isUp=False,    # Down
        isIn=False     # Out
    )
    
    std_error_far = std_far / np.sqrt(M)
    ci_lower_far = price_far - 1.96 * std_error_far
    ci_upper_far = price_far + 1.96 * std_error_far
    
    print(f"Precio estimado: {price_far:.4f}")
    print(f"Error estándar:  {std_error_far:.4f}")
    print(f"IC 95%: [{ci_lower_far:.4f}, {ci_upper_far:.4f}]")
    
    print("\n" + "-" * 70)
    print("Caso 3: American Down-and-Out Put con H=10 (muy lejana)")
    print("-" * 70)
    
    H_very_far = 10  # Barrera muy lejana
    price_very_far, std_very_far = monte_carlo_lsm_barrier(
        S0, K, H_very_far, T, r, sigma,
        delta=0,
        iterations=M,
        steps=N,
        isCall=False,  # Put
        isUp=False,    # Down
        isIn=False     # Out
    )
    
    std_error_very_far = std_very_far / np.sqrt(M)
    ci_lower_very_far = price_very_far - 1.96 * std_error_very_far
    ci_upper_very_far = price_very_far + 1.96 * std_error_very_far
    
    print(f"Precio estimado: {price_very_far:.4f}")
    print(f"Error estándar:  {std_error_very_far:.4f}")
    print(f"IC 95%: [{ci_lower_very_far:.4f}, {ci_upper_very_far:.4f}]")
    