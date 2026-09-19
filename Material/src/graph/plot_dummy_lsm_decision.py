import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def plot_lsm_decision_tree():
    graph_dir = os.path.dirname(os.path.abspath(__file__))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Coordinates and dimensions
    box_w = 2.5
    box_h = 1.2
    
    y_top = 4
    y_mid = 2
    y_bot = 0
    
    x_steps = [1, 5, 9]
    t_labels = ['t = 1', 't = 2', 't = 3 (Vencimiento)']
    
    # Draw timelines
    ax.plot([0, 11], [y_mid, y_mid], color='lightgray', linestyle='--', linewidth=2, zorder=0)
    
    def draw_box(x, y, text, color='lightblue', edge='blue'):
        box = mpatches.FancyBboxPatch((x - box_w/2, y - box_h/2), box_w, box_h,
                                      boxstyle="round,pad=0.1",
                                      ec=edge, fc=color, zorder=3, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=11, fontweight='bold')
        
    def draw_arrow(x1, y1, x2, y2, text=None, text_offset=(0, 0.2)):
        ax.annotate("",
                    xy=(x2, y2), xycoords='data',
                    xytext=(x1, y1), textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5, shrinkA=5, shrinkB=5),
                    zorder=2)
        if text:
            ax.text((x1+x2)/2 + text_offset[0], (y1+y2)/2 + text_offset[1], text,
                    ha='center', va='center', fontsize=10, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))

    # Time 1
    draw_box(x_steps[0], y_mid, "Evaluar Trayectoria\nen t=1", color='#e6f2ff')
    draw_box(x_steps[0], y_top, "Ejercer\nValor = h(t=1)", color='#d4edda', edge='green')
    draw_box(x_steps[0], y_bot, "Continuar\nValor = C(t=1)", color='#fff3cd', edge='orange')
    
    draw_arrow(x_steps[0], y_mid + box_h/2, x_steps[0], y_top - box_h/2, "Si h > C")
    draw_arrow(x_steps[0], y_mid - box_h/2, x_steps[0], y_bot + box_h/2, "Si h <= C")
    
    # Time 2
    draw_arrow(x_steps[0] + box_w/2, y_bot, x_steps[1] - box_w/2, y_mid, "El tiempo\navanza")
    
    draw_box(x_steps[1], y_mid, "Evaluar Trayectoria\nen t=2", color='#e6f2ff')
    draw_box(x_steps[1], y_top, "Ejercer\nValor = h(t=2)", color='#d4edda', edge='green')
    draw_box(x_steps[1], y_bot, "Continuar\nValor = C(t=2)", color='#fff3cd', edge='orange')
    
    draw_arrow(x_steps[1], y_mid + box_h/2, x_steps[1], y_top - box_h/2, "Si h > C")
    draw_arrow(x_steps[1], y_mid - box_h/2, x_steps[1], y_bot + box_h/2, "Si h <= C")
    
    # Time 3
    draw_arrow(x_steps[1] + box_w/2, y_bot, x_steps[2] - box_w/2, y_mid, "El tiempo\navanza")
    
    draw_box(x_steps[2], y_mid, "Evaluar Trayectoria\nen t=3", color='#e6f2ff')
    draw_box(x_steps[2], y_top, "Ejercer\nValor = h(t=3)", color='#d4edda', edge='green')
    draw_box(x_steps[2], y_bot, "Expira sin valor\nValor = 0", color='#f8d7da', edge='red')
    
    draw_arrow(x_steps[2], y_mid + box_h/2, x_steps[2], y_top - box_h/2, "Si h > 0")
    draw_arrow(x_steps[2], y_mid - box_h/2, x_steps[2], y_bot + box_h/2, "Si h <= 0")
    
    # Annotations
    for x, label in zip(x_steps, t_labels):
        ax.text(x, y_bot - 1.5, label, ha='center', va='center', fontsize=13, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="#f1f1f1", ec="gray"))
        
    # Leyenda explicativa
    texto_leyenda = (
        "h(t) = Valor Intrínseco (Pago inmediato si ejerce)\n"
        "C(t) = Valor de Continuación (Esperanza del pago futuro descontado)\n"
        "Se calcula C(t) mediante regresión Longstaff-Schwartz"
    )
    ax.text(5.5, y_top + 1.2, texto_leyenda, ha='center', va='center', fontsize=11, 
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="black"))
    
    ax.set_xlim(-1, 12)
    ax.set_ylim(-2.5, 6)
    ax.axis('off')
    
    plt.title('Diagrama de Decisión: Método Longstaff-Schwartz', fontsize=16, y=1.05)
    plt.tight_layout()
    
    output_path = os.path.join(graph_dir, 'dummy_lsm_decision.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"Gráfico guardado en: {output_path}")

if __name__ == '__main__':
    plot_lsm_decision_tree()
