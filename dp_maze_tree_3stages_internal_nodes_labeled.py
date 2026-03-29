# dp_maze_tree_3stages_labeled.py
# Binary “maze-like” branching figure with edge rewards,
# labeled leaves A–H and internal nodes I–O.

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
    if x1 == x0:
        t = 0.5
    else:
        t = (x_label - x0) / (x1 - x0)
    t = float(np.clip(t, 0.05, 0.95))

    y_on_edge = y0 + t * (y1 - y0)
    sign = 1.0 if (y1 - y0) >= 0 else -1.0
    y_text = y_on_edge + sign * dy

    txt = ax.text(x_label, y_text, str(text),
                  ha="center", va="center",
                  fontsize=fontsize, color="black", zorder=5)
    txt.set_path_effects([pe.withStroke(linewidth=3, foreground="white")])
    return txt


def make_dp_maze(save_path="dp_maze_tree_3stages_internal_nodes_labeled_type0.pdf",
                 show=True, include_mouse=True):

    # Rewards
    r1 = [1, 2]
    r2 = [1, 2, 3, 4]
    r3 = [2, 1, 4, 3, 2, 1, 4, 3]

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

    LABEL_ALPHA = [0.62, 0.62, 0.70]
    LABEL_DY    = [0.34, 0.28, 0.22]

    stage_x = []
    for d in range(depth):
        x0 = d * x_gap
        x1 = (d + 1) * x_gap
        stage_x.append(x0 + LABEL_ALPHA[d] * (x1 - x0))

    # Draw edges and edge rewards
    for child in [0, 1]:
        x0, y0 = pos[(0, 0)]
        x1, y1 = pos[(1, child)]
        ax.plot([x0, x1], [y0, y1], color="black", lw=2)
        edge_label_aligned(ax, x0, y0, x1, y1,
                           r1[child], stage_x[0], dy=LABEL_DY[0])

    for parent in [0, 1]:
        for j in [0, 1]:
            child = 2 * parent + j
            x0, y0 = pos[(1, parent)]
            x1, y1 = pos[(2, child)]
            ax.plot([x0, x1], [y0, y1], color="black", lw=2)
            edge_label_aligned(ax, x0, y0, x1, y1,
                               r2[2 * parent + j],
                               stage_x[1], dy=LABEL_DY[1])

    for parent in range(4):
        for j in [0, 1]:
            leaf = 2 * parent + j
            x0, y0 = pos[(2, parent)]
            x1, y1 = pos[(3, leaf)]
            ax.plot([x0, x1], [y0, y1], color="black", lw=2)
            edge_label_aligned(ax, x0, y0, x1, y1,
                               r3[leaf],
                               stage_x[2], dy=LABEL_DY[2])

    # Draw node dots (excluding root)
    for (d, i), (x, y) in pos.items():
        if d == 0:
            continue
        ax.add_patch(Circle((x, y), radius=0.06,
                            facecolor="white",
                            edgecolor="black",
                            lw=1.5, zorder=2))

    # Mouse
    x_root, y_root = pos[(0, 0)]
    if include_mouse:
        s = 0.9
        clearance = 0.55
        rightmost_mouse = 0.85 * s
        mouse_x = x_root - (rightmost_mouse + clearance)
        draw_mouse(ax, mouse_x, y_root, s=s)

    # Leaf labels A–H
    for i, lab in enumerate(leaf_labels):
        x, y = pos[(3, i)]
        ax.text(x + 0.25, y, lab,
                ha="left", va="center",
                fontsize=13, fontweight="bold", zorder=6)

    # Internal node labels with offsets
    internal_labels = {
        (2, 0): "I",
        (2, 1): "J",
        (2, 2): "K",
        (2, 3): "L",
        (1, 0): "M",
        (1, 1): "N",
        (0, 0): "O",
    }

    dy_small = 0.18    # ~ one quarter of label height
    dx_root  = 0.18
    dy_root  = 0.35

    for (d, i), lab in internal_labels.items():
        x, y = pos[(d, i)]
        dx, dy = 0.0, 0.0

        if lab in ("I", "K"):
            dy = dy_small
        if lab in ("J", "L"):
            dy = -dy_small
        if lab == "O":
            dx = dx_root
            dy = dy_root

        ax.text(x - 0.25 + dx, y + dy, lab,
                ha="right", va="center",
                fontsize=13, fontweight="bold", zorder=7)

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
    make_dp_maze(show=True, include_mouse=True)
