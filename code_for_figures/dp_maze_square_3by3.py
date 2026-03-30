import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse

def draw_mouse(ax, x, y, s=0.35):
    """Refined mouse drawing based on your provided style."""
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

def make_grid_maze(save_path="grid_maze.pdf", show=True):
    # Rewards matrix: [5, 2, 1; 4, 0, 8; 1, 2, 6]
    # In matplotlib, row 0 is usually at the bottom, so we reverse for visual top-down match
    rewards = np.array([[5, 2, 1],
                        [4, 0, 8],
                        [1, 2, 6]])
    
    rows, cols = rewards.shape
    fig, ax = plt.subplots(figsize=(6, 6))

    # Grid settings
    spacing = 2.0
    node_radius = 0.45

    # 1. Draw Edges first (so they sit behind nodes)
    for r in range(rows):
        for c in range(cols):
            x, y = c * spacing, (rows - 1 - r) * spacing
            # Horizontal edge
            if c < cols - 1:
                ax.plot([x, x + spacing], [y, y], color="black", lw=1.5, zorder=1)
            # Vertical edge
            if r < rows - 1:
                ax.plot([x, x], [y, y - spacing], color="black", lw=1.5, zorder=1)

    # 2. Draw Nodes and Rewards
    for r in range(rows):
        for c in range(cols):
            x, y = c * spacing, (rows - 1 - r) * spacing
            
            # Draw node circle
            circle = Circle((x, y), radius=node_radius, facecolor="white", 
                            edgecolor="black", lw=1.5, zorder=2)
            ax.add_patch(circle)
            
            # Draw reward value inside
            ax.text(x, y, str(rewards[r, c]), ha="center", va="center", 
                    fontsize=20, zorder=3)

    # 3. Add 'Start' and 'Goal' labels
    # Start: Top-left (0, 2*spacing)
    ax.text(0, (rows-1)*spacing + 0.8, "START", ha="center", va="bottom", 
            fontsize=14, fontweight="bold")
    
    # Goal: Bottom-right (2*spacing, 0)
    ax.text((cols-1)*spacing, -0.8, "GOAL", ha="center", va="top", 
            fontsize=14, fontweight="bold")

    # 4. Draw Mouse near Start
    # Positioned to the left of the start node to avoid overlap
    mouse_x = -1.2
    mouse_y = (rows - 1) * spacing
    draw_mouse(ax, mouse_x, mouse_y, s=0.7)

    # Final Styling
    ax.set_aspect("equal")
    ax.axis("off")
    
    # Padding the limits to fit labels and mouse
    ax.set_xlim(-2.5, (cols-1)*spacing + 1.5)
    ax.set_ylim(-1.5, (rows-1)*spacing + 1.5)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

if __name__ == "__main__":
    make_grid_maze(save_path="dp_maze_square_3by3.pdf")
