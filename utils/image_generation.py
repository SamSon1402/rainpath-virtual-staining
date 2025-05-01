"""
Synthetic image generation utilities for the RainPath Virtual Staining application.

This module provides functions to generate synthetic tissue images for demonstration
and testing purposes. These synthetic images simulate different tissue types and
structures that would be found in real histopathology samples.
"""

import numpy as np
import os
from PIL import Image, ImageFilter, ImageEnhance
import random


def generate_synthetic_tissue(size=(400, 400), tissue_type="normal", seed=None):
    """
    Generate synthetic tissue image for demonstration.
    
    Parameters:
    -----------
    size : tuple(int, int)
        Size of the output image in pixels (width, height)
    tissue_type : str
        Type of tissue to generate: "normal", "tumor", or "fibrotic"
    seed : int, optional
        Random seed for reproducibility
        
    Returns:
    --------
    PIL.Image
        RGB image of synthetic tissue
    """
    # Set random seed if provided
    if seed is not None:
        np.random.seed(seed)
    
    # Different patterns based on tissue type
    if tissue_type == "normal":
        # Normal tissue has more regular patterns
        base = np.random.rand(size[0], size[1])
        # Add some structure (cell-like patterns)
        x, y = np.meshgrid(np.linspace(0, 20, size[0]), np.linspace(0, 20, size[1]))
        cells = np.sin(x) * np.cos(y) * 0.2 + 0.3
        tissue = (base * 0.4 + cells).clip(0, 1)
        
    elif tissue_type == "tumor":
        # Tumor tissue has more irregular, denser patterns
        base = np.random.rand(size[0], size[1])
        # Add irregular structures
        x, y = np.meshgrid(np.linspace(0, 30, size[0]), np.linspace(0, 30, size[1]))
        cells = np.sin(x*0.7) * np.sin(y*0.9) * 0.3 + 0.4
        tissue = (base * 0.5 + cells).clip(0, 1)
        
    elif tissue_type == "fibrotic":
        # Fibrotic tissue has more linear structures
        base = np.random.rand(size[0], size[1]) * 0.3
        # Add linear structures
        x, y = np.meshgrid(np.linspace(0, 15, size[0]), np.linspace(0, 15, size[1]))
        fibers = (np.sin(x) + np.cos(y)) * 0.25 + 0.4
        tissue = (base + fibers).clip(0, 1)

    elif tissue_type == "necrotic":
        # Necrotic tissue has fragmented, irregular structures
        base = np.random.rand(size[0], size[1]) * 0.5
        # Add fragmented structures
        x, y = np.meshgrid(np.linspace(0, 40, size[0]), np.linspace(0, 40, size[1]))
        debris = np.sin(x*1.5) * np.cos(y*0.8) * 0.3 + 0.2
        # Add noise to represent cellular debris
        noise = np.random.rand(size[0], size[1]) * 0.4
        tissue = (base + debris + noise).clip(0, 1)
        
    else:  # Default case
        tissue = np.random.rand(size[0], size[1])
    
    # Convert to PIL Image
    img_array = (tissue * 255).astype(np.uint8)
    img = Image.fromarray(img_array)
    
    # Convert to RGB
    img = img.convert('RGB')
    
    # Add some texture and blur to make it more realistic
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    
    return img


def create_tissue_dataset(output_dir, count=10, tissue_types=None, size=(400, 400)):
    """
    Create a dataset of synthetic tissue images.
    
    Parameters:
    -----------
    output_dir : str
        Directory to save images to
    count : int
        Number of images to generate per tissue type
    tissue_types : list(str), optional
        List of tissue types to generate. If None, generates all types
    size : tuple(int, int)
        Size of images to generate
        
    Returns:
    --------
    dict
        Dictionary with paths to generated images by tissue type
    """
    if tissue_types is None:
        tissue_types = ["normal", "tumor", "fibrotic", "necrotic"]
    
    # Create directories if they don't exist
    for tissue_type in tissue_types:
        os.makedirs(os.path.join(output_dir, tissue_type), exist_ok=True)
    
    # Generate and save images
    dataset = {tissue_type: [] for tissue_type in tissue_types}
    
    for tissue_type in tissue_types:
        for i in range(count):
            # Generate random seed for reproducibility
            seed = random.randint(0, 10000)
            
            # Generate tissue image
            img = generate_synthetic_tissue(size=size, tissue_type=tissue_type, seed=seed)
            
            # Save image
            filename = f"{tissue_type}_{i+1:03d}.png"
            filepath = os.path.join(output_dir, tissue_type, filename)
            img.save(filepath)
            
            # Add to dataset
            dataset[tissue_type].append(filepath)
    
    return dataset


def apply_noise_and_artifacts(img, artifact_level=0.2):
    """
    Apply realistic noise and artifacts to a synthetic tissue image.
    
    Parameters:
    -----------
    img : PIL.Image
        Input image
    artifact_level : float
        Level of artifacts to add (0.0 to 1.0)
        
    Returns:
    --------
    PIL.Image
        Image with added noise and artifacts
    """
    # Convert to numpy array
    img_array = np.array(img)
    
    # Add random noise
    noise = np.random.normal(0, 15, img_array.shape).astype(np.int16)
    noisy_img = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Add some blur artifacts in random spots
    if artifact_level > 0:
        noisy_img = Image.fromarray(noisy_img)
        
        # Random blur artifacts
        if random.random() < artifact_level:
            blur_size = random.randint(20, 100)
            blur_x = random.randint(0, img.width - blur_size)
            blur_y = random.randint(0, img.height - blur_size)
            
            # Create a mask for blurring only a region
            mask = Image.new('L', img.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((blur_x, blur_y, blur_x + blur_size, blur_y + blur_size), 
                             fill=255)
            
            # Apply blur
            blurred = noisy_img.filter(ImageFilter.GaussianBlur(radius=3))
            noisy_img = Image.composite(blurred, noisy_img, mask)
        
        # Random brightness artifacts
        if random.random() < artifact_level:
            enhancer = ImageEnhance.Brightness(noisy_img)
            factor = random.uniform(0.7, 1.3)
            noisy_img = enhancer.enhance(factor)
        
        return noisy_img
    else:
        return Image.fromarray(noisy_img)


# If module is run directly, generate some example images
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    # Test generation of different tissue types
    tissue_types = ["normal", "tumor", "fibrotic", "necrotic"]
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten()
    
    for i, tissue_type in enumerate(tissue_types):
        img = generate_synthetic_tissue(tissue_type=tissue_type, seed=42)
        axes[i].imshow(img)
        axes[i].set_title(f"{tissue_type.capitalize()} Tissue")
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.savefig("synthetic_tissue_examples.png")
    plt.close()
    
    print("Generated example images of synthetic tissues.")