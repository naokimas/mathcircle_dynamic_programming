import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, FancyArrowPatch

def draw_realistic_frog(ax, x, y, s=0.5):
    """Draws a frog with a more natural anatomy and legs, facing right."""
    c_body = "#4CAF50"
    c_belly = "#8BC34A"
    
    # Back Leg
    back_thigh = Ellipse((x - 0.2*s, y - 0.1*s), width=0.7*s, height=0.4*s, 
                         angle=40, facecolor=c_body, edgecolor="black", lw=1, zorder=9)
    back_foot = Ellipse((x - 0.35*s, y - 0.3*s), width=0.4*s, height=0.15*s, 
                        angle=-10, facecolor=c_body, edgecolor="black", lw=1, zorder=8)
    
    # Front Leg
    front_leg = Ellipse((x + 0.3*s, y - 0.25*s), width=0.15*s, height=0.4*s, 
                        angle=-10, facecolor=c_body, edgecolor="black", lw=1, zorder=11)
    
    # Body
    body = Ellipse((x, y), width=1.3*s, height=0.8*s, 
                   facecolor=c_body, edgecolor="black", lw=1.2, zorder=10)
    belly = Ellipse((x + 0.1*s, y - 0.15*s), width=0.8*s, height=0.4*s, 
                    facecolor=c_belly, edgecolor="none", zorder=10.5)
    
    # Eyes
    eye_mound = Circle((x + 0.35*s, y + 0.3*s), radius=0.2*s, 
                       facecolor=c_body, edgecolor="black", lw=1, zorder=11)
    eye_white = Circle((x + 0.4*s, y + 0.32*s), radius=0.12*s, 
                       facecolor="white", edgecolor="black", lw=0.5, zorder=12)
    pupil = Circle((x + 0.45*s, y + 0.32*s), radius=0.06*s, facecolor="black", zorder=13)
    
    for p in (back_thigh, back_foot, front_leg, body, belly, eye_mound, eye_white, pupil):
        ax.add_patch(p)

def make_frog_stone_low_arch(save_path="frog_stones_1.pdf", show=True):
    fig, ax = plt.subplots(figsize=(10, 4))
    
    rewards = [0, -1, 2, 3]
    num_stones = len(rewards)
    # 40% smaller than original 1.8x1.0
    w, h = 1.08, 0.6
    x_coords = np.arange(num_stones) * 2.5
    y_stone = 0
    
    # 1. Draw Stones and Labels
    for i, (x, r) in enumerate(zip(x_coords, rewards)):
        stone = Ellipse((x, y_stone), width=w, height=h, 
                        facecolor="#d3d3d3", edgecolor="black", lw=1.2, zorder=2)
        ax.add_patch(stone)
        
        # Reward Value (Normal weight)
        ax.text(x, y_stone, f"${r}$", ha="center", va="center", 
                fontsize=20, fontweight="normal", zorder=3)
        
        # Stone Label (Lifted closer to oval)
        ax.text(x, y_stone - 0.45, f"stone {i}", ha="center", va="top", 
                fontsize=14, fontweight="normal")

    # 2. Draw Low-Arch Arrows (Height reduced by half)
    for i in range(num_stones):
        if i + 1 < num_stones:
            # Short Jump: rad changed from -0.5 to -0.25
            start = (x_coords[i] + 0.2, 0.25)
            end = (x_coords[i+1] - 0.2, 0.25)
            arrow = FancyArrowPatch(start, end, connectionstyle="arc3,rad=-0.25", 
                                     arrowstyle='->,head_width=3,head_length=6',
                                     lw=1.2, color="black", zorder=5)
            ax.add_patch(arrow)
            
        if i + 2 < num_stones:
            # Skip Jump: rad changed from -0.6 to -0.3
            start = (x_coords[i] + 0.1, 0.35)
            end = (x_coords[i+2] - 0.1, 0.35)
            arrow_skip = FancyArrowPatch(start, end, connectionstyle="arc3,rad=-0.3", 
                                         arrowstyle='->,head_width=3,head_length=6',
                                         lw=1.2, color="black", zorder=4)
            ax.add_patch(arrow_skip)

    # 3. Draw Realistic Frog
    draw_realistic_frog(ax, x_coords[0] - 1.8, y_stone, s=0.7)

    # Formatting
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(x_coords[0] - 3.0, x_coords[-1] + 1.5)
    ax.set_ylim(-1.5, 2.5)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

if __name__ == "__main__":
    make_frog_stone_low_arch()
