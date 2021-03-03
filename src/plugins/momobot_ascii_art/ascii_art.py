# -*- coding: UTF-8 -*-
"""
 * @author  zfj
 * @date  2020/10/7 18:09
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import requests as req
from io import BytesIO
import os


#       522K
# 0.2   9.15M   失真严重
# 0.3   18.3M
# 0.4   29.4M


sample_rate = 0.8
font_path = os.path.dirname(os.path.abspath(__file__)) + "/思源黑体SourceHanSansCN-Medium.otf"
font_size = 12
# print(sample_rate)
## 获取字符像素个数
#  char_to_pixels(set("test"))
## return [(22, 's'), (22, 't'), (25, 'e')]
def char_to_pixels(text, path=font_path, fontsize=font_size):
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw
    import numpy as np
    from collections import Counter

    res = []
    font = ImageFont.truetype(path, fontsize)
    for char in text:
        w, h = font.getsize(char)
        h *= 2
        image = Image.new("L", (w, h), 1)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), char, font=font)
        arr = np.asarray(image)
        arr = np.where(arr, 0, 1)
        arr = arr[(arr != 0).any(axis=1)]
        # return arr
        res_arr_init = arr.flatten()
        Counter(res_arr_init)
        # print(sum(res_arr_init==1))
        res.append((sum(res_arr_init == 1), char))
    res = sorted(res)
    return res


async def ascii_art(file, save_path, draw_string=" .VM"):
    # im = Image.open(file)
    # print(sample_rate)
    # print("draw_string", draw_string)
    font = ImageFont.truetype(font_path, size=font_size)
    letter_size = font.getsize(draw_string[len(draw_string) - 1 :])
    # print(letter_size)
    if letter_size[0] > font_size - 1:
        # print("中文")
        example_char = "正"
        aspect_ratio_rate = 1
    else:
        # print("英文")
        example_char = "X"
        letter_size = font.getsize(example_char)
        aspect_ratio_rate = letter_size[1] / letter_size[0]
    try:
        response = req.get(file)
        im = Image.open(BytesIO(response.content)).convert("RGB")
        # Compute letter aspect ratio
        # font = ImageFont.load_default()
        font = ImageFont.truetype(font_path, size=font_size)
        aspect_ratio = font.getsize(example_char)[0] / font.getsize(example_char)[1] * aspect_ratio_rate
        new_im_size = np.array([im.size[0] * sample_rate, im.size[1] * sample_rate * aspect_ratio]).astype(int)

        # Downsample the image
        im = im.resize(new_im_size)

        # Keep a copy of image for color sampling
        im_color = np.array(im)

        # Convert to gray scale image
        im = im.convert("L")

        # Convert to numpy array for image manipulation
        im = np.array(im)

        # Defines all the symbols in ascending order that will form the final ascii
        symbols = np.array(list(draw_string))

        # Normalize minimum and maximum to [0, max_symbol_index)
        im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)
        # im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)

        # Generate the ascii art
        # im_new=im*2.5
        ascii = symbols[im.astype(int)]

        # Create an output image for drawing ascii text
        letter_size = font.getsize(example_char)
        letter_size_new = (letter_size[0], int(letter_size[1] / aspect_ratio_rate))
        # print(letter_size)
        im_out_size = new_im_size * letter_size_new
        bg_color = "black"
        im_out = Image.new("RGB", tuple(im_out_size), bg_color)
        draw = ImageDraw.Draw(im_out)

        # Draw text
        y = 0
        for i, line in enumerate(ascii):
            for j, ch in enumerate(line):
                color = tuple(im_color[i, j])  # sample color from original image
                draw.text((letter_size_new[0] * j, y), ch[0], fill=color, font=font)
            y += letter_size_new[1]  # increase y by letter height

        # Save image file
        # im_out_next=ImageEnhance.Brightness(im_out).enhance(0.5)
        im_out.show
        im_out.save(save_path + "/temp.ascii.png")
        return True
    except Exception as e:
        print(e)
        return False
