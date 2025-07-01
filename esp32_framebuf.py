import framebuf  # type: ignore

buf = bytearray(480 * 480 * 2)  # 2 bytes per pixel
fb = framebuf.FrameBuffer(buf, 480, 480, framebuf.RGB565)

# Fill buffer with green color
fb.fill(0x13f8)  # RGB565 for green
print("Buffer filled with green color")

with open("fb.raw", "wb") as f:
    f.write(buf)