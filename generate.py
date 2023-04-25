#!/usr/bin/env python

import cairo
import math
import itertools
import pathlib

from PIL import Image

def generate_circle(width, height, radius, thickness, directory="output"):
    s = cairo.ImageSurface(cairo.FORMAT_A8, width, height)
    ctx = cairo.Context(s)

    ctx.set_source_rgba(0.0, 0.0, 0.0, 0.0)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()

    ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
    ctx.arc(width / 2, height / 2, radius, 0, 2*math.pi)
    ctx.set_line_width(thickness)
    ctx.stroke()

    data = s.get_data()
    stride = s.get_stride()

    img = Image.new("P", (width, height), 0)
    mod_img = Image.new("P", (width, height), 0)

    # Create the palette for the mod texture
    palette = []
    palette.extend([255, 0, 255])

    for x in range(128):
        palette.extend([x, x, x])

    mod_img.putpalette(palette, "RGB")

    for x in range(width):
        for y in range(height):
            pos = (y * stride) + x
            value = data[pos]

            img.putpixel((x, y), value)

            if value == 0:
                # Color all transparent pixels as magenta
                mod_img.putpixel((x, y), 0)
            else:
                # Compute appropriate black value by inverting the alpha and
                # scaling between [0, 127]
                v = 255 - value
                v = v // 2
                mod_img.putpixel((x, y), v + 1)

    output_dir = pathlib.Path(directory)
    output_dir.mkdir(exist_ok=1)

    img_path = output_dir / f"CircleD{int(radius * 2)}T{int(thickness)}.bmp"
    mod_img_path = output_dir / f"CircleD{int(radius * 2)}T{int(thickness)}Modulate.bmp"

    img.save(img_path, "bmp")
    mod_img.save(mod_img_path, "bmp")


width = 64
height = 64

radii = [3.5, 4.0]
thicknesses = [1.0, 2.0, 3.0, 4.0, 5.0]

for (r, t) in itertools.product(radii, thicknesses):
    generate_circle(width, height, r, t)
