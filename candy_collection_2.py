import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch, Ellipse

def draw_kid(ax, x, y, s=0.4):
    """Draws a kid character inside a room."""
    # Head
    ax.add_patch(Circle((x, y + 0.35*s), 0.22*s, facecolor="#FFDBAC", edgecolor="black", lw=1, zorder=10))
    # Body (Shirt)
    ax.add_patch(Rectangle((x - 0.18*s, y - 0.25*s), 0.36*s, 0.45*s, facecolor="#3498db", edgecolor="black", lw=1, zorder=9))
    # Eyes
    ax.add_patch(Circle((x - 0.08*s, y + 0.38*s), 0.025*s, facecolor="black", zorder=11))
    ax.add_patch(Circle((x + 0.08*s, y + 0.38*s), 0.025*s, facecolor="black", zorder=11))
    # Smile
    theta = np.linspace(200, 340, 15)
    ax.plot(x + 0.1*s*np.cos(np.radians(theta)), y + 0.33*s + 0.1*s*np.sin(np.radians(theta)), color="black", lw=1.5, zorder=11)

def draw_candy(ax, x, y, s=0.2, bitter=False):
    """Draws a sweet candy or a horrible-tasting one."""
    color = "#9b59b6" if not bitter else "#3e2723" 
    tri_l = Polygon([[x-s, y+s/2], [x-s, y-s/2], [x, y]], facecolor=color, edgecolor="black", lw=0.5, zorder=7)
    tri_r = Polygon([[x+s, y+s/2], [x+s, y-s/2], [x, y]], facecolor=color, edgecolor="black", lw=0.5, zorder=7)
    center = Ellipse((x, y), width=s*1.2, height=s*0.8, facecolor=color, edgecolor="black", lw=1, zorder=8)
    ax.add_patch(tri_l)
    ax.add_patch(tri_r)
    ax.add_patch(center)
    
    if bitter:
        ax.plot([x-s/2.5, x+s/2.5], [y-s/2.5, y+s/2.5], color="black", lw=1.5, zorder=9)
        ax.plot([x-s/2.5, x+s/2.5], [y+s/2.5, y-s/2.5], color="black", lw=1.5, zorder=9)
        ax.plot([x-0.1, x-0.15], [y+0.2, y+0.35], color="black", lw=0.5, zorder=9)
        ax.plot([x+0.1, x+0.15], [y+0.2, y+0.35], color="black", lw=0.5, zorder=9)

def make_house_new_values(save_path="candy_collection_2.pdf", show=True):
    # Updated rewards as requested: 3, 4, 5, 1
    rewards = [3, 4, 5, 1]
    candy_counts = [3, 4, 5, 1] 
    
    num_rooms = len(rewards)
    room_w, room_h = 4.0, 3.5
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    for i in range(num_rooms):
        x_start = i * room_w
        
        # 1. Draw Room
        rect = Rectangle((x_start, 0), room_w, room_h, facecolor="#FFF9C4", edgecolor="black", lw=2, zorder=2)
        ax.add_patch(rect)
        
        # 2. Reward Text (Centered)
        reward_y = room_h / 2
        ax.text(x_start + room_w/2, reward_y, str(rewards[i]), ha="center", va="center", 
                fontsize=36, fontweight="normal", zorder=5)
        
        # 3. Room Labels
        ax.text(x_start + room_w/2, -0.42, f"room {i}", ha="center", va="top", fontsize=26.4)

        # 4. Draw Candies (Shifted right to avoid overlap)
        count = candy_counts[i]
        # None of the new rewards are negative, so bitter is False for all
        spacing_x, spacing_y = 0.5, 0.4
        start_x = x_start + room_w * 0.65
        
        for c in range(count):
            cx = start_x + (c % 2) * spacing_x
            cy = 0.5 + (c // 2) * spacing_y
            draw_candy(ax, cx, cy, s=0.22, bitter=False)

    # 5. Common Roof
    roof_h = 1.5
    roof = Polygon([[-0.5, room_h], [num_rooms*room_w + 0.5, room_h], 
                    [(num_rooms*room_w)/2, room_h + roof_h]], 
                   facecolor="#E57373", edgecolor="black", lw=2, zorder=3)
    ax.add_patch(roof)

    # 6. Kid in Room 0
    draw_kid(ax, 0.8, 0.6, s=1.6)

    # 7. Arrows (Polished spacing)
    for i in range(num_rooms):
        x_c = i * room_w + room_w/2
        
        # Self-loop (Stay)
        loop_y = reward_y + 0.6 
        ax.add_patch(FancyArrowPatch((x_c - 0.4, loop_y), (x_c + 0.4, loop_y),
                                     connectionstyle="arc3,rad=-2.0", arrowstyle='->,head_width=4,head_length=8',
                                     lw=2, color="black", zorder=6))
        
        # Move Arrow
        if i < num_rooms - 1:
            ax.add_patch(FancyArrowPatch((x_c + 0.6, reward_y), (x_c + room_w - 0.6, reward_y),
                                         connectionstyle="arc3,rad=-0.3", arrowstyle='->,head_width=4,head_length=8',
                                         lw=2, color="black", zorder=6))

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1, num_rooms * room_w + 1)
    ax.set_ylim(-1.5, room_h + roof_h + 0.5)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

if __name__ == "__main__":
    make_house_new_values()