import base64
from io import BytesIO
from typing import Tuple
import matplotlib


import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request, jsonify
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


@app.route("/api", methods=["POST"])
def api_generate_palette():
    if request.method == "POST":
        image = request.files["image"].read()
        img = Image.open(BytesIO(image))
        num_colors = 8
        color_palette, color_palette_hex = get_palette(img, num_colors)

        color_palette_hex.sort(reverse=True)

        _, palette_image_path = get_palette_image(color_palette)

        return jsonify({
            "palette_image_path": f"https://{request.host}/{palette_image_path}",
            "color_palette": color_palette.tolist(),
            "color_palette_hex": color_palette_hex,
        }), 200


@app.route("/tritone", methods=["POST"])
def tritone():
    if request.method == "POST":
        image = request.files["image"].read()
        uploaded_image = base64.b64encode(image).decode()
        img = Image.open(BytesIO(image))
        
        tritone_img = apply_tritone(img)
        
        # Save tritone image
        tritone_buffer = BytesIO()
        tritone_img.save(tritone_buffer, format='PNG')
        tritone_base64 = base64.b64encode(tritone_buffer.getvalue()).decode()
        
        # Define tritone colors for display
        tritone_colors = ["#0f0e83", "#e44c9a", "#00aa13"]  # Resistance Blue, Brave Pink, Hero Green
        
        return render_template(
            "index.html",
            uploaded_image=uploaded_image,
            tritone_image=tritone_base64,
            tritone_colors=tritone_colors
        )


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

    return palette_image_base64, palette_image_path


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


def apply_tritone(img: Image) -> Image:
    # Define the three tritone colors
    resistance_blue = np.array([15, 14, 131])
    brave_pink = np.array([228, 76, 154])  # #e44c9a
    hero_green = np.array([0, 170, 19])    # #00aa13
    
    # Convert image to numpy array
    img_array = np.array(img)
    original_shape = img_array.shape
    
    # Convert to grayscale to get luminance values
    if len(img_array.shape) == 3:
        grayscale = np.dot(img_array[...,:3], [0.299, 0.587, 0.114])
    else:
        grayscale = img_array
    
    # Normalize grayscale values to 0-1
    grayscale_norm = grayscale / 255.0
    
    # Create output array
    tritone_img = np.zeros((original_shape[0], original_shape[1], 3), dtype=np.uint8)
    
    # Map grayscale values to tritone colors
    # Dark areas (0-0.33) -> Resistance Blue
    # Mid areas (0.33-0.67) -> Brave Pink  
    # Light areas (0.67-1.0) -> Hero Green
    
    dark_mask = grayscale_norm <= 0.33
    mid_mask = (grayscale_norm > 0.33) & (grayscale_norm <= 0.67)
    light_mask = grayscale_norm > 0.67
    
    # For smoother transitions, blend colors based on luminance within each range
    for i in range(original_shape[0]):
        for j in range(original_shape[1]):
            lum = grayscale_norm[i, j]
            
            if lum <= 0.33:
                # Blend from black to resistance blue
                blend_factor = lum / 0.33
                tritone_img[i, j] = resistance_blue * blend_factor
            elif lum <= 0.67:
                # Blend from resistance blue to brave pink
                blend_factor = (lum - 0.33) / 0.34
                tritone_img[i, j] = resistance_blue * (1 - blend_factor) + brave_pink * blend_factor
            else:
                # Blend from brave pink to hero green
                blend_factor = (lum - 0.67) / 0.33
                tritone_img[i, j] = brave_pink * (1 - blend_factor) + hero_green * blend_factor
    
    return Image.fromarray(tritone_img)


@app.errorhandler(500)
def internal_server_error(error):
    return "Mohon Bersabar, Coba Lagi"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
