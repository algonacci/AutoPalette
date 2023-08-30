import base64
import os
from io import BytesIO
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, jsonify, render_template, request
from PIL import Image
from sklearn.cluster import KMeans

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files["image"].read()
        img = Image.open(BytesIO(image))
        num_colors = 8
        color_palette, kmeans = get_palette(img, num_colors)

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

        return render_template(
            "index.html",
            color_palette=color_palette,
            palette_image_base64=palette_image_base64
        )

    return render_template("index.html")


def image_to_base64(image):
    image_pil = Image.fromarray((image * 255).astype(np.uint8))
    if image_pil.mode == "RGBA":
        image_pil = image_pil.convert("RGB")
    buffer = BytesIO()
    image_pil.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()


def load_image(path: str) -> np.ndarray:
    if path.startswith(("http://", "https://")):
        response = requests.get(path)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(path)
    return img


def get_palette(
    img: Image, n_colors: int, resize_shape: Tuple[int, int] = (100, 100)
) -> Tuple[np.ndarray, KMeans]:
    img = np.asarray(img.resize(resize_shape)) / 255.0
    h, w, c = img.shape
    img_arr = img.reshape(h * w, c)
    kmeans = KMeans(n_clusters=n_colors, n_init="auto").fit(img_arr)
    palette = (kmeans.cluster_centers_ * 255).astype(int)
    return palette, kmeans


def quantize_image(image: Image, kmeans: KMeans) -> np.ndarray:
    image_np = np.asarray(image) / 255.0
    h, w, c = image_np.shape
    flatten = image_np.reshape(h * w, c)
    pixel_rgb_clusters = kmeans.predict(flatten)
    image_quantized = kmeans.cluster_centers_[pixel_rgb_clusters]
    return image_quantized.reshape(h, w, c)


if __name__ == "__main__":
    app.run(debug=False,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)))
