import os
import cv2
import numpy as np
from scipy.fftpack import dct
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model


def extract_color_layout(image_path: str, grid_size: int = 8) -> np.ndarray:
    """
    Extract MPEG-7 Color Layout features from image.

    Args:
        image_path (str): Path to the input image.
        grid_size (int): Grid size to divide image (default 8x8).

    Returns:
        np.ndarray: First 6 DCT coefficients from color layout.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Unable to read image file: {image_path}")

    img = cv2.resize(img, (256, 256))
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

    # Split image into grid_size x grid_size blocks
    grid_rows = np.array_split(ycrcb, grid_size, axis=0)
    grid_blocks = [np.array_split(row, grid_size, axis=1) for row in grid_rows]

    features = []
    for row_blocks in grid_blocks:
        for block in row_blocks:
            avg_y = np.mean(block[:, :, 0])
            avg_cr = np.mean(block[:, :, 1])
            avg_cb = np.mean(block[:, :, 2])
            features.extend([avg_y, avg_cr, avg_cb])

    # Apply DCT and take first 6 coefficients
    dct_coeffs = dct(features, norm='ortho')[:6]
    dct_min, dct_max = np.min(dct_coeffs), np.max(dct_coeffs)
    dct_coeffs = (dct_coeffs - dct_min) / (dct_max - dct_min + 1e-8)
    
    return dct_coeffs[:6]




# Khởi tạo mô hình VGG16 với GlobalAveragePooling2D
vgg_model = None
if vgg_model is None:
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)  # Giảm kích thước từ (7, 7, 512) xuống (512,)
    vgg_model = Model(inputs=base_model.input, outputs=x)




def extract_vgg_feature(img_path: str) -> np.ndarray:
    """
    Extract 512-dim VGG16 feature vector from image.

    Args:
        img_path (str): Path to the input image.

    Returns:
        np.ndarray: Flattened VGG16 feature vector of shape (512,).
    """
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image not found: {img_path}")

    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = preprocess_input(x)
    x = np.expand_dims(x, axis=0)
 
    features = vgg_model.predict(x)
    return features.flatten()

    
def extract_vgg_feature_batch(img_paths: list) -> np.ndarray:
    imgs = [image.load_img(p, target_size=(224, 224)) for p in img_paths]
    x = np.array([image.img_to_array(img) for img in imgs])
    x = preprocess_input(x)

    features = vgg_model.predict(x)
    return features.reshape(len(img_paths), -1)