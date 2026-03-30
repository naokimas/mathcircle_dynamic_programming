import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse

def draw_mouse(ax, x, y, s=0.35):
    body = Ellipse((x, y), width=1.2*s, height=0.75*s,
                   facecolor="#cfcfcf", edgecolor="black", lw=1, zorder=10)
    head = Circle((x + 0.55*s, y + 0.10*s), radius=0.28*s,
                  facecolor="#cfcfcf", edgecolor="black", lw=1, zorder=10)
    ear1 = Circle((x + 0.68*s, y + 0.32*s), radius=0.14*s,
                  facecolor="#d9d9d9", edgecolor="black", lw=1, zorder=10)
    ear2 = Circle((x + 0.50*s, y + 0.35*s), radius=0.14*s,
                  facecolor="#d9d9d9", edgecolor="black", lw=1, zorder=10)
    eye = Circle((x + 0.64*s, y + 0.13*s), radius=0.03*s,
                 facecolor="black", edgecolor="black", zorder=11)
    nose = Circle((x + 0.82*s, y + 0.06*s), radius=0.03*s,
                  facecolor="black", edgecolor="black", zorder=11)

    for p in (body, head, ear1, ear2, eye, nose):
        ax.add_patch(p)

    t = np.linspace(0, 1, 60)
    tail_x = x - 0.65*s - 0.55*s*t
    tail_y = y + 0.10*s*np.sin(2*np.pi*t)
    ax.plot(tail_x, tail_y, color="black", lw=1, zorder=9)

def make_asymmetric_tree(save_path="dp_maze_tree_incomplete.pdf", show=True):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define Nodes: (x, y, reward)
    # Layer 0
    nodes = {
        "root": (0, 0, 5)
    }
    # Layer 1
    nodes.update({
        "n4": (2, 2, 4),
        "n8": (2, -2, 8)
    })
    # Layer 2
    nodes.update({
        "n11": (4, 3, 11),
        "n2":  (4, 1, 2),
        "n13": (4, -1, 13),
        "n4_2": (4, -3, 4)
    })
    # Layer 3 (Terminals)
    nodes.update({
        "n7": (6, 3.5, 7),
        "n1_1": (6, 2.5, 1),
        "n1_2": (6, -2.5, 1),
        "n3": (6, -3.5, 3)
    })

    # Define Edges (parent_key, child_key)
    edges = [
        ("root", "n4"), ("root", "n8"),
        ("n4", "n11"), ("n4", "n2"),
        ("n8", "n13"), ("n8", "n4_2"),
        ("n11", "n7"), ("n11", "n1_1"),
        ("n4_2", "n1_2"), ("n4_2", "n3")
    ]

    # Draw Edges
    for p_key, c_key in edges:
        x0, y0, _ = nodes[p_key]
        x1, y1, _ = nodes[c_key]
        ax.plot([x0, x1], [y0, y1], color="black", lw=1.5, zorder=1)

    # Draw Nodes
    node_radius = 0.35
    for key, (x, y, val) in nodes.items():
        circle = Circle((x, y), radius=node_radius, facecolor="white", 
                        edgecolor="black", lw=1.5, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, f"${val}$", ha="center", va="center", 
                fontsize=16, zorder=3)

    # Label Start
    ax.text(0, 0.6, "START", ha="center", va="bottom", fontsize=10, fontweight="bold")

    # Draw Mouse
    draw_mouse(ax, -1.2, 0, s=0.7)

    # Add labels A-F to the right of specific nodes
    label_map = {
        "n7": "A", "n1_1": "B", "n2": "C", 
        "n13": "D", "n1_2": "E", "n3": "F"
    }
    for key, label in label_map.items():
        x, y, _ = nodes[key]
        ax.text(x + 0.5, y, label, ha="left", va="center", 
                fontsize=18)

    # Formatting
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-2, 7.5)
    ax.set_ylim(-4.5, 4.5)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

if __name__ == "__main__":
    make_asymmetric_tree()
