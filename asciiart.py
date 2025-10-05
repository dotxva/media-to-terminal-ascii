import sys
from PIL import Image
import os
import cv2
import time

path_to_media = sys.argv[1]
image_types = ['jpg', 'jpeg', 'png']
video_types = ['mp4', 'webm', 'avi', 'mov']

def print_frame(img):
    target_width = 100
    target_height = 100

    imgw, imgh = img.size

    w = target_width
    h = int(imgh * (w / imgw) * 0.5)

    img = img.resize((w, h))
    colored_pixels = list(img.getdata())
    img = img.convert("L")

    pixels = list(img.getdata())

    pixels_and_coloreds = list(zip(pixels, colored_pixels))

    ascii_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^'. "

    def calculate_char_index(brightness):
        return int(brightness / 255 * (len(ascii_chars) - 1))

    os.system("")
    os.system("cls")

    for i in range(h):
        image_pixel_row = pixels_and_coloreds[i * w:(i + 1) * w]
        for pixel in image_pixel_row:
            print(
                f"\033[38;2;{pixel[1][0]};{pixel[1][1]};{pixel[1][2]}m{ascii_chars[calculate_char_index(pixel[0])]}\033[0m",
                end="")
        print("")


if path_to_media.split('.')[-1].lower() in image_types:
    image = Image.open(path_to_media)
    print_frame(image)
elif path_to_media.split('.')[-1].lower() in video_types:
    video = cv2.VideoCapture(path_to_media)
    fps = video.get(cv2.CAP_PROP_FPS)
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        print_frame(pil_image)
        time.sleep(1/(4*fps))
elif path_to_media.split('.')[-1].lower() == "gif":
    gif = Image.open(path_to_media)
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_rgb = gif.convert("RGB")
        print_frame(frame_rgb)
        delay = gif.info.get('duration', 100) / 1000
        time.sleep(delay)
else:
    print("media type not supported.")
