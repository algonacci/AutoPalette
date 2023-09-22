import base64
from io import BytesIO
from typing import Tuple
import matplotlib


import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request
from PIL import Image
import requests
from sklearn.cluster import KMeans

matplotlib.use("agg")  # Set the backend to non-interactive

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files["image"].read()
        uploaded_image = base64.b64encode(
            image).decode()  # Convert to base64
        img = Image.open(BytesIO(image))
        num_colors = 8
        color_palette, color_palette_hex = get_palette(img, num_colors)

        color_palette_hex.sort(reverse=True)

        palette_image_base64 = get_palette_image(color_palette)

        return render_template(
            "index.html",
            color_palette=color_palette,
            color_palette_hex=color_palette_hex,
            palette_image_base64=palette_image_base64,
            uploaded_image=uploaded_image
        )

    return render_template("index.html")


def get_palette_image(color_palette):
    color_palette_sorted = np.array(
        sorted(color_palette, key=lambda x: x.mean())[::-1])

    plt.imshow(color_palette_sorted[np.newaxis, :, :])
    plt.axis("off")
    palette_image_path = "static/palette_image.png"
    plt.savefig(palette_image_path, bbox_inches="tight",
                pad_inches=0, format="png")
    plt.close()

    with open(palette_image_path, "rb") as img_file:
        palette_image_base64 = base64.b64encode(img_file.read()).decode()

    return palette_image_base64


def load_image(path: str) -> np.ndarray:
    if path.startswith(("http://", "https://")):
        response = requests.get(path)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(path)
    return img


def get_palette(
    img: Image, n_colors: int, resize_shape: Tuple[int, int] = (100, 100)
) -> np.ndarray:
    img = np.asarray(img.resize(resize_shape)) / 255.0
    h, w, c = img.shape
    img_arr = img.reshape(h * w, c)
    kmeans = KMeans(n_clusters=n_colors, n_init="auto").fit(img_arr)
    palette_rgb = (kmeans.cluster_centers_ * 255).astype(int)
    palette_hex = [matplotlib.colors.rgb2hex(
        color) for color in palette_rgb/255]
    return palette_rgb, palette_hex


@app.errorhandler(500)
def internal_server_error(error):
    return "Mohon Bersabar, Coba Lagi"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
