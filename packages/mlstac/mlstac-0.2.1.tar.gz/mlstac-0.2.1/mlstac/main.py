"""
ISP Model Manager module for efficient model loading and management.
Handles downloading, loading, and accessing machine learning models from repositories.
"""
import json
from pathlib import Path

import fsspec
import pystac
import safetensors.numpy
from mlstac.fetch import download_file, load_python_module, load_stac_item
from mlstac.utils import get_scheme

# Central repository URL constant
ISP_REPO_URL = "https://huggingface.co/isp-uv-es/mlm/resolve/main/"

class ModelManager:
    """
    Manages ISP models with capabilities for fetching, downloading, and loading models.
    
    Attributes:
        source (str): Location of the model (URL or local path)
        scheme (str): Access scheme ('snippet', 'local', etc.)
        model_item (pystac.Item): STAC metadata for the model
        module: Python module containing model loading functions
    """
    
    def __init__(self, source):
        """
        Initialize the model manager.
        
        Args:
            source (str): Source identifier for the model
        """
        self.scheme = get_scheme(source)
        # Prepend repository URL if source is a snippet reference
        if self.scheme == "snippet":
            source = f"{ISP_REPO_URL}{source}"
            
        self.source = source
        self.item = load_stac_item(self.source)
        self.module = load_python_module(self.source)

    def download(self, output_dir):
        """
        Download all model files to the specified directory.
        
        Args:
            output_dir (str): Target directory for downloaded files
        """
        # Model artifacts to download with their suffixes
        artifacts = [
            "/model.safetensor",     # Trained model weights
            "/model.jit",            # Compiled model
            "/mlm.json",             # Model metadata
            "/load.py",              # Model loader script
            "/example_data.safetensor"  # Example data for testing
        ]
        
        # Download all required files
        for suffix in artifacts:
            download_file(
                source=self.source,
                snippet_suffix=suffix,
                outpath=output_dir
            )

        # Update source and reload model info
        self.source = output_dir
        self.item = self.load()
        self.scheme = "local"

    def load(self):
        """
        Load and update model metadata from local storage.
        
        Returns:
            pystac.Item: Updated STAC item with local file references
        """
        with fsspec.open(f"{self.source}/mlm.json", "r") as f:
            mlm_data = json.load(f)
            
            # Update asset paths to absolute local paths
            asset_files = {
                "trainable": "/model.safetensor",
                "compile": "/model.jit",
                "example_data": "/example_data.safetensor"
            }
            
            for asset_key, filename in asset_files.items():
                mlm_data["assets"][asset_key]["href"] = str(Path(f"{self.source}{filename}").absolute())
                
        return pystac.item.Item.from_dict(mlm_data)
    
    def load_example_data(self):
        """
        Load example data for model testing.
        
        Returns:
            Processed example data in the format expected by the model
        """
        with fsspec.open(f"{self.source}/example_data.safetensor", "rb") as f:
            tensor_data = f.read()
        numpy_data = safetensors.numpy.load(tensor_data)
        return self.module.load_example(numpy_data)
    
    def load_trainable_model(self):
        """
        Load the trainable version of the model.
        
        Returns:
            Trainable model instance
            
        Raises:
            ValueError: If model hasn't been downloaded locally
        """
        self._verify_local_access()
        self.item = self.load()
        return self.module.load_trainable(self.item.assets["trainable"].href)
    
    def load_compiled_model(self):
        """
        Load the compiled (optimized) version of the model.
        
        Returns:
            Compiled model instance for inference
            
        Raises:
            ValueError: If model hasn't been downloaded locally
        """
        self._verify_local_access()
        self.item = self.load()
        return self.module.load_compile(self.item.assets["compile"].href)
    
    def _verify_local_access(self):
        """
        Verify model is available locally before attempting to load.
        
        Raises:
            ValueError: If model hasn't been downloaded locally
        """
        if self.scheme != "local":
            raise ValueError("The model must be downloaded locally first. Run .download(path)")