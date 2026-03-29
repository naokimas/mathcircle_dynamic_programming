import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, FancyArrowPatch

def draw_realistic_frog(ax, x, y, s=0.5):
    """Draws a frog with a natural anatomy and legs, facing right."""
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

def make_7_stone_final(save_path="frog_stones_2.pdf", show=True):
    # Rewards for stones 0 through 6
    rewards = [0, 3, -1, 2, -3, 3, 1]
    num_stones = len(rewards)
    
    # Stone dimensions
    w, h = 1.08, 0.6
    # Compact spacing (reduced from 2.4 to 1.92)
    x_gap = 1.92
    x_coords = np.arange(num_stones) * x_gap
    y_stone = 0
    
    fig, ax = plt.subplots(figsize=(12, 4)) 
    
    # 1. Draw Stones and Labels
    for i, (x, r) in enumerate(zip(x_coords, rewards)):
        # Stone Oval
        stone = Ellipse((x, y_stone), width=w, height=h, 
                        facecolor="#d3d3d3", edgecolor="black", lw=1.2, zorder=2)
        ax.add_patch(stone)
        
        # Reward Value (Normal weight)
        ax.text(x, y_stone, f"${r}$", ha="center", va="center", 
                fontsize=20, fontweight="normal", zorder=3)
        
        # Stone Label (Lifted closer to oval)
        ax.text(x, y_stone - 0.45, f"stone {i}", ha="center", va="top", 
                fontsize=14, fontweight="normal")

    # 2. Draw Arched Arrows (Adjacent and Skip 1 only)
    for i in range(num_stones):
        # Adjacent Jump (+1)
        if i + 1 < num_stones:
            start = (x_coords[i] + 0.15, 0.25)
            end = (x_coords[i+1] - 0.15, 0.25)
            # Low-arch curvature
            ax.add_patch(FancyArrowPatch(start, end, connectionstyle="arc3,rad=-0.25", 
                                          arrowstyle='->,head_width=3,head_length=6',
                                          lw=1.0, color="black", zorder=5))
            
        # Skip 1 Stone (+2)
        if i + 2 < num_stones:
            start = (x_coords[i] + 0.1, 0.35)
            end = (x_coords[i+2] - 0.1, 0.35)
            # Slightly higher arch to distinguish from adjacent jump
            ax.add_patch(FancyArrowPatch(start, end, connectionstyle="arc3,rad=-0.35", 
                                          arrowstyle='->,head_width=3,head_length=6',
                                          lw=1.0, color="black", zorder=4))

    # 3. Draw Realistic Frog
    draw_realistic_frog(ax, x_coords[0] - 1.5, y_stone, s=0.7)

    # Final Styling
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(x_coords[0] - 2.5, x_coords[-1] + 1.2)
    ax.set_ylim(-1.2, 2.5)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

if __name__ == "__main__":
    make_7_stone_final()