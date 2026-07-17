import os
from PIL import Image, ImageDraw

BACKS_DIR = "card backs"
WIDTH, HEIGHT = 500, 726
CORNER_RADIUS = 26  # Perfect proportional radius for 500x726 dimensions

def draw_rounded_card_back(color_hex, filename):
    # 1. Start with a COMPLETELY transparent base canvas (0, 0, 0, 0)
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 2. Draw the white card base with rounded corners
    draw.rounded_rectangle(
        [0, 0, WIDTH, HEIGHT], 
        radius=CORNER_RADIUS, 
        fill="#FFFFFF"
    )
    
    # 3. Draw the colored inner felt rectangle with matching rounded corners
    margin = 30
    draw.rounded_rectangle(
        [margin, margin, WIDTH - margin, HEIGHT - margin], 
        radius=max(5, CORNER_RADIUS - 10), 
        fill=color_hex
    )
    
    # 4. Generate the classic diamond geometric pattern inside the colored boundary
    pattern_margin = margin + 10
    step = 25  
    
    for x in range(pattern_margin, WIDTH - pattern_margin, step):
        for y in range(pattern_margin, HEIGHT - pattern_margin, step):
            # Only draw the patterns if they safely sit within our inner colored space
            draw.line([x, y, x + 10, y + 10], fill="#FFFFFF", width=2)
            draw.line([x + 10, y, x, y + 10], fill="#FFFFFF", width=2)

    # 5. Save out as a transparent PNG file
    os.makedirs(BACKS_DIR, exist_ok=True)
    target_path = os.path.join(BACKS_DIR, filename)
    img.save(target_path, "PNG")
    print(f"Created high-res transparent card back: {target_path}")

if __name__ == "__main__":
    # Render both custom matching asset styles with clean edges
    draw_rounded_card_back("#B22222", "back_red.png")    # Firebrick Red
    draw_rounded_card_back("#104E8B", "back_blue.png")   # Deep Royal Blue