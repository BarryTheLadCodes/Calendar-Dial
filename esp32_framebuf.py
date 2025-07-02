import gc

WIDTH = 480
HEIGHT = 480
BYTES_PER_PIXEL_IN = 4  # RGBA8888
BYTES_PER_PIXEL_OUT = 2  # RGB565

gc.collect()  # Run garbage collector to free memory

print("Allocating output buffer...")
rgb565_buf = bytearray(WIDTH * HEIGHT * BYTES_PER_PIXEL_OUT)

print("Reading input file and converting RGBA to RGB565...")
with open("calendarface_final.raw", "rb") as f_in:
    for y in range(HEIGHT):
        # Read one line of RGBA input
        line_rgba = bytearray(f_in.read(WIDTH * BYTES_PER_PIXEL_IN))
        if len(line_rgba) != WIDTH * BYTES_PER_PIXEL_IN:
            raise ValueError(f"Unexpected EOF at line {y}")

        # Convert line pixels and store in rgb565_buf at correct offset
        for x in range(WIDTH):
            r = line_rgba[x*4 + 0]
            g = line_rgba[x*4 + 1]
            b = line_rgba[x*4 + 2]

            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            pos = (y * WIDTH + x) * BYTES_PER_PIXEL_OUT
            rgb565_buf[pos] = rgb565 & 0xFF
            rgb565_buf[pos + 1] = rgb565 >> 8

print("All lines converted. Writing to output file...")

with open("fb.raw", "wb") as f_out:
    f_out.write(rgb565_buf)

print("Done.")