import os
import plistlib

import numpy as np
from PIL import Image, ImageChops
from typing_extensions import deprecated

formal_icon_names = {
    "cube":    "player",
    "ship":    "ship",
    "ball":    "player_ball",
    "ufo":     "bird",
    "wave":    "dart",
    "robot":   "robot",
    "spider":  "spider",
    "swing":   "swing",
    "jetpack": "jetpack"
}

valid_id_ranges = {
    "player":      (0, 485),
    "ship":        (1, 169),
    "player_ball": (0, 118),
    "bird":        (1, 149),
    "dart":        (1, 96),
    "robot":       (1, 68),
    "spider":      (1, 69),
    "swing":       (1, 43),
    "jetpack":     (1, 8),
}


def layer_extract(src: Image.Image, plist: dict, gamemode_type: str, icon_number: int, p_layer: str = "", *,
                  icon_part: str = "", upscale: bool = False):
    """extracts a layer for an icon from the specified spritesheet and its associated plist"""
    try:

        slice_indexes = plist["frames"][f"{gamemode_type}_{icon_number:0>2}"
                                        f"{icon_part}{p_layer}_001.png"]["textureRect"]
        slice_indexes = slice_indexes.replace("{", "").replace("}", "").split(",")
        slice_indexes[0] = int(slice_indexes[0])
        slice_indexes[1] = int(slice_indexes[1])

        if plist["frames"][f"{gamemode_type}_{icon_number:0>2}{icon_part}{p_layer}_001.png"]["textureRotated"] is True:
            y_size = int(slice_indexes[2])
            x_size = int(slice_indexes[3])
            slice_indexes[2] = slice_indexes[0] + x_size
            slice_indexes[3] = slice_indexes[1] + y_size
        else:
            y_size = int(slice_indexes[3])
            x_size = int(slice_indexes[2])
            slice_indexes[2] = slice_indexes[0] + x_size
            slice_indexes[3] = slice_indexes[1] + y_size

        icon_layer = src.crop(slice_indexes)

        if plist["frames"][f"{gamemode_type}_{icon_number:0>2}{icon_part}{p_layer}_001.png"]["textureRotated"] is True:
            icon_layer = icon_layer.rotate(90, expand=True)

        if upscale is True:
            icon_layer = icon_layer.resize((icon_layer.width * 2, icon_layer.height * 2), resample=Image.Resampling.BOX)

    except KeyError as error:
        if p_layer == "_extra":
            icon_layer = None
        else:
            raise error

    return icon_layer


def layer_color(layer: Image, color_rgba: tuple):
    """
    colors a greyscale rgba image with the given color by multiplying the image with said color

    img = (img_r * r, img_g * g, img_b * b, img_a * a)

    :param layer: the layer you want to color
    :param color_rgba: the color you want to use
    :return: the colored layer
    """
    color = Image.new("RGBA", layer.size, color_rgba)

    layer = ImageChops.multiply(layer, color)

    return layer


def add_to_center(final_img: Image.Image, layer: Image.Image,
                  offset: tuple[int, int], x_offset: int = 0, y_offset: int = 0):
    """
    alpha composites a layer into the center of the final_img

    :param final_img: image to modify
    :param layer: layer to be added to the final_img
    :param offset: offset from the center of the final_img
    :param x_offset: offsets the center in the x-axis
    :param y_offset: offsets the center in the y-axis
    :return:
    """
    img_w, img_h = layer.size
    bg_w, bg_h = final_img.size
    offset = ((bg_w - img_w) // 2 + offset[0] + x_offset, (bg_h - img_h) // 2 - offset[1] + y_offset)

    final_img.alpha_composite(layer, dest=offset)


# ==================================================================================================================== #

# These require the parts to already be composited onto an image of the same size


def add_robot_parts_old(head: Image.Image, ltop: Image.Image, lbot: Image.Image, foot: Image.Image,
                        size: tuple[int, int], is_glow: bool = False, center_offset: tuple = (0, 0)):
    """
    Note: the center offset does not work as intended, preferably leave it at the default
    """
    robot = Image.new("RGBA", size, (255, 255, 255, 0))

    # back leg
    darken = 0.6

    add_to_center(robot, lbot.rotate(36, resample=Image.Resampling.BICUBIC, expand=True),
                  (-30 + center_offset[0], -50 + center_offset[1]))  # robot _03

    add_to_center(robot, ltop.rotate(-65, resample=Image.Resampling.BICUBIC, expand=True),
                  (-36 + center_offset[0], -22 + center_offset[1]))  # robot _02

    add_to_center(robot, foot, (-16 + center_offset[0], -64 + center_offset[1]))  # robot _04

    if not is_glow:
        robot = layer_color(robot, (int(darken * 255), int(darken * 255), int(darken * 255), 255))

    # head
    robot.alpha_composite(head)  # robot _01 it's here where the offset fails because I can't be bothered to write it

    # front leg
    add_to_center(robot, lbot.rotate(43, resample=Image.Resampling.BICUBIC, expand=True),
                  (-22 + center_offset[0], -45 + center_offset[1]))  # robot _03

    add_to_center(robot, ltop.rotate(-45.5, resample=Image.Resampling.BICUBIC, expand=True),
                  (-29 + center_offset[0], -26 + center_offset[1]))  # robot _02

    add_to_center(robot, foot, (6 + center_offset[0], -64 + center_offset[1]))  # robot _04

    return robot


def add_robot_parts(head: Image.Image, ltop: Image.Image, lbot: Image.Image, foot: Image.Image,
                    size: tuple[int, int],
                    is_glow: bool = False, center_offset: tuple = (0, 0)):
    if is_glow and head is None:  # what is this for???
        return None

    # these offsets and what not were taken directly from Robot_AnimDesc.plist
    robot = Image.new("RGBA", size, (255, 255, 255, 0))

    # back leg
    darken = 0.6
    const = 4.1

    add_to_center(robot, lbot.rotate(29.672, resample=Image.Resampling.BICUBIC, expand=True),
                  (int(-7.175 * const) + center_offset[0], int(-6.875 * const) + center_offset[1]))  # robot _03

    add_to_center(robot, ltop.rotate(-57.968, resample=Image.Resampling.BICUBIC, expand=True),
                  (int(-7.175 * const) + center_offset[0], int(-1.025 * const) + center_offset[1]))  # robot _02

    add_to_center(robot, foot,
                  (int(-2.675 * const) + center_offset[0], int(-10.9 * const) + center_offset[1]))  # robot _04

    if not is_glow:
        robot = layer_color(robot, (int(darken * 255), int(darken * 255), int(darken * 255), 255))

    # head
    add_to_center(robot, head.rotate(2.285, resample=Image.Resampling.BICUBIC, expand=True),
                  (int(0.25 * const) + center_offset[0], int(5.5 * const) + center_offset[1]))  # robot _01

    # front leg
    add_to_center(robot, lbot.rotate(42.941, resample=Image.Resampling.BICUBIC, expand=True),
                  (int(-4.525 * const) + center_offset[0], int(-6.625 * const) + center_offset[1]))  # robot _03

    add_to_center(robot, ltop.rotate(-42.501, resample=Image.Resampling.BICUBIC, expand=True),
                  (int(-5.75 * const) + center_offset[0], int(-2.15 * const) + center_offset[1]))  # robot _02

    add_to_center(robot, foot,
                  (int(2.275 * const) + center_offset[0], int(-10.9 * const) + center_offset[1]))  # robot _04

    return robot


def add_spider_parts(head: Image.Image, front: Image.Image, back1: Image.Image, back2: Image.Image,
                     size: tuple[int, int], is_glow: bool = False, center_offset: tuple = (0, 0)):
    if is_glow and head is None:
        return None

    # these offsets and what not were taken directly from Spider_AnimDesc.plist
    spider = Image.new("RGBA", size, (255, 255, 255, 0))

    # left legs
    darken = 0.6
    const = 3.6

    add_to_center(spider, front.resize((int(front.width * 0.88), int(front.height * 0.88))),
                  (int(5.625 * const) + center_offset[0], int(-7.5 * const) + center_offset[1]))  # spider _02

    add_to_center(spider, front.resize((int(front.width * 0.88), int(front.height * 0.88)))
                  .transpose(Image.Transpose.FLIP_LEFT_RIGHT),
                  (int(16 * const) + center_offset[0], int(-7.5 * const) + center_offset[1]))  # spider _02

    if not is_glow:
        spider = layer_color(spider, (int(darken * 255), int(darken * 255), int(darken * 255), 255))

    # right legs
    # back leg
    add_to_center(spider, back2.rotate(7.682, resample=Image.Resampling.BICUBIC, expand=True),
                  (int(-5 * const) + center_offset[0], int(0.125 * const) + center_offset[1]))  # spider _04

    # head
    add_to_center(spider, head,
                  (int(0.625 * const) + center_offset[0], int(4.5 * const) + center_offset[1]))  # spider _01

    # front leg
    add_to_center(spider, back1.rotate(-38.963, resample=Image.Resampling.BICUBIC, expand=True),
                  (int(-14.825 * const) + center_offset[0], int(-7.7 * const) + center_offset[1]))  # spider _03

    add_to_center(spider, front,
                  (int(-2.75 * const) + center_offset[0], int(-6.625 * const) + center_offset[1]))  # spider _02

    return spider


# ==================================================================================================================== #


def process_offset(offset_str: str, icon_gamemode: str, p_layer: str, upscale: bool):
    """
    Converts a raw offset string (as found in the plist) into a tuple of integers

    This is used to handle cases such as an empty string (the game allows those), floating point values (they should
    not be allowed, but there are a couple sprites that have them in the base game, and the games doesn't crash beacuse
    of it), and a special offset for ufo domes (because that's apparently a thing)

    The upscale bool is used for upscaled, medium resolution sprites. This because some functions, such as add robot and
    spider parts, are only programmed to work on uhd textures, therefore you're required to upscale medium textures to
    work with those (if you instead want to work with low resolution sprites, please reconsider your life choices)
    """
    offset = offset_str.replace("{", "").replace("}", "").split(",")

    # I've only had to handle this because of texture packs :'v
    # surprised that the game doesn't crash with this
    # turns out the game uses a (0, 0) offset by default, so it allows for an empty string, this is kind of annoying
    if offset[0] == "":
        offset = (0, 0)
    else:
        # oh, and this int(float()) thing has to do with not allowing floats on sprite offsets
        # since I assumed there would be some texture packs that would do this without realizing it back when I made
        # it support other texture packs, but turns out there are 3 icons on the base game that have floats in some
        # of their sprites, and all of them are 3x3 transparent pixels. I love robtop games
        offset = (int(float(offset[0])), int(float(offset[1])))

    if upscale is True:
        offset = (offset[0] * 2, offset[1] * 2)

    # turns out the damn ufo domes have a default value too, what the hell man
    # I don't know what I'm doing anymore really
    if icon_gamemode == "bird" and p_layer == "_3":
        offset = (offset[0], offset[1] - 59)

    return offset


# ==================================================================================================================== #

# Sheetless icon compositing

# __"icon"
#  |
#  |__"_01"
#  | |
#  | |__""
#  | |__"_2"
#  | |__"_extra" <- "_02", "_03", and "_04" don't have this layer
#  | |__"_3"     <- ufo only
#  | |__"_glow"
#  |
#  |__"_02"
#  | | ...
#  |
#  |__"_03"
#  | | ...
#  |
#  |__"_04"
#    | ...

def make_part(images: dict[str, Image.Image], offsets: dict[str, tuple[int, int]], size: tuple[int, int],
              p1_color: tuple, p2_color: tuple, glow_color: tuple, extra_color: tuple, *,
              merge_glow: bool, x_offset: int = 0, y_offset: int = 0):
    """
    renders an icon part given its layers and offsets, the dict structure should be as follows:

    - images / offsets
        - "p1"
        - "p2"
        - "extra" <- not required
        - "dome"  <- not required
        - "glow"

    the values to the keys in the image dict should be PIL.Image.Image objects,
    and the values to the keys in the offsets dict should be a tuple of 2 integers

    only the offsets dict is checked for the non required layers
    """
    bg_img = Image.new("RGBA", size, (255, 255, 255, 0))
    bg_img_glow = bg_img.copy()

    if offsets.get("dome") is not None:
        add_to_center(bg_img, images["dome"], offsets["dome"], x_offset=x_offset, y_offset=y_offset)

    add_to_center(bg_img, layer_color(images["p2"], p2_color), offsets["p2"], x_offset=x_offset, y_offset=y_offset)

    add_to_center(bg_img, layer_color(images["p1"], p1_color), offsets["p1"], x_offset=x_offset, y_offset=y_offset)

    if offsets.get("extra") is not None:
        add_to_center(bg_img, layer_color(images["extra"], extra_color), offsets["extra"],
                      x_offset=x_offset, y_offset=y_offset)

    add_to_center(bg_img_glow, layer_color(images["glow"], glow_color), offsets["glow"],
                  x_offset=x_offset, y_offset=y_offset)

    if merge_glow:
        return Image.alpha_composite(bg_img_glow, bg_img)

    return bg_img, bg_img_glow


def make_icon(icon_gamemode: str, images: dict[str, dict[str, Image.Image]],
              offsets: dict[str, dict[str, tuple[int, int]]], size: tuple[int, int],
              p1_color: tuple, p2_color: tuple, glow_color: tuple, extra_color: tuple, *,
              merge_glow: bool = True, center_offset: tuple = (0, 0)):
    """
    renders an icon given its layers and offsets, the dict structure should be as follows:

    - images / offsets
        - "01":
            - "p1"
            - "p2"
            - "extra" <- "_02", "_03", and "_04" don't have this layer (though this isn't checked)
            - "dome"  <- ufo only (will not throw error if the gamemode isn't ufo yet a dome is defined)
            - "glow"
        - "02"
        - "03"
        - "04"

    the values to the keys in the image dict should be PIL.Image.Image objects,
    and the values to the keys in the offsets dict should be a tuple of 2 integers
    """

    if icon_gamemode not in {"player", "ship", "player_ball", "bird", "dart", "robot", "spider", "swing", "jetpack"}:
        did_you_mean = f". Did you mean '{formal_icon_names[icon_gamemode]}' instead?" \
            if formal_icon_names.get(icon_gamemode) is not None else "."

        raise ValueError(f"icon of gamemode {icon_gamemode} is not supported{did_you_mean}")

    if icon_gamemode == "bird":
        offsets["01"]["dome"] = (offsets["01"]["dome"][0], offsets["01"]["dome"][1] + 59)

        icon, glow = make_part(images["01"], offsets["01"], size, p1_color, p2_color, glow_color, extra_color,
                               merge_glow=False, y_offset=int(images["01"]["dome"].height / 4))

    elif icon_gamemode == "robot":
        robot_head, robot_head_glow = make_part(images["01"], offsets["01"], size, p1_color, p2_color, glow_color,
                                                extra_color, merge_glow=False)
        robot_leg1, robot_leg1_glow = make_part(images["02"], offsets["02"], size, p1_color, p2_color, glow_color,
                                                extra_color, merge_glow=False)
        robot_leg2, robot_leg2_glow = make_part(images["03"], offsets["03"], size, p1_color, p2_color, glow_color,
                                                extra_color, merge_glow=False)
        robot_leg3, robot_leg3_glow = make_part(images["04"], offsets["04"], size, p1_color, p2_color, glow_color,
                                                extra_color, merge_glow=False)

        icon, glow = add_robot_parts(robot_head, robot_leg1, robot_leg2, robot_leg3, size, False, center_offset), \
            add_robot_parts(robot_head_glow, robot_leg1_glow, robot_leg2_glow, robot_leg3_glow, size, True,
                            center_offset)

    elif icon_gamemode == "spider":
        spider_head, spider_head_glow = make_part(images["01"], offsets["01"], size, p1_color, p2_color, glow_color,
                                                  extra_color, merge_glow=False)
        spider_leg1, spider_leg1_glow = make_part(images["02"], offsets["02"], size, p1_color, p2_color, glow_color,
                                                  extra_color, merge_glow=False)
        spider_leg2, spider_leg2_glow = make_part(images["03"], offsets["03"], size, p1_color, p2_color, glow_color,
                                                  extra_color, merge_glow=False)
        spider_leg3, spider_leg3_glow = make_part(images["04"], offsets["04"], size, p1_color, p2_color, glow_color,
                                                  extra_color, merge_glow=False)

        icon, glow = (add_spider_parts(spider_head, spider_leg1, spider_leg2, spider_leg3, size, False, center_offset),
                      add_spider_parts(spider_head_glow, spider_leg1_glow, spider_leg2_glow, spider_leg3_glow, size,
                                       True, center_offset))

    else:
        icon, glow = make_part(images["01"], offsets["01"], size, p1_color, p2_color, glow_color, extra_color,
                               merge_glow=False, x_offset=center_offset[0], y_offset=center_offset[1])

    if merge_glow:
        return Image.alpha_composite(glow, icon)

    return icon, glow


# ==================================================================================================================== #

# Composite icons from spritesheet


def add_layer_to_img(final_img: Image.Image, src: Image.Image, plist: dict, icon_gamemode: str,
                     icon_number: int, color: tuple, p_layer: str = "", *, icon_part: str = "",
                     x_offset: int = 0, y_offset: int = 0, upscale: bool = False):
    layer = layer_extract(src, plist, icon_gamemode, icon_number, p_layer, icon_part=icon_part, upscale=upscale)

    if layer is not None:
        layer = layer_color(layer, color)

        # gets the offset
        offset = plist["frames"][f"{icon_gamemode}_{icon_number:0>2}{icon_part}{p_layer}_001.png"]["spriteOffset"]

        offset = process_offset(offset, icon_gamemode, p_layer, upscale)

        add_to_center(final_img, layer, offset, x_offset, y_offset)


def get_icon_and_glow(icon_name: str, icon_number: int, p1_color: tuple, p2_color: tuple, glow_color: tuple,
                      source_02: Image.Image, plist_02: dict, source_glow: Image.Image, plist_glow: dict,
                      use_glow: bool, size: tuple[int, int] = (220, 220), icon_part: str = "", *, upscale: bool = False,
                      center_offset: tuple = (0, 0)):
    icon = Image.new('RGBA', size, (255, 255, 255, 0))

    # adds an extra offset if the icon is an ufo because of the dome
    if icon_name == "bird":
        ufo_offset = int(layer_extract(source_02, plist_02, icon_name, icon_number, "_3", upscale=upscale).height / 2.5)
        # ufo_offset = 0
    else:
        ufo_offset = 0

    # glow layer
    if use_glow:
        glow = Image.new('RGBA', size, (255, 255, 255, 0))
        add_layer_to_img(glow, source_glow, plist_glow, icon_name, icon_number, glow_color, "_glow",
                         x_offset=center_offset[0], y_offset=ufo_offset + center_offset[1], icon_part=icon_part,
                         upscale=upscale)
    else:
        glow = None

    # dome
    if ufo_offset != 0:
        add_layer_to_img(icon, source_02, plist_02, "bird", icon_number, (255, 255, 255, 255), "_3",
                         x_offset=center_offset[0], y_offset=-ufo_offset + center_offset[1], upscale=upscale)

    # p2 layer
    add_layer_to_img(icon, source_02, plist_02, icon_name, icon_number, p2_color, "_2",
                     x_offset=center_offset[0], y_offset=ufo_offset + center_offset[1], icon_part=icon_part,
                     upscale=upscale)

    # p1 layer
    add_layer_to_img(icon, source_02, plist_02, icon_name, icon_number, p1_color,
                     x_offset=center_offset[0], y_offset=ufo_offset + center_offset[1], icon_part=icon_part,
                     upscale=upscale)

    # extra layer (doesn't do anything if there's no extra layer)
    add_layer_to_img(icon, source_02, plist_02, icon_name, icon_number, (255, 255, 255, 255), "_extra",
                     x_offset=center_offset[0], y_offset=ufo_offset + center_offset[1], icon_part=icon_part,
                     upscale=upscale)

    return icon, glow


def make_robot(robot_id: int, p1_color: tuple, p2_color: tuple, glow_color: tuple, use_glow: bool,
               source_02: Image.Image, plist_02: dict, size: tuple[int, int] = (220, 220), *, alt_pose: bool = False,
               upscale: bool = False, center_offset: tuple = (0, 0)):
    robot_head, robot_head_glow = get_icon_and_glow("robot", robot_id, p1_color, p2_color, glow_color,
                                                    source_02, plist_02, source_02, plist_02, use_glow, size, "_01",
                                                    upscale=upscale)
    robot_leg1, robot_leg1_glow = get_icon_and_glow("robot", robot_id, p1_color, p2_color, glow_color,
                                                    source_02, plist_02, source_02, plist_02, use_glow, size, "_02",
                                                    upscale=upscale)
    robot_leg2, robot_leg2_glow = get_icon_and_glow("robot", robot_id, p1_color, p2_color, glow_color,
                                                    source_02, plist_02, source_02, plist_02, use_glow, size, "_03",
                                                    upscale=upscale)
    robot_leg3, robot_leg3_glow = get_icon_and_glow("robot", robot_id, p1_color, p2_color, glow_color,
                                                    source_02, plist_02, source_02, plist_02, use_glow, size, "_04",
                                                    upscale=upscale)

    if alt_pose:
        return add_robot_parts_old(robot_head, robot_leg1, robot_leg2, robot_leg3, size, False, center_offset), \
            add_robot_parts_old(robot_head_glow, robot_leg1_glow, robot_leg2_glow, robot_leg3_glow, size, True,
                                center_offset)
    else:
        return add_robot_parts(robot_head, robot_leg1, robot_leg2, robot_leg3, size, False, center_offset), \
            add_robot_parts(robot_head_glow, robot_leg1_glow, robot_leg2_glow, robot_leg3_glow, size, True,
                            center_offset)


def make_spider(spider_id: int, p1_color: tuple, p2_color: tuple, glow_color: tuple, use_glow: bool,
                source_02: Image.Image, plist_02: dict, size: tuple[int, int] = (220, 220), *,
                upscale: bool = False, center_offset: tuple = (0, 0)):
    spider_head, spider_head_glow = get_icon_and_glow("spider", spider_id, p1_color, p2_color, glow_color,
                                                      source_02, plist_02, source_02, plist_02, use_glow, size, "_01",
                                                      upscale=upscale)
    spider_leg1, spider_leg1_glow = get_icon_and_glow("spider", spider_id, p1_color, p2_color, glow_color,
                                                      source_02, plist_02, source_02, plist_02, use_glow, size, "_02",
                                                      upscale=upscale)
    spider_leg2, spider_leg2_glow = get_icon_and_glow("spider", spider_id, p1_color, p2_color, glow_color,
                                                      source_02, plist_02, source_02, plist_02, use_glow, size, "_03",
                                                      upscale=upscale)
    spider_leg3, spider_leg3_glow = get_icon_and_glow("spider", spider_id, p1_color, p2_color, glow_color,
                                                      source_02, plist_02, source_02, plist_02, use_glow, size, "_04",
                                                      upscale=upscale)

    return (add_spider_parts(spider_head, spider_leg1, spider_leg2, spider_leg3, size, False, center_offset),
            add_spider_parts(spider_head_glow, spider_leg1_glow, spider_leg2_glow, spider_leg3_glow, size, True,
                             center_offset))


def make_icon_from_spritesheet(icon_name: str, icon_id: int, p1_color: tuple, p2_color: tuple, glow_color: tuple,
                               source_02: Image.Image, plist_02: dict, source_glow: Image.Image, plist_glow: dict,
                               use_glow: bool,
                               size: tuple[int, int] = (220, 220), *, merge_glow: bool = True,
                               alt_pose_robot: bool = False,
                               upscale: bool = False, center_offset: tuple = (0, 0)):
    if icon_name == "robot":
        icon, glow = make_robot(icon_id, p1_color, p2_color, glow_color, use_glow, source_02, plist_02, size,
                                alt_pose=alt_pose_robot, upscale=upscale, center_offset=center_offset)
    elif icon_name == "spider":
        icon, glow = make_spider(icon_id, p1_color, p2_color, glow_color, use_glow, source_02, plist_02, size,
                                 upscale=upscale, center_offset=center_offset)
    else:
        icon, glow = get_icon_and_glow(icon_name, icon_id, p1_color, p2_color, glow_color,
                                       source_02, plist_02, source_glow, plist_glow, use_glow, size,
                                       upscale=upscale, center_offset=center_offset)

    if merge_glow:
        return Image.alpha_composite(glow, icon) if glow is not None else icon

    else:
        return icon, glow


@deprecated("Use Icon22 instead")
class Icon:
    def __init__(self, gamemode: str, sprite_id: int,
                 p1_color: tuple[int, int, int, int], p2_color: tuple[int, int, int, int],
                 glow_color: tuple[int, int, int, int],
                 use_glow: bool, texture_quality: str = "uhd"):
        self.gamemode = gamemode
        if gamemode in formal_icon_names.values():
            self.gamemode_name = self.gamemode
        else:
            try:
                self.gamemode_name = formal_icon_names[self.gamemode]
            except KeyError:
                raise ValueError(f"gamemode `{gamemode}` is not valid")

        self.id = sprite_id

        self.p1 = p1_color
        self.p2 = p2_color
        self.glow = glow_color

        self.use_glow = use_glow

        file_name = f"{self.gamemode_name}_{sprite_id:0>2}{'-' if texture_quality != '' else ''}{texture_quality}"

        source_spritesheet = (Image.open(os.path.join(os.path.dirname(__file__), "icons", f"{file_name}.png"))
                              .convert("RGBA"))

        with open(os.path.join(os.path.dirname(__file__), "icons", f"{file_name}.plist"), "rb") as plist_file:
            plist = plistlib.load(plist_file)

        self.source = source_spritesheet
        self.plist = plist

    def render(self, source_size: tuple[int, int] = (220, 220), center_offset: tuple = (0, 0), merge_glow: bool = True):
        return make_icon_from_spritesheet(self.gamemode_name, self.id, self.p1, self.p2, self.glow,
                                          self.source, self.plist, self.source, self.plist, self.use_glow,
                                          source_size, center_offset=center_offset, merge_glow=merge_glow)

    def change_palette(self, p1_color: tuple[int, int, int] = None,
                       p2_color: tuple[int, int, int] = None,
                       glow_color: tuple[int, int, int] = None):

        if p1_color is not None:
            self.p1 = p1_color

        if p2_color is not None:
            self.p2 = p2_color

        if glow_color is not None:
            self.glow = glow_color


class Icon22:
    def __init__(self, spritesheet: Image.Image, plist_dict: dict,
                 p1_color: tuple[int, int, int, int], p2_color: tuple[int, int, int, int],
                 glow_color: tuple[int, int, int, int],
                 use_glow: bool):

        gamemode, icon_id = plist_dict["metadata"]["realTextureFileName"].split("/")[1].split(".")[0].split("-")[
            0].rsplit("_", maxsplit=1)

        self.gamemode_name = gamemode
        self.id = int(icon_id)

        self.p1 = p1_color
        self.p2 = p2_color
        self.glow = glow_color

        self.use_glow = use_glow

        self.source = spritesheet
        self.plist = plist_dict

    def render(self, source_size: tuple[int, int] = (220, 220), center_offset: tuple = (0, 0), merge_glow: bool = True):
        return make_icon_from_spritesheet(self.gamemode_name, self.id, self.p1, self.p2, self.glow,
                                          self.source, self.plist, self.source, self.plist, self.use_glow,
                                          source_size, center_offset=center_offset, merge_glow=merge_glow)

    def change_palette(self, p1_color: tuple[int, int, int] = None,
                       p2_color: tuple[int, int, int] = None,
                       glow_color: tuple[int, int, int] = None):

        if p1_color is not None:
            self.p1 = p1_color

        if p2_color is not None:
            self.p2 = p2_color

        if glow_color is not None:
            self.glow = glow_color

    @classmethod
    def from_vanilla(cls, gamemode: str, sprite_id: int,
                     p1_color: tuple[int, int, int, int], p2_color: tuple[int, int, int, int],
                     glow_color: tuple[int, int, int, int],
                     use_glow: bool, *, texture_quality: str = "uhd"):

        if gamemode in formal_icon_names.values():
            gamemode_name = gamemode
        else:
            try:
                gamemode_name = formal_icon_names[gamemode]
            except KeyError:
                raise ValueError(f"gamemode `{gamemode}` is not valid")

        if not (valid_id_ranges[gamemode_name][0] <= sprite_id <= valid_id_ranges[gamemode_name][1]):
            raise ValueError(f"a {gamemode} of id {sprite_id} doesn't exist or is not supported")

        file_name = f"{gamemode_name}_{sprite_id:0>2}{'-' if texture_quality != '' else ''}{texture_quality}"

        source_spritesheet = (Image.open(os.path.join(os.path.dirname(__file__), "icons", f"{file_name}.png"))
                              .convert("RGBA"))

        with open(os.path.join(os.path.dirname(__file__), "icons", f"{file_name}.plist"), "rb") as plist_file:
            plist = plistlib.load(plist_file)

        return cls(source_spritesheet, plist, p1_color, p2_color, glow_color, use_glow)


class IconSet:

    def __init__(self, cube: int, ship: int, ball: int, ufo: int, wave: int, robot: int, spider: int, swing: int,
                 jetpack: int,
                 p1_color: tuple[int, int, int, int], p2_color: tuple[int, int, int, int],
                 glow_color: tuple[int, int, int, int],
                 use_glow: bool, texture_quality: str = "uhd", **kwargs):
        self.cube = Icon22.from_vanilla("cube", cube, p1_color, p2_color, glow_color, use_glow,
                                        texture_quality=texture_quality)
        self.ship = Icon22.from_vanilla("ship", ship, p1_color, p2_color, glow_color, use_glow,
                                        texture_quality=texture_quality)
        self.ball = Icon22.from_vanilla("ball", ball, p1_color, p2_color, glow_color, use_glow,
                                        texture_quality=texture_quality)
        self.ufo = Icon22.from_vanilla("ufo", ufo, p1_color, p2_color, glow_color, use_glow,
                                       texture_quality=texture_quality)
        self.wave = Icon22.from_vanilla("wave", wave, p1_color, p2_color, glow_color, use_glow,
                                        texture_quality=texture_quality)
        self.robot = Icon22.from_vanilla("robot", robot, p1_color, p2_color, glow_color, use_glow,
                                         texture_quality=texture_quality)
        self.spider = Icon22.from_vanilla("spider", spider, p1_color, p2_color, glow_color, use_glow,
                                          texture_quality=texture_quality)
        self.swing = Icon22.from_vanilla("swing", swing, p1_color, p2_color, glow_color, use_glow,
                                         texture_quality=texture_quality)
        self.jetpack = Icon22.from_vanilla("jetpack", jetpack, p1_color, p2_color, glow_color, use_glow,
                                           texture_quality=texture_quality)

        self.p1 = p1_color
        self.p2 = p2_color
        self.glow = glow_color

        self.use_glow = use_glow

        self.texture_quality = texture_quality

    def render_iconset(self):
        iconset = np.hstack([self.cube.render(), self.ship.render(), self.ball.render(), self.ufo.render(),
                             self.wave.render(), self.robot.render(), self.spider.render(), self.swing.render(),
                             self.jetpack.render()])
        return Image.fromarray(iconset, "RGBA")


class IconBuilder:

    def __init__(self, p1_color: tuple, p2_color: tuple, glow_color: tuple, use_glow: bool,
                 source_02: Image.Image, plist_02: dict, source_glow: Image.Image, plist_glow: dict,
                 layer_size: tuple[int, int] = (220, 220),
                 *, alt_pose_robot: bool = False, upscale_icons: bool = False, **kwargs):
        self.p1 = p1_color
        self.p2 = p2_color
        self.glow = glow_color
        self.use_glow = use_glow

        self.s_02 = source_02
        self.p_02 = plist_02
        self.s_glow = source_glow
        self.p_glow = plist_glow

        self.size = layer_size
        self.upscale = upscale_icons

        self.alt_pose = alt_pose_robot

    def make_icon(self, icon_name: str, icon_id: int):
        return make_icon_from_spritesheet(icon_name, icon_id, self.p1, self.p2, self.glow, self.s_02, self.p_02,
                                          self.s_glow, self.p_glow, self.use_glow, self.size,
                                          alt_pose_robot=self.alt_pose, upscale=self.upscale)

    def make_iconset(self, cube_id: int, ship_id: int, ball_id: int, ufo_id: int, wave_id: int, robot_id: int,
                     spider_id: int):
        cube = make_icon_from_spritesheet("player", cube_id, self.p1, self.p2, self.glow, self.s_02, self.p_02,
                                          self.s_glow, self.p_glow, self.use_glow, self.size, upscale=self.upscale)
        ship = make_icon_from_spritesheet("ship", ship_id, self.p1, self.p2, self.glow, self.s_02, self.p_02,
                                          self.s_glow, self.p_glow, self.use_glow, self.size, upscale=self.upscale)
        ball = make_icon_from_spritesheet("player_ball", ball_id, self.p1, self.p2, self.glow, self.s_02, self.p_02,
                                          self.s_glow, self.p_glow, self.use_glow, self.size, upscale=self.upscale)
        ufo = make_icon_from_spritesheet("bird", ufo_id, self.p1, self.p2, self.glow, self.s_02, self.p_02, self.s_glow,
                                         self.p_glow, self.use_glow, self.size, upscale=self.upscale)
        wave = make_icon_from_spritesheet("dart", wave_id, self.p1, self.p2, self.glow, self.s_02, self.p_02,
                                          self.s_glow, self.p_glow, self.use_glow, self.size, upscale=self.upscale)
        robot = make_icon_from_spritesheet("robot", robot_id, self.p1, self.p2, self.glow, self.s_02, self.p_02,
                                           self.s_glow, self.p_glow, self.use_glow, self.size,
                                           alt_pose_robot=self.alt_pose, upscale=self.upscale)
        spider = make_icon_from_spritesheet("spider", spider_id, self.p1, self.p2, self.glow, self.s_02, self.p_02,
                                            self.s_glow, self.p_glow, self.use_glow, self.size, upscale=self.upscale)

        iconset = np.hstack([cube, ship, ball, ufo, wave, robot, spider])
        return Image.fromarray(iconset, "RGBA")

# file_name = "player_ball_64"
#
# source_spritesheet = (Image.open(os.path.join(os.path.dirname(__file__), "icons", f"{file_name}.png"))
#                         .convert("RGBA"))
#
# with open(os.path.join(os.path.dirname(__file__), "icons", f"{file_name}.plist"), "rb") as plist_file:
#     plist = plistlib.load(plist_file)
#
# test_icon = Icon22.from_vanilla("cube", 489, (255, 255, 255, 255), (255, 255 ,255, 255), (255, 255, 255, 255), True)
# test_icon.render().show()
# test_icon = Icon22(source_spritesheet, plist)
