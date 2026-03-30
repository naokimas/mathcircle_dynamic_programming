import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import matplotlib.patheffects as pe
import random

def draw_mouse(ax, x, y, s=0.35):
    body = Ellipse((x, y), width=1.2*s, height=0.75*s,
                   facecolor="#cfcfcf", edgecolor="black", lw=1, zorder=3)
    head = Circle((x + 0.55*s, y + 0.10*s), radius=0.28*s,
                  facecolor="#cfcfcf", edgecolor="black", lw=1, zorder=3)
    ear1 = Circle((x + 0.68*s, y + 0.32*s), radius=0.14*s,
                  facecolor="#d9d9d9", edgecolor="black", lw=1, zorder=3)
    ear2 = Circle((x + 0.50*s, y + 0.35*s), radius=0.14*s,
                  facecolor="#d9d9d9", edgecolor="black", lw=1, zorder=3)
    eye = Circle((x + 0.64*s, y + 0.13*s), radius=0.03*s,
                 facecolor="black", edgecolor="black", zorder=4)
    nose = Circle((x + 0.82*s, y + 0.06*s), radius=0.03*s,
                  facecolor="black", edgecolor="black", zorder=4)

    for p in (body, head, ear1, ear2, eye, nose):
        ax.add_patch(p)

    t = np.linspace(0, 1, 60)
    tail_x = x - 0.65*s - 0.55*s*t
    tail_y = y + 0.10*s*np.sin(2*np.pi*t)
    ax.plot(tail_x, tail_y, color="black", lw=1, zorder=2)


def edge_label_aligned(ax, x0, y0, x1, y1, text, x_label, dy=0.15, fontsize=9):
    if x1 == x0:
        t = 0.5
    else:
        t = (x_label - x0) / (x1 - x0)
    t = float(np.clip(t, 0.05, 0.95))

    y_on_edge = y0 + t * (y1 - y0)
    sign = 1.0 if (y1 - y0) >= 0 else -1.0
    y_text = y_on_edge + sign * dy

    txt = ax.text(x_label, y_text, str(text),
                  ha="center", va="center", fontsize=fontsize,
                  color="black", zorder=5)

    txt.set_path_effects([pe.withStroke(linewidth=2, foreground="white")])
    return txt


def make_dp_maze_5_stages(save_path="dp_maze_tree_5stages.pdf", show=True, include_mouse=True):
    depth = 5
    x_gap = 2.5
    
    # Generate random rewards for each stage {1, 2, 3, 4}
    # stage d has 2^(d+1) edges
    stage_rewards = []
    for d in range(depth):
        stage_rewards.append([random.randint(1, 4) for _ in range(2**(d+1))])

    # 32 leaf labels (0-31)
    leaf_labels = [str(i) for i in range(2**depth)]

    # Dynamic positioning
    ys_leaf = np.linspace(8.0, -8.0, 2**depth)
    pos = {}
    
    # Leaves
    for i in range(2**depth):
        pos[(depth, i)] = (depth * x_gap, float(ys_leaf[i]))
        
    # Back-calculate internal nodes
    for d in range(depth - 1, -1, -1):
        for i in range(2**d):
            y = (pos[(d + 1, 2*i)][1] + pos[(d + 1, 2*i + 1)][1]) / 2
            pos[(d, i)] = (d * x_gap, y)

    fig, ax = plt.subplots(figsize=(14, 8))

    # Fine-tuned label positioning for high density
    LABEL_ALPHA = [0.55] * depth 
    LABEL_DY = [0.3, 0.25, 0.2, 0.15, 0.12]

    stage_x = []
    for d in range(depth):
        x0 = d * x_gap
        x1 = (d + 1) * x_gap
        stage_x.append(x0 + LABEL_ALPHA[d] * (x1 - x0))

    # Draw Edges and Labels
    for d in range(depth):
        for parent in range(2**d):
            for child_idx in [0, 1]:
                child = 2 * parent + child_idx
                x0, y0 = pos[(d, parent)]
                x1, y1 = pos[(d + 1, child)]
                
                # Plot edge
                ax.plot([x0, x1], [y0, y1], color="black", lw=1.2, alpha=0.7, zorder=1)
                
                # Plot label
                reward = stage_rewards[d][2 * parent + child_idx]
                edge_label_aligned(ax, x0, y0, x1, y1, reward, 
                                   x_label=stage_x[d], dy=LABEL_DY[d])

    # Nodes (excluding root)
    for (d, i), (x, y) in pos.items():
        if d == 0: continue
        radius = 0.05 if d < 5 else 0.03
        ax.add_patch(Circle((x, y), radius=radius,
                            facecolor="white", edgecolor="black",
                            lw=1, zorder=2))

    # Mouse
    x_root, y_root = pos[(0, 0)]
    if include_mouse:
        s = 0.7
        draw_mouse(ax, x_root - 0.8, y_root, s=s)
    else:
        ax.add_patch(Circle((x_root, y_root), radius=0.1, facecolor="white", edgecolor="black", lw=2))

    # Terminal Labels
    for i in range(2**depth):
        x, y = pos[(depth, i)]
        ax.text(x + 0.2, y, leaf_labels[i], ha="left", va="center",
                fontsize=8, fontweight="bold", zorder=5)

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-2, depth * x_gap + 2)
    ax.set_ylim(min(ys_leaf) - 1, max(ys_leaf) + 1)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

if __name__ == "__main__":
    make_dp_maze_5_stages(show=True)
