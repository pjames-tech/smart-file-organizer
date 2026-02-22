"""Create polished icon assets from a high-quality folder reference image."""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


CANVAS_SIZE = 1024
ICON_PADDING = 0.06
BG_TOLERANCE = 26

SOURCE_ICON = Path("icon_reference.png")
APP_ICON_PNG = Path("app_icon.png")
APP_ICON_ICO = Path("app_icon.ico")
ICO_SIZES = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]


def _close_to_color(px: tuple[int, ...], target: tuple[int, int, int], tolerance: int) -> bool:
    return (
        abs(px[0] - target[0]) <= tolerance
        and abs(px[1] - target[1]) <= tolerance
        and abs(px[2] - target[2]) <= tolerance
    )


def _remove_flat_background(image: Image.Image, tolerance: int = BG_TOLERANCE) -> Image.Image:
    rgba = image.convert("RGBA")
    width, height = rgba.size
    pixels = rgba.load()

    corners = [
        pixels[0, 0],
        pixels[width - 1, 0],
        pixels[0, height - 1],
        pixels[width - 1, height - 1],
    ]
    bg = (
        sum(c[0] for c in corners) // 4,
        sum(c[1] for c in corners) // 4,
        sum(c[2] for c in corners) // 4,
    )

    mask = Image.new("L", (width, height), 255)
    mask_pixels = mask.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(1, height - 1):
        queue.append((0, y))
        queue.append((width - 1, y))

    while queue:
        x, y = queue.popleft()
        idx = y * width + x
        if visited[idx]:
            continue
        visited[idx] = 1

        if not _close_to_color(pixels[x, y], bg, tolerance):
            continue

        mask_pixels[x, y] = 0
        if x > 0:
            queue.append((x - 1, y))
        if x < width - 1:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y < height - 1:
            queue.append((x, y + 1))

    rgba.putalpha(mask)
    alpha_bbox = rgba.getchannel("A").getbbox()
    if not alpha_bbox:
        raise ValueError("Could not isolate icon from background.")
    return rgba.crop(alpha_bbox)


def _center_on_canvas(image: Image.Image, size: int = CANVAS_SIZE, padding: float = ICON_PADDING) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    max_side = int(round(size * (1 - (padding * 2))))
    scale = min(max_side / image.width, max_side / image.height)
    scaled = image.resize((int(round(image.width * scale)), int(round(image.height * scale))), Image.Resampling.LANCZOS)
    x = (size - scaled.width) // 2
    y = (size - scaled.height) // 2
    canvas.alpha_composite(scaled, (x, y))
    return canvas


def _build_curved_star(size: int) -> Image.Image:
    star = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(star)
    cx = size // 2
    cy = size // 2

    arm_len = int(size * 0.68)
    arm_w = int(size * 0.21)
    radius = arm_w // 2

    draw.rounded_rectangle(
        (cx - arm_w // 2, cy - arm_len // 2, cx + arm_w // 2, cy + arm_len // 2),
        radius=radius,
        fill=(236, 241, 249, 255),
    )
    draw.rounded_rectangle(
        (cx - arm_len // 2, cy - arm_w // 2, cx + arm_len // 2, cy + arm_w // 2),
        radius=radius,
        fill=(236, 241, 249, 255),
    )
    star = star.rotate(45, resample=Image.Resampling.BICUBIC)

    draw = ImageDraw.Draw(star)
    core = int(size * 0.11)
    draw.ellipse((cx - core, cy - core, cx + core, cy + core), fill=(243, 196, 117, 255))
    return star


def _add_center_emblem(image: Image.Image) -> Image.Image:
    icon = image.copy()
    star_size = int(CANVAS_SIZE * 0.28)
    star = _build_curved_star(star_size)
    x = (CANVAS_SIZE - star_size) // 2
    y = int(CANVAS_SIZE * 0.54) - (star_size // 2)

    shadow = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse(
        (
            x + int(star_size * 0.18),
            y + int(star_size * 0.64),
            x + int(star_size * 0.82),
            y + int(star_size * 0.98),
        ),
        fill=(12, 42, 97, 48),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(max(2, CANVAS_SIZE // 90)))
    icon.alpha_composite(shadow)
    icon.alpha_composite(star, (x, y))
    return icon


def build_icon() -> Image.Image:
    if not SOURCE_ICON.exists():
        raise FileNotFoundError(f"Missing source icon: {SOURCE_ICON}")

    source = Image.open(SOURCE_ICON)
    cutout = _remove_flat_background(source)
    centered = _center_on_canvas(cutout)
    return _add_center_emblem(centered)


def export_icon() -> None:
    icon = build_icon()
    icon.save(APP_ICON_PNG)
    icon.save(APP_ICON_ICO, format="ICO", sizes=ICO_SIZES)
    print(f"Generated {APP_ICON_PNG} and {APP_ICON_ICO} from {SOURCE_ICON}")


if __name__ == "__main__":
    export_icon()
