import requests
import numpy as np
import matplotlib.pyplot as plt

# Replace with your ESP32's IP address
esp32_url = "http://192.168.0.179/"  # <-- change to actual IP

# Image dimensions
width = 480
height = 480

# Download the raw file
print("Downloading...")
response = requests.get(esp32_url)

if response.status_code == 200:
    raw_data = response.content
    print(f"Downloaded {len(raw_data)} bytes")

    expected_size = width * height * 2  # RGB565 = 2 bytes per pixel
    if len(raw_data) != expected_size:
        print(f"⚠️ Expected {expected_size} bytes, got {len(raw_data)}")

    # Convert to numpy array of 16-bit integers
    pixels = np.frombuffer(raw_data, dtype=np.uint16)

    # Extract RGB components
    r = ((pixels >> 11) & 0x1F) << 3
    g = ((pixels >> 5) & 0x3F) << 2
    b = (pixels & 0x1F) << 3

    # Stack into 8-bit RGB image
    rgb = np.stack((r, g, b), axis=-1).astype(np.uint8)
    rgb = rgb.reshape((height, width, 3))

    # Display the image
    plt.imshow(rgb)
    plt.title("ESP32 Framebuffer (RGB565)")
    plt.axis('off')
    plt.show()

else:
    print("Failed to download image. HTTP status:", response.status_code)