"""
Virtual staining algorithms for the RainPath Virtual Staining application.

This module provides functions to apply virtual staining effects to tissue images,
simulating the appearance of different histochemical stains used in pathology.
"""

import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def apply_virtual_stain(img, stain_type="H&E", intensity=0.8, contrast=1.2):
    """
    Apply virtual staining effect to the image.
    
    Parameters:
    -----------
    img : PIL.Image
        Input image (unstained/raw tissue)
    stain_type : str
        Type of stain to apply: "H&E", "Masson's Trichrome", "PAS", etc.
    intensity : float
        Intensity of the stain (0.5 to 1.5)
    contrast : float
        Contrast adjustment (0.5 to 2.0)
        
    Returns:
    --------
    PIL.Image
        Virtually stained image
    """
    # Convert PIL image to numpy array for processing
    img_array = np.array(img)
    
    # Different staining based on type
    if stain_type == "H&E":
        # Create H&E-like coloring
        # Hematoxylin (purplish-blue for nuclei)
        hematoxylin = img_array.copy() / 255.0
        hematoxylin = 1 - hematoxylin  # Invert
        
        # Eosin (pinkish for cytoplasm)
        eosin = img_array.copy() / 255.0
        
        # Combine: R channel gets more eosin, B channel gets more hematoxylin
        stained = np.zeros_like(img_array)
        stained[:,:,0] = ((eosin[:,:,0] * 0.7 + 0.3) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Red
        stained[:,:,1] = ((eosin[:,:,1] * 0.5 + hematoxylin[:,:,1] * 0.5) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Green
        stained[:,:,2] = ((hematoxylin[:,:,2] * 0.7 + 0.3) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Blue
        
    elif stain_type == "Masson's Trichrome":
        # Create Masson's Trichrome-like coloring (blue for collagen, red for muscle/cytoplasm)
        base = img_array.copy() / 255.0
        inverted = 1 - base  # Invert
        
        # Combine channels for trichrome effect
        stained = np.zeros_like(img_array)
        stained[:,:,0] = ((base[:,:,0] * 0.8 + 0.2) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Red
        stained[:,:,1] = ((base[:,:,1] * 0.5) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Green
        stained[:,:,2] = ((inverted[:,:,2] * 0.8) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Blue
        
    elif stain_type == "PAS":
        # Create Periodic acid–Schiff-like coloring (magenta for glycogen, mucus)
        base = img_array.copy() / 255.0
        
        # Combine channels for PAS effect (magenta)
        stained = np.zeros_like(img_array)
        stained[:,:,0] = ((base[:,:,0] * 0.9 + 0.1) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Red
        stained[:,:,1] = ((base[:,:,1] * 0.4) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Green
        stained[:,:,2] = ((base[:,:,2] * 0.7 + 0.3) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Blue
    
    elif stain_type == "Silver":
        # Create silver stain effect (black/brown for reticulin fibers)
        base = img_array.copy() / 255.0
        inverted = 1 - base  # Invert for silver effect
        
        # Calculate a gray value for silver effect
        gray = 0.3 * inverted[:,:,0] + 0.59 * inverted[:,:,1] + 0.11 * inverted[:,:,2]
        
        # Apply sepia tone for silver stain effect
        stained = np.zeros_like(img_array)
        stained[:,:,0] = ((gray * 0.9) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Red
        stained[:,:,1] = ((gray * 0.7) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Green
        stained[:,:,2] = ((gray * 0.5) * 255 * intensity).clip(0, 255).astype(np.uint8)  # Blue
    
    elif stain_type == "Congo Red":
        # Create Congo Red stain effect (red for amyloid)
        base = img_array.copy() / 255.0
        
        # Apply red coloring
        stained = np.zeros_like(img_array)
        stained[:,:,0] = ((1 - base[:,:,0]) * 0.9 + 0.1) * 255 * intensity  # Red
        stained[:,:,1] = ((1 - base[:,:,1]) * 0.3) * 255 * intensity  # Green
        stained[:,:,2] = ((1 - base[:,:,2]) * 0.3) * 255 * intensity  # Blue
        stained = stained.clip(0, 255).astype(np.uint8)
        
    else:  # Default grayscale
        stained = img_array
    
    # Convert back to PIL image
    result = Image.fromarray(stained)
    
    # Apply contrast adjustment
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(result)
        result = enhancer.enhance(contrast)
        
    return result


def get_stain_description(stain_type):
    """
    Return description for different stain types.
    
    Parameters:
    -----------
    stain_type : str
        The type of stain
        
    Returns:
    --------
    str
        Description of the stain
    """
    descriptions = {
        "H&E": "Hematoxylin & Eosin stain highlights cell nuclei in blue-purple and cytoplasm in pink. It's the most common stain used in histology.",
        "Masson's Trichrome": "This stain shows collagen fibers in blue, nuclei in black, and cytoplasm/muscle in red. Useful for identifying fibrotic tissue.",
        "PAS": "Periodic acid–Schiff stain highlights structures containing glycogen, mucus and basement membranes in magenta. Used to identify certain fungal infections and kidney conditions.",
        "Silver": "Silver stains are used to visualize reticulin fibers, basement membranes, and certain microorganisms. They appear black or dark brown against a lighter background.",
        "Congo Red": "Congo Red stain is used to identify amyloid deposits, which appear red-orange. Under polarized light, amyloid shows apple-green birefringence."
    }
    return descriptions.get(stain_type, "No description available.")


def get_stain_matrix(stain_type):
    """
    Get the normalized stain matrix for the specified stain type.
    This represents the RGB absorption characteristics of the stain.
    
    Parameters:
    -----------
    stain_type : str
        Type of stain
        
    Returns:
    --------
    numpy.ndarray
        2x3 matrix representing the stain's RGB absorption characteristics
    """
    # Define stain matrices for common stains
    # Values are normalized RGB absorption coefficients
    stain_matrices = {
        "H&E": np.array([
            [0.65, 0.70, 0.29],  # Hematoxylin
            [0.07, 0.99, 0.11]   # Eosin
        ]),
        "Masson's Trichrome": np.array([
            [0.25, 0.15, 0.80],  # Aniline Blue (collagen)
            [0.80, 0.15, 0.15]   # Biebrich Scarlet-Acid Fuchsin (cytoplasm)
        ]),
        "PAS": np.array([
            [0.85, 0.27, 0.57],  # PAS positive (magenta)
            [0.10, 0.10, 0.80]   # Hematoxylin (counterstain)
        ]),
        "Silver": np.array([
            [0.33, 0.33, 0.33],  # Silver (grayscale)
            [0.00, 0.00, 0.00]   # No second stain
        ]),
        "Congo Red": np.array([
            [0.90, 0.20, 0.30],  # Congo Red
            [0.20, 0.20, 0.80]   # Hematoxylin (counterstain)
        ])
    }
    
    return stain_matrices.get(stain_type, np.array([[0.33, 0.33, 0.33], [0.33, 0.33, 0.33]]))


def stain_normalization(source_image, target_image, stain_type="H&E"):
    """
    Normalize the staining of the source image to match the target image.
    
    Parameters:
    -----------
    source_image : PIL.Image
        The image to be normalized
    target_image : PIL.Image
        The reference image with desired staining
    stain_type : str
        Type of stain used
        
    Returns:
    --------
    PIL.Image
        Normalized image
    """
    # Convert images to numpy arrays
    source = np.array(source_image).astype(np.float32) / 255.0
    target = np.array(target_image).astype(np.float32) / 255.0
    
    # Basic color normalization (mean and std adjustment)
    # This is a simplified version of stain normalization
    
    # For each channel, normalize the source to match target statistics
    normalized = np.zeros_like(source)
    
    for i in range(3):  # RGB channels
        src_channel = source[:,:,i]
        tgt_channel = target[:,:,i]
        
        # Calculate statistics
        src_mean, src_std = np.mean(src_channel), np.std(src_channel)
        tgt_mean, tgt_std = np.mean(tgt_channel), np.std(tgt_channel)
        
        # Normalize
        if src_std > 0:
            normalized[:,:,i] = ((src_channel - src_mean) / src_std) * tgt_std + tgt_mean
        else:
            normalized[:,:,i] = tgt_mean
    
    # Clip values to valid range
    normalized = np.clip(normalized, 0, 1)
    
    # Convert back to PIL image
    normalized_image = Image.fromarray((normalized * 255).astype(np.uint8))
    
    return normalized_image


def display_stain_comparison(unstained_image, stain_types=None):
    """
    Display a comparison of different stains applied to the same image.
    
    Parameters:
    -----------
    unstained_image : PIL.Image
        The unstained image to apply virtual stains to
    stain_types : list(str), optional
        List of stain types to apply. If None, uses default set
        
    Returns:
    --------
    matplotlib.figure.Figure
        Figure with the comparison
    """
    if stain_types is None:
        stain_types = ["H&E", "Masson's Trichrome", "PAS", "Silver", "Congo Red"]
    
    # Create figure
    fig, axes = plt.subplots(1, len(stain_types) + 1, figsize=(4 * (len(stain_types) + 1), 4))
    
    # Display original image
    axes[0].imshow(unstained_image)
    axes[0].set_title("Unstained")
    axes[0].axis('off')
    
    # Apply and display each stain
    for i, stain_type in enumerate(stain_types):
        stained = apply_virtual_stain(unstained_image, stain_type=stain_type)
        axes[i+1].imshow(stained)
        axes[i+1].set_title(stain_type)
        axes[i+1].axis('off')
    
    plt.tight_layout()
    return fig


# If module is run directly, generate some example stained images
if __name__ == "__main__":
    from image_generation import generate_synthetic_tissue
    
    # Generate a synthetic tissue image
    tissue = generate_synthetic_tissue(tissue_type="normal", seed=42)
    
    # Display stain comparison
    fig = display_stain_comparison(tissue)
    plt.savefig("stain_comparison.png")
    plt.close()
    
    print("Generated example stained images.")