"""
Utility functions for the RainPath Virtual Staining application.

This package contains modules for:
- Synthetic image generation for tissue samples
- Virtual staining algorithms
- Performance metrics calculation
"""

# Import key functions for easy access
from .image_generation import (
    generate_synthetic_tissue,
    create_tissue_dataset
)

from .staining import (
    apply_virtual_stain,
    get_stain_description,
    get_stain_matrix,
    stain_normalization
)

from .metrics import (
    calculate_metrics,
    calculate_ssim,
    calculate_color_accuracy,
    calculate_nuclei_detection_accuracy,
    calculate_edge_preservation
)

__all__ = [
    'generate_synthetic_tissue',
    'create_tissue_dataset',
    'apply_virtual_stain',
    'get_stain_description',
    'get_stain_matrix',
    'stain_normalization',
    'calculate_metrics',
    'calculate_ssim',
    'calculate_color_accuracy',
    'calculate_nuclei_detection_accuracy',
    'calculate_edge_preservation'
]