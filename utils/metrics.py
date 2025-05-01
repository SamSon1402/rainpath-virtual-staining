"""
Performance metrics calculation for the RainPath Virtual Staining application.

This module provides functions to calculate various metrics for evaluating the
quality of virtually stained images compared to reference stained images.
"""

import numpy as np
from PIL import Image, ImageFilter
import random
from scipy.ndimage import gaussian_filter

def calculate_metrics(original, stained, model_quality=0.85):
    """
    Calculate synthetic metrics for model evaluation.
    
    Parameters:
    -----------
    original : PIL.Image
        Original unstained image
    stained : PIL.Image
        Virtually stained image
    model_quality : float
        Base quality factor to simulate model performance (0.0 to 1.0)
        
    Returns:
    --------
    dict
        Dictionary of calculated metrics
    """
    # For MVP, we'll generate some plausible metrics
    # In a real app, these would be calculated from actual model outputs
    
    # Add some random variation but keep metrics generally aligned with model_quality
    variation = 0.1
    
    metrics = {
        "Structural Similarity": calculate_ssim(original, stained, model_quality),
        "Color Accuracy": calculate_color_accuracy(original, stained, model_quality),
        "Nuclei Detection": calculate_nuclei_detection_accuracy(original, stained, model_quality),
        "Edge Preservation": calculate_edge_preservation(original, stained, model_quality),
        "Overall Quality": model_quality
    }
    
    # Ensure metrics are in valid range
    for key in metrics:
        metrics[key] = max(0, min(1, metrics[key]))
        
    return metrics


def calculate_ssim(original, stained, base_quality=0.85):
    """
    Calculate a synthetic Structural Similarity Index (SSIM) for demonstration.
    
    In a real implementation, this would use skimage.metrics.structural_similarity
    or a similar function to calculate actual SSIM between ground truth and 
    virtually stained images.
    
    Parameters:
    -----------
    original : PIL.Image
        Original unstained image
    stained : PIL.Image
        Virtually stained image
    base_quality : float
        Base quality factor to simulate model performance
        
    Returns:
    --------
    float
        Simulated SSIM score (0.0 to 1.0)
    """
    # Add some randomness based on image characteristics
    orig_array = np.array(original.convert('L'))
    stained_array = np.array(stained.convert('L'))
    
    # Use edge detection to estimate structural complexity
    orig_edges = np.array(original.convert('L').filter(ImageFilter.FIND_EDGES))
    edge_density = np.mean(orig_edges) / 255.0
    
    # More complex images (more edges) tend to have lower SSIM
    complexity_factor = 1.0 - (edge_density * 0.3)
    
    # Simulate an SSIM calculation
    variation = 0.1
    ssim = base_quality * complexity_factor * (1 + random.uniform(-variation, variation))
    
    return max(0, min(1, ssim))


def calculate_color_accuracy(original, stained, base_quality=0.85):
    """
    Calculate a synthetic color accuracy metric for demonstration.
    
    Parameters:
    -----------
    original : PIL.Image
        Original unstained image
    stained : PIL.Image
        Virtually stained image
    base_quality : float
        Base quality factor to simulate model performance
        
    Returns:
    --------
    float
        Simulated color accuracy score (0.0 to 1.0)
    """
    # Calculate color distribution in stained image
    stained_array = np.array(stained)
    color_variance = np.std(stained_array.reshape(-1, 3), axis=0).mean() / 255.0
    
    # More color variance generally means better staining distinction
    variance_factor = min(1.0, color_variance * 5)
    
    # Simulate a color accuracy metric
    variation = 0.1
    color_accuracy = base_quality * variance_factor * (1 + random.uniform(-variation, variation))
    
    return max(0, min(1, color_accuracy))


def calculate_nuclei_detection_accuracy(original, stained, base_quality=0.85):
    """
    Calculate a synthetic nuclei detection accuracy metric for demonstration.
    
    Parameters:
    -----------
    original : PIL.Image
        Original unstained image
    stained : PIL.Image
        Virtually stained image
    base_quality : float
        Base quality factor to simulate model performance
        
    Returns:
    --------
    float
        Simulated nuclei detection accuracy score (0.0 to 1.0)
    """
    # Convert to grayscale for analysis
    stained_gray = np.array(stained.convert('L'))
    
    # Apply threshold to identify potential nuclei regions
    # This is a very simplified simulation of nuclei detection
    threshold = 100  # Arbitrary threshold for demo
    potential_nuclei = stained_gray < threshold
    nuclei_density = np.mean(potential_nuclei)
    
    # Adjust based on reasonable nuclei density
    density_factor = 1.0
    if nuclei_density < 0.05:
        # Too few nuclei detected
        density_factor = nuclei_density / 0.05
    elif nuclei_density > 0.3:
        # Too many nuclei detected (likely false positives)
        density_factor = 1.0 - ((nuclei_density - 0.3) / 0.7)
    
    # Simulate nuclei detection accuracy
    variation = 0.15  # Nuclei detection has more variability
    nuclei_accuracy = base_quality * density_factor * (1 + random.uniform(-variation, variation))
    
    return max(0, min(1, nuclei_accuracy))


def calculate_edge_preservation(original, stained, base_quality=0.85):
    """
    Calculate a synthetic edge preservation metric for demonstration.
    
    Parameters:
    -----------
    original : PIL.Image
        Original unstained image
    stained : PIL.Image
        Virtually stained image
    base_quality : float
        Base quality factor to simulate model performance
        
    Returns:
    --------
    float
        Simulated edge preservation score (0.0 to 1.0)
    """
    # Convert to grayscale for edge detection
    orig_gray = np.array(original.convert('L'))
    stained_gray = np.array(stained.convert('L'))
    
    # Apply simple edge detection (gradient magnitude)
    def simple_edge_detection(img):
        # Apply Gaussian filter to reduce noise
        img_smoothed = gaussian_filter(img, sigma=1)
        
        # Compute gradients
        gradient_x = np.gradient(img_smoothed, axis=1)
        gradient_y = np.gradient(img_smoothed, axis=0)
        
        # Compute gradient magnitude
        gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
        
        return gradient_magnitude
    
    # Get edges
    orig_edges = simple_edge_detection(orig_gray)
    stained_edges = simple_edge_detection(stained_gray)
    
    # Calculate edge density
    orig_edge_density = np.mean(orig_edges > 20)  # Arbitrary threshold for demo
    stained_edge_density = np.mean(stained_edges > 20)
    
    # Compare edge densities (should be similar in good staining)
    edge_ratio = min(orig_edge_density, stained_edge_density) / max(orig_edge_density, stained_edge_density)
    if edge_ratio < 0.1:
        edge_ratio = 0.1  # Prevent extreme values
    
    # Simulate edge preservation metric
    variation = 0.1
    edge_preservation = base_quality * edge_ratio * (1 + random.uniform(-variation, variation))
    
    return max(0, min(1, edge_preservation))


def generate_performance_report(metrics, tissue_type, stain_type):
    """
    Generate a performance report based on calculated metrics.
    
    Parameters:
    -----------
    metrics : dict
        Dictionary of calculated metrics
    tissue_type : str
        Type of tissue analyzed
    stain_type : str
        Type of stain applied
        
    Returns:
    --------
    str
        Performance report text
    """
    overall_score = metrics["Overall Quality"]
    quality_level = "High" if overall_score > 0.8 else "Medium" if overall_score > 0.6 else "Low"
    
    # Generate report
    report = f"# Virtual Staining Performance Report\n\n"
    report += f"## Analysis Summary\n"
    report += f"- Tissue Type: {tissue_type.capitalize()}\n"
    report += f"- Stain Type: {stain_type}\n"
    report += f"- Overall Quality: {overall_score:.2f} ({quality_level})\n\n"
    
    report += f"## Detailed Metrics\n"
    for metric, value in metrics.items():
        if metric != "Overall Quality":
            report += f"- {metric}: {value:.2f}\n"
    
    report += f"\n## Recommendations\n"
    
    # Generate recommendations based on the lowest metric
    lowest_metric = min(metrics.items(), key=lambda x: x[1] if x[0] != "Overall Quality" else 1.0)
    
    if lowest_metric[0] == "Structural Similarity":
        report += "- Model struggles with preserving structural details\n"
        report += "- Consider adding more structural constraints to the loss function\n"
        report += "- Increase the weight of structural similarity in training\n"
    
    elif lowest_metric[0] == "Color Accuracy":
        report += "- Color reproduction needs improvement\n"
        report += "- Consider color normalization preprocessing\n"
        report += "- Add color-specific loss terms to the training objective\n"
    
    elif lowest_metric[0] == "Nuclei Detection":
        report += "- Nuclei representation can be enhanced\n"
        report += "- Consider adding a nuclei segmentation auxiliary task\n"
        report += "- Augment training data with nuclei-specific examples\n"
    
    elif lowest_metric[0] == "Edge Preservation":
        report += "- Edge definition needs improvement\n"
        report += "- Add edge-aware loss components\n"
        report += "- Consider multi-scale gradient matching techniques\n"
    
    return report


# If module is run directly, run some example metrics calculations
if __name__ == "__main__":
    from image_generation import generate_synthetic_tissue
    from staining import apply_virtual_stain
    
    # Generate a synthetic tissue image
    tissue = generate_synthetic_tissue(tissue_type="normal", seed=42)
    
    # Apply virtual staining
    stained = apply_virtual_stain(tissue, stain_type="H&E")
    
    # Calculate metrics
    metrics = calculate_metrics(tissue, stained, model_quality=0.85)
    
    # Print metrics
    print("Calculated Metrics:")
    for metric, value in metrics.items():
        print(f"- {metric}: {value:.4f}")
    
    # Generate report
    report = generate_performance_report(metrics, "normal", "H&E")
    print("\nPerformance Report:")
    print(report)