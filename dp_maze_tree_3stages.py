# dp_maze_tree_3stages.py
# Binary “maze-like” branching figure with edge rewards and A–H terminals.


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import matplotlib.patheffects as pe


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


def edge_label_aligned(ax, x0, y0, x1, y1, text, x_label, dy=0.25, fontsize=12):
    """
    Place reward text at a fixed x (shared across a stage), and slightly above/below the edge.
    This keeps all labels in a stage horizontally aligned and avoids sitting on the line.
    """
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

    # White outline for readability WITHOUT a filled box that occludes edges
    txt.set_path_effects([pe.withStroke(linewidth=3, foreground="white")])
    return txt


def make_dp_maze(save_path="dp_maze.png", show=True, include_mouse=True):
    # Rewards (as specified)
    type = 1
    if type==0:
        r1 = [1, 2]
        r2 = [1, 2, 3, 4]
        r3 = [2, 1, 4, 3, 2, 1, 4, 3]
    elif type==1:
        r1 = [1, 2]
        r2 = [3, 1, 2, 3]
        r3 = [4, 1, 4, 2, 3, 2, 2, 1]

    leaf_labels = list("ABCDEFGH")

    depth = 3
    x_gap = 2.2

    ys_leaf = np.linspace(3.5, -3.5, 2**depth)

    # Node positions
    pos = {}
    for i in range(2**depth):
        pos[(depth, i)] = (depth * x_gap, float(ys_leaf[i]))
    for d in range(depth - 1, -1, -1):
        for i in range(2**d):
            y = (pos[(d + 1, 2*i)][1] + pos[(d + 1, 2*i + 1)][1]) / 2
            pos[(d, i)] = (d * x_gap, y)

    fig, ax = plt.subplots(figsize=(12, 5))

    # Per-stage label x positions (constant within each stage => horizontal alignment)
    # stage 0: depth0->1, stage 1: depth1->2, stage 2: depth2->3
    LABEL_ALPHA = [0.62, 0.62, 0.70]   # fraction across each edge (same for all edges in that stage)
    LABEL_DY    = [0.34, 0.28, 0.22]   # vertical offset off the edge (up edges go up; down edges go down)

    stage_x = []
    for d in range(depth):
        x0 = d * x_gap
        x1 = (d + 1) * x_gap
        stage_x.append(x0 + LABEL_ALPHA[d] * (x1 - x0))

    # Draw edges + labels
    # depth 0 -> 1
    for child in [0, 1]:
        x0, y0 = pos[(0, 0)]
        x1, y1 = pos[(1, child)]
        ax.plot([x0, x1], [y0, y1], color="black", lw=2, zorder=1)
        edge_label_aligned(ax, x0, y0, x1, y1, r1[child], x_label=stage_x[0], dy=LABEL_DY[0])

    # depth 1 -> 2
    for parent in [0, 1]:
        for j in [0, 1]:
            child = 2 * parent + j
            x0, y0 = pos[(1, parent)]
            x1, y1 = pos[(2, child)]
            ax.plot([x0, x1], [y0, y1], color="black", lw=2, zorder=1)
            edge_label_aligned(ax, x0, y0, x1, y1, r2[2 * parent + j], x_label=stage_x[1], dy=LABEL_DY[1])

    # depth 2 -> 3
    for parent in range(4):
        for j in [0, 1]:
            leaf = 2 * parent + j
            x0, y0 = pos[(2, parent)]
            x1, y1 = pos[(3, leaf)]
            ax.plot([x0, x1], [y0, y1], color="black", lw=2, zorder=1)
            edge_label_aligned(ax, x0, y0, x1, y1, r3[leaf], x_label=stage_x[2], dy=LABEL_DY[2])

    # Nodes (small dots), excluding root
    for (d, i), (x, y) in pos.items():
        if d == 0:
            continue
        ax.add_patch(Circle((x, y), radius=0.06,
                            facecolor="white", edgecolor="black",
                            lw=1.5, zorder=2))

    # Mouse: moved further left so it does not overlap the tree
    x_root, y_root = pos[(0, 0)]
    if include_mouse:
        s = 0.9
        clearance = 0.55  # increase this if you want even more separation
        rightmost_mouse = 0.85 * s      # approx rightmost extent relative to mouse center
        mouse_x = x_root - (rightmost_mouse + clearance)
        draw_mouse(ax, mouse_x, y_root, s=s)
    else:
        ax.add_patch(Circle((x_root, y_root), radius=0.10,
                            facecolor="white", edgecolor="black",
                            lw=2, zorder=3))

    # Terminal labels A–H
    for i, lab in enumerate(leaf_labels):
        x, y = pos[(3, i)]
        ax.text(x + 0.25, y, lab, ha="left", va="center",
                fontsize=13, fontweight="bold", zorder=5)

    # Styling (no title)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-3.2, depth * x_gap + 2.0)
    ax.set_ylim(min(ys_leaf) - 1.0, max(ys_leaf) + 1.0)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    make_dp_maze(save_path="dp_maze_tree_3stages.pdf", show=True, include_mouse=True)