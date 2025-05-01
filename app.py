import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import io
import base64
from matplotlib.colors import LinearSegmentedColormap
import time
import random

# Set page configuration
st.set_page_config(
    page_title="RainPath Virtual Staining",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for retro gaming style
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono:wght@400;700&display=swap');
    
    /* Main styles */
    * {
        font-family: 'Space Mono', monospace;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'VT323', monospace !important;
        text-transform: uppercase;
        color: #FFD700 !important;
        text-shadow: 3px 3px 0px #FF6B6B;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }
    
    h1 {
        font-size: 3.5rem !important;
    }
    
    h2 {
        font-size: 2.5rem !important;
        border-bottom: 4px solid #FFD700;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #2E2E2E;
        background-image: linear-gradient(#3E3E3E, #2E2E2E);
        border-right: 4px solid #FFD700;
    }
    
    /* Cards and sections */
    .stCard {
        border: 4px solid #FFD700;
        border-radius: 0px !important;
        background-color: #3E3E3E !important;
        box-shadow: 8px 8px 0px #FF6B6B !important;
        margin-bottom: 2rem !important;
        padding: 1rem !important;
    }
    
    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        font-family: 'VT323', monospace !important;
        border: 3px solid #FFD700 !important;
        border-radius: 0px !important;
        background-color: #2E2E2E !important;
        color: #FFD700 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 4px 4px 0px #FF6B6B !important;
        transition: all 0.1s ease !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translate(2px, 2px) !important;
        box-shadow: 2px 2px 0px #FF6B6B !important;
    }
    
    .stButton > button:active, .stDownloadButton > button:active {
        transform: translate(4px, 4px) !important;
        box-shadow: 0px 0px 0px #FF6B6B !important;
    }
    
    /* Sliders */
    .stSlider > div > div {
        color: #FFD700 !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #FF6B6B !important;
    }
    
    .stSlider > div > div > div > div > div {
        background-color: #FFD700 !important;
        border-radius: 0px !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #FFD700 !important;
        border-radius: 0px !important;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        border: 3px solid #FFD700 !important;
        border-radius: 0px !important;
        background-color: #2E2E2E !important;
        color: #FFFFFF !important;
        font-family: 'Space Mono', monospace !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div > div {
        border: 3px solid #FFD700 !important;
        border-radius: 0px !important;
        background-color: #2E2E2E !important;
        color: #FFFFFF !important;
    }
    
    /* Metric */
    .stMetric {
        background-color: #2E2E2E !important;
        border: 3px solid #FFD700 !important;
        border-radius: 0px !important;
        box-shadow: 4px 4px 0px #FF6B6B !important;
        padding: 0.5rem !important;
    }
    
    .stMetric > div {
        justify-content: center !important;
    }
    
    .stMetric label {
        font-family: 'VT323', monospace !important;
        color: #FFD700 !important;
        font-size: 1.5rem !important;
        text-transform: uppercase !important;
    }
    
    .stMetric p {
        font-family: 'VT323', monospace !important;
        color: #FFFFFF !important;
        font-size: 2rem !important;
        text-align: center !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2E2E2E !important;
        border: 3px solid #FFD700 !important;
        border-radius: 0px !important;
        color: #FFD700 !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.2rem !important;
        text-transform: uppercase !important;
        margin-right: 5px !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFD700 !important;
        color: #2E2E2E !important;
    }
    
    /* Main content */
    .main .block-container {
        padding: 2rem !important;
        background-color: #1E1E1E;
        background-image: 
            linear-gradient(rgba(40, 40, 40, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(40, 40, 40, 0.1) 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* Table */
    .stTable, .dataframe {
        font-family: 'Space Mono', monospace !important;
        border: 3px solid #FFD700 !important;
    }
    
    .stTable th, .dataframe th {
        background-color: #FFD700 !important;
        color: #1E1E1E !important;
        font-family: 'VT323', monospace !important;
        text-transform: uppercase !important;
        font-size: 1.2rem !important;
        padding: 0.5rem !important;
    }
    
    .stTable td, .dataframe td {
        font-family: 'Space Mono', monospace !important;
        border: 1px solid #FFD700 !important;
        padding: 0.5rem !important;
    }
    
    /* Loading spinner */
    .stSpinner > div > div > div {
        border-color: #FFD700 transparent transparent transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Apply custom CSS
local_css()

# Helper functions for synthetic data generation
def generate_synthetic_tissue(size=(400, 400), tissue_type="normal"):
    """Generate synthetic tissue image for demonstration"""
    # Base noise
    np.random.seed(42)  # For reproducibility
    
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
        
    else:  # Default case
        tissue = np.random.rand(size[0], size[1])
    
    # Convert to PIL Image
    img_array = (tissue * 255).astype(np.uint8)
    img = Image.fromarray(img_array)
    
    # Convert to RGB
    img = img.convert('RGB')
    return img

def apply_virtual_stain(img, stain_type="H&E", intensity=0.8, contrast=1.2):
    """Apply virtual staining effect to the image"""
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
        
    else:  # Default grayscale
        stained = img_array
    
    # Convert back to PIL image
    result = Image.fromarray(stained)
    
    # Apply contrast adjustment
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(result)
        result = enhancer.enhance(contrast)
        
    return result

def calculate_metrics(original, stained, model_quality=0.85):
    """Calculate synthetic metrics for model evaluation"""
    # For MVP, we'll generate some plausible metrics
    # In a real app, these would be calculated from actual model outputs
    
    # Add some random variation but keep metrics generally aligned with model_quality
    variation = 0.1
    
    metrics = {
        "Structural Similarity": model_quality * (1 + random.uniform(-variation, variation)),
        "Color Accuracy": model_quality * (1 + random.uniform(-variation, variation)),
        "Nuclei Detection": model_quality * (1 + random.uniform(-variation, variation)),
        "Edge Preservation": model_quality * (1 + random.uniform(-variation, variation)),
        "Overall Quality": model_quality
    }
    
    # Ensure metrics are in valid range
    for key in metrics:
        metrics[key] = max(0, min(1, metrics[key]))
        
    return metrics

def get_stain_description(stain_type):
    """Return description for different stain types"""
    descriptions = {
        "H&E": "Hematoxylin & Eosin stain highlights cell nuclei in blue-purple and cytoplasm in pink. It's the most common stain used in histology.",
        "Masson's Trichrome": "This stain shows collagen fibers in blue, nuclei in black, and cytoplasm/muscle in red. Useful for identifying fibrotic tissue.",
        "PAS": "Periodic acid–Schiff stain highlights structures containing glycogen, mucus and basement membranes in magenta. Used to identify certain fungal infections and kidney conditions."
    }
    return descriptions.get(stain_type, "No description available.")

def display_model_info(model_quality):
    """Display information about the virtual staining model"""
    quality_level = "High" if model_quality > 0.8 else "Medium" if model_quality > 0.6 else "Low"
    
    st.markdown(f"""
    <div class="stCard">
        <h2>Virtual Staining Model Status</h2>
        <p>Current Model: <span style="color:#FFD700">RainPath-VS-{int(model_quality*100)}</span></p>
        <p>Quality Level: <span style="color:#FFD700">{quality_level}</span></p>
        <p>Training Progress: <span style="color:#FFD700">{int(model_quality*100)}%</span></p>
        <p>Last Updated: <span style="color:#FFD700">May 1, 2025</span></p>
    </div>
    """, unsafe_allow_html=True)

def display_retro_metrics(metrics):
    """Display metrics in a retro gaming style"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stMetric">
            <label>Structural Similarity</label>
            <p>{metrics['Structural Similarity']:.2f}</p>
            <div style="background:#2E2E2E; border:2px solid #FFD700; height:20px; width:100%;">
                <div style="background:#FFD700; width:{metrics['Structural Similarity']*100}%; height:100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stMetric" style="margin-top:10px;">
            <label>Color Accuracy</label>
            <p>{metrics['Color Accuracy']:.2f}</p>
            <div style="background:#2E2E2E; border:2px solid #FFD700; height:20px; width:100%;">
                <div style="background:#FFD700; width:{metrics['Color Accuracy']*100}%; height:100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stMetric">
            <label>Nuclei Detection</label>
            <p>{metrics['Nuclei Detection']:.2f}</p>
            <div style="background:#2E2E2E; border:2px solid #FFD700; height:20px; width:100%;">
                <div style="background:#FFD700; width:{metrics['Nuclei Detection']*100}%; height:100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stMetric" style="margin-top:10px;">
            <label>Edge Preservation</label>
            <p>{metrics['Edge Preservation']:.2f}</p>
            <div style="background:#2E2E2E; border:2px solid #FFD700; height:20px; width:100%;">
                <div style="background:#FFD700; width:{metrics['Edge Preservation']*100}%; height:100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stMetric" style="height:120px; display:flex; flex-direction:column; justify-content:center;">
            <label>Overall Quality</label>
            <p style="font-size:3rem !important;">{metrics['Overall Quality']:.2f}</p>
            <div style="background:#2E2E2E; border:2px solid #FFD700; height:20px; width:100%;">
                <div style="background:#FFD700; width:{metrics['Overall Quality']*100}%; height:100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def plot_training_history():
    """Plot synthetic training history data"""
    # Generate synthetic training data
    epochs = 20
    train_loss = np.exp(-np.linspace(0, 2, epochs)) * 0.5 + np.random.randn(epochs) * 0.05
    val_loss = np.exp(-np.linspace(0, 1.8, epochs)) * 0.5 + np.random.randn(epochs) * 0.07 + 0.05
    train_acc = 1 - np.exp(-np.linspace(0, 2, epochs)) * 0.6 + np.random.randn(epochs) * 0.03
    train_acc = np.clip(train_acc, 0, 1)
    val_acc = 1 - np.exp(-np.linspace(0, 1.8, epochs)) * 0.6 + np.random.randn(epochs) * 0.05
    val_acc = np.clip(val_acc, 0, 1)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot loss
    ax1.plot(range(1, epochs+1), train_loss, 'o-', color='#FFD700', label='Training Loss')
    ax1.plot(range(1, epochs+1), val_loss, 'o-', color='#FF6B6B', label='Validation Loss')
    ax1.set_title('Model Loss', color='#FFD700', fontsize=14)
    ax1.set_xlabel('Epochs', color='white')
    ax1.set_ylabel('Loss', color='white')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Plot accuracy
    ax2.plot(range(1, epochs+1), train_acc, 'o-', color='#FFD700', label='Training Accuracy')
    ax2.plot(range(1, epochs+1), val_acc, 'o-', color='#FF6B6B', label='Validation Accuracy')
    ax2.set_title('Model Accuracy', color='#FFD700', fontsize=14)
    ax2.set_xlabel('Epochs', color='white')
    ax2.set_ylabel('Accuracy', color='white')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Set background color and style
    fig.patch.set_facecolor('#1E1E1E')
    for ax in [ax1, ax2]:
        ax.set_facecolor('#2E2E2E')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.tick_params(colors='white')
        for label in ax.get_xticklabels():
            label.set_color('white')
        for label in ax.get_yticklabels():
            label.set_color('white')
    
    plt.tight_layout()
    return fig

def display_tissue_comparison(tissue_types=['normal', 'tumor', 'fibrotic']):
    """Display comparison of virtual staining across different tissue types"""
    cols = st.columns(len(tissue_types))
    
    for i, tissue_type in enumerate(tissue_types):
        with cols[i]:
            # Generate original image
            original = generate_synthetic_tissue(tissue_type=tissue_type)
            
            # Apply virtual staining
            stained = apply_virtual_stain(original, stain_type="H&E")
            
            # Display
            st.markdown(f"<h3 style='text-align:center;'>{tissue_type.capitalize()} Tissue</h3>", unsafe_allow_html=True)
            st.image(stained, caption=f"Virtual H&E Stain", use_column_width=True)
            
            # Add some mock metrics
            quality = 0.9 if tissue_type == 'normal' else 0.8 if tissue_type == 'tumor' else 0.7
            st.markdown(f"""
            <div style="background:#2E2E2E; border:2px solid #FFD700; padding:10px; text-align:center; margin-top:10px;">
                <p style="margin:0; color:#FFD700;">Quality Score: {quality:.2f}</p>
                <div style="background:#1E1E1E; height:10px; width:100%; margin-top:5px;">
                    <div style="background:#FFD700; width:{quality*100}%; height:100%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Main application
def main():
    # Header with animation effect
    st.markdown("""
    <div style="text-align:center; margin-bottom:30px;">
        <h1 class="title">RainPath Virtual Staining</h1>
        <p style="font-family:'VT323', monospace; font-size:1.5rem; margin-top:-15px; color:#FF6B6B;">
            LEVEL UP YOUR HISTOPATHOLOGY ANALYSIS
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("<h2>CONTROL PANEL</h2>", unsafe_allow_html=True)
        
        # Model quality (simulating model versions/performance)
        model_quality = st.slider("Model Performance", 0.5, 1.0, 0.85, 0.01)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Image generation settings
        st.markdown("<h3>Tissue Settings</h3>", unsafe_allow_html=True)
        tissue_type = st.selectbox("Tissue Type", ["normal", "tumor", "fibrotic"])
        
        st.markdown("<h3>Stain Settings</h3>", unsafe_allow_html=True)
        stain_type = st.selectbox("Stain Type", ["H&E", "Masson's Trichrome", "PAS"])
        stain_intensity = st.slider("Stain Intensity", 0.5, 1.5, 1.0, 0.1)
        stain_contrast = st.slider("Stain Contrast", 0.5, 2.0, 1.2, 0.1)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Generate button
        if st.button("GENERATE STAIN"):
            st.session_state.regenerate = True
        else:
            if 'regenerate' not in st.session_state:
                st.session_state.regenerate = True
        
        # Show stain description
        st.markdown(f"""
        <div style="background:#2E2E2E; border:2px solid #FFD700; padding:10px; margin-top:20px;">
            <h4 style="margin-top:0;">Stain Info</h4>
            <p style="font-size:0.9rem;">{get_stain_description(stain_type)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["Virtual Staining Demo", "Model Performance", "Tissue Comparison"])
    
    with tab1:
        # Generate images if needed
        if st.session_state.regenerate:
            with st.spinner("Generating virtual stain..."):
                # Simulate processing delay
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Generate original image
                original = generate_synthetic_tissue(tissue_type=tissue_type)
                
                # Apply virtual staining
                stained = apply_virtual_stain(original, stain_type=stain_type, 
                                             intensity=stain_intensity, contrast=stain_contrast)
                
                # Store in session state
                st.session_state.original = original
                st.session_state.stained = stained
                st.session_state.regenerate = False
                
                # Calculate metrics
                st.session_state.metrics = calculate_metrics(original, stained, model_quality)
                
                # Clear progress bar
                progress_bar.empty()
        
        # Display model info
        display_model_info(model_quality)
        
        # Display images
        if 'original' in st.session_state and 'stained' in st.session_state:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h2>Original Tissue</h2>", unsafe_allow_html=True)
                st.image(st.session_state.original, use_column_width=True)
                
            with col2:
                st.markdown(f"<h2>Virtual {stain_type} Stain</h2>", unsafe_allow_html=True)
                st.image(st.session_state.stained, use_column_width=True)
            
            # Display metrics
            st.markdown("<h2>Performance Metrics</h2>", unsafe_allow_html=True)
            display_retro_metrics(st.session_state.metrics)
            
    with tab2:
        st.markdown("<h2>Model Training Progress</h2>", unsafe_allow_html=True)
        
        # Display training history plot
        fig = plot_training_history()
        st.pyplot(fig)
        
        # Display dataset statistics
        st.markdown("<h2>Dataset Information</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="stCard">
                <h3>Training Dataset</h3>
                <ul style="list-style-type:none; padding-left:0;">
                    <li>➤ <span style="color:#FFD700">Normal Tissues:</span> 2,500 samples</li>
                    <li>➤ <span style="color:#FFD700">Tumor Tissues:</span> 1,800 samples</li>
                    <li>➤ <span style="color:#FFD700">Fibrotic Tissues:</span> 1,200 samples</li>
                    <li>➤ <span style="color:#FFD700">Other Types:</span> 500 samples</li>
                    <li>➤ <span style="color:#FFD700">Total Slides:</span> 6,000 samples</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="stCard">
                <h3>Stain Distribution</h3>
                <ul style="list-style-type:none; padding-left:0;">
                    <li>➤ <span style="color:#FFD700">H&E:</span> 70% of samples</li>
                    <li>➤ <span style="color:#FFD700">Masson's Trichrome:</span> 20% of samples</li>
                    <li>➤ <span style="color:#FFD700">PAS:</span> 7% of samples</li>
                    <li>➤ <span style="color:#FFD700">Other Stains:</span> 3% of samples</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Model architecture diagram
        st.markdown("<h2>Model Architecture</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="stCard" style="text-align:center;">
            <pre style="font-family:'Space Mono', monospace; color:#FFD700; line-height:1.5;">
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
|  Input Layer      |---->|  Encoder Blocks   |---->|  Bottleneck       |
|  (Raw Tissue)     |     |  (Conv + BN + ReLU)|     |  (Feature Maps)   |
|                   |     |                   |     |                   |
+-------------------+     +-------------------+     +-------------------+
                                                           |
                                                           v
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
|  Output Layer     |<----|  Decoder Blocks   |<----|  Skip Connections |
|  (Stained Image)  |     |  (Upsampling)     |     |  (Feature Fusion) |
|                   |     |                   |     |                   |
+-------------------+     +-------------------+     +-------------------+
            </pre>
        </div>
        """, unsafe_allow_html=True)
        
    with tab3:
        st.markdown("<h2>Tissue Type Comparison</h2>", unsafe_allow_html=True)
        st.markdown("""
        <p style="margin-bottom:20px;">
        Evaluating virtual staining performance across different tissue types is 
        critical for model enhancement. Below shows how the current model performs 
        on various tissue samples.
        </p>
        """, unsafe_allow_html=True)
        
        # Display comparison across tissue types
        display_tissue_comparison()
        
        # Challenging cases
        st.markdown("<h2>Challenging Cases</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="stCard">
            <h3>Current Challenges</h3>
            <ul style="list-style-type:none; padding-left:0;">
                <li>➤ <span style="color:#FFD700">Necrotic Areas:</span> 62% accuracy</li>
                <li>➤ <span style="color:#FFD700">Dense Fibrotic Regions:</span> 68% accuracy</li>
                <li>➤ <span style="color:#FFD700">Rare Tissue Types:</span> 57% accuracy</li>
                <li>➤ <span style="color:#FFD700">Artifacts in Source Images:</span> 49% accuracy</li>
            </ul>
            <p>These challenging cases represent primary targets for the model enhancement project.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Proposed improvements
        st.markdown("<h2>Proposed Improvements</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="stCard">
                <h3>Data Augmentation</h3>
                <ul style="list-style-type:none; padding-left:0;">
                    <li>➤ <span style="color:#FFD700">Synthetic Data Generation</span></li>
                    <li>➤ <span style="color:#FFD700">Advanced Transformations</span></li>
                    <li>➤ <span style="color:#FFD700">Targeted Oversampling</span></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="stCard">
                <h3>Model Architecture</h3>
                <ul style="list-style-type:none; padding-left:0;">
                    <li>➤ <span style="color:#FFD700">Attention Mechanisms</span></li>
                    <li>➤ <span style="color:#FFD700">Tissue-Specific Branches</span></li>
                    <li>➤ <span style="color:#FFD700">Multi-Stage Training</span></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="background:#2E2E2E; padding:10px; border-top:3px solid #FFD700; margin-top:30px; text-align:center;">
        <p style="font-family:'VT323', monospace; color:#FFD700; font-size:1.2rem; margin:0;">
            RAINPATH VIRTUAL STAINING MVP DEMO v1.0
        </p>
        <p style="color:#FF6B6B; font-size:0.8rem; margin:5px 0 0 0;">
            © 2025 RainPath Innovations
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()