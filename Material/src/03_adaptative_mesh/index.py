import os
import sys
import subprocess

figures_dir = '../../code/03_metodos_valoracion/figures'
os.makedirs(figures_dir, exist_ok=True)

scripts = [
    'fig1_trinomial_tree.py',
    'fig2_par_impar_convergence.py',
    'fig3_amm_concept.py',
    'fig4_amm_vanilla.py',
    'fig5_jagged_convergence.py',
    'fig6_amm_barrier.py',
    'fig7_quadrinomial_branching.py',
    'fig8_rmse_vs_time.py'
]

for i, script in enumerate(scripts, 1):
    print(f"[{i}/{len(scripts)}] Ejecutando {script}...")
    try:
        result = subprocess.run([sys.executable, f"03_adaptative_mesh/{script}"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(f"  Warns: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"  ERROR executing {script}:")
        print(f"  {e.stderr}")
        continue
    except FileNotFoundError:
        print(f"  ERROR: file {script} not found")
        continue
    print()
