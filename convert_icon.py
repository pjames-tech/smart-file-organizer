from PIL import Image
import sys

try:
    img = Image.open("app_icon.png")
    # Save as ICO with multiple sizes for best scaling
    img.save("app_icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("Icon converted successfully.")
except Exception as e:
    print(f"Error converting icon: {e}")
