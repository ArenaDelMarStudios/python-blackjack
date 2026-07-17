import os
from PIL import Image

# Setup paths based on your requested layout
INPUT_DIR = "cards 500x726"
OUTPUT_DIR = "cards"
TARGET_WIDTH = 172
TARGET_HEIGHT = 250

def batch_resize_cards():
    # Verify the high-res folder actually exists
    if not os.path.exists(INPUT_DIR):
        print(f"❌ Error: Could not find the folder '{INPUT_DIR}'")
        print("Please make sure your high-res cards are inside that folder.")
        return

    # Create the optimized output folder if it doesn't exist yet
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Gather all images inside the high-res folder
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.png')]
    
    if not files:
        print(f"⚠ No PNG files found inside '{INPUT_DIR}'.")
        return

    print(f"🔄 Found {len(files)} files. Optimizing down to {TARGET_WIDTH}x{TARGET_HEIGHT}...")

    success_count = 0
    for filename in files:
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        try:
            with Image.open(input_path) as img:
                # LANCZOS keeps text/details sharp. 
                # Keeping RGBA mode preserves your brand-new rounded corners!
                resized_img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
                resized_img.save(output_path, "PNG")
                success_count += 1
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")

    print(f"✅ Success! {success_count} optimized cards are ready inside the '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    batch_resize_cards()