from launchpad import Launchpad
import sys
import time
import argparse
from PIL import Image, ImageSequence

lp = Launchpad()

# helpers
def set_led(row, col, colour):
    # toprow
    if row == 0 and col < 8:
        lp.set_top_led(col, colour)

    # right column
    elif col == 8 and row > 0:
        lp.set_right_led(row - 1, colour)

    # main grid
    elif row > 0 and col < 8:
        lp.set_grid_led(row - 1, col, colour)

# rgb value approximations for interpolation
PALETTE = {
    "black": (0, 0, 0),

    "red_low": (85, 0, 0),
    "red_med": (170, 0, 0),
    "red_max": (255, 0, 0),

    "green_low": (0, 85, 0),
    "green_med": (0, 170, 0),
    "green_max": (0, 255, 0),

    "yellow_low": (85, 85, 0),
    "yellow_med": (170, 170, 0),
    "yellow_max": (255, 255, 0),
}

def palette_for_mode(mode):
    if mode == "red":
        return {k: v for k, v in PALETTE.items() if "red" in k or k == "black"}
    if mode == "green":
        return {k: v for k, v in PALETTE.items() if "green" in k or k == "black"}
    if mode == "yellow":
        return {k: v for k, v in PALETTE.items() if "yellow" in k or k == "black"}
    return PALETTE

# approximate closest colour from the very limited colour selection
def closest_colour(rgb, palette):
    r, g, b = rgb

    best = None
    best_dist = 1e9

    # magic
    for name, (pr, pg, pb) in palette.items():
        d = (r-pr)**2 + (g-pg)**2 + (b-pb)**2
        if d < best_dist:
            best_dist = d
            best = name

    return best

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("gif") # file location
    parser.add_argument("-fps", type=float, default=None) # fps to run at
    parser.add_argument(
        "-m",
        "--mode",
        default="full",
        choices=["full", "red", "green", "yellow"]
    ) # colours to be used
    return parser.parse_args()

# convert image to 9x9 and create an array of arrays
def load_frames(path):
    img = Image.open(path)

    frames = []
    for frame in ImageSequence.Iterator(img):
        f = frame.convert("RGB")
        f = f.resize((9, 9), Image.BILINEAR)
        frames.append(f)

    return frames, img

# go through the input array and write every pixel one by one
def render_frame(frame, palette):
    px = frame.load()

    for row in range(9):
        for col in range(9):
            rgb = px[col, row]
            colour = closest_colour(rgb, palette)
            set_led(row, col, colour)

def main():
    args = parse_args()

    print("loading gif")
    frames, img = load_frames(args.gif)
    print("image loaded")
    
    if args.fps:
        fps = args.fps
    else: # if no fps provided, use fps from metadata
        duration = img.info.get("duration", 100)
        fps = 1000 / duration if duration > 0 else 10

    delay = 1.0 / fps
    
    palette = palette_for_mode(args.mode)

    print("running")
    # the main drawing loop
    while True:
        for frame in frames:
            render_frame(frame, palette)
            time.sleep(delay)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("please provide gif file path as an argument\n")
        exit()

    try:
        print("ctrl + c to exit")
        main()
    except KeyboardInterrupt:
        for row in range(9):
            for col in range(9):
                set_led(row, col, "black")
        print("\nctrl+c exit")
    except Exception as e:
        print(f"\nexception!!! {e}")
