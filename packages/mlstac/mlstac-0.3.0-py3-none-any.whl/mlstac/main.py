"""
MLSTAC main module.

This module provides a clean interface for working with MLSTAC models through STAC metadata,
supporting multiple storage backends.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import fsspec
import pystac
from tqdm import tqdm
import safetensors.numpy

from mlstac.fetch import download_file, load_python_module, load_stac_item
from mlstac.utils import get_scheme

# Central repository URL constant
ISP_REPO_URL = "https://huggingface.co/isp-uv-es/mlstac/resolve/main/"


class ModelLoader:
    """
    Manages machine learning models with capabilities for fetching, downloading, and loading.
    
    This class provides a unified interface for working with ML models regardless of 
    their storage location (local, remote) or format. It uses STAC metadata to describe
    model properties and capabilities.
    
    Attributes:
        source (str): Location of the model (URL or local path)
        scheme (str): Access scheme ('snippet', 'local', 'http', etc.)
        item (pystac.Item): STAC metadata for the model
        module (types.ModuleType, optional): Python module containing model loading functions
    
    Examples:
        >>> # Load a model from a snippet reference
        >>> model = ModelLoader("resnet50")
        >>> 
        >>> # Download the model locally
        >>> model.download("./models")
        >>> 
        >>> # Load the model for inference
        >>> inference_model = model.load_compiled_model()
    """
    
    def __init__(self, source: str, auto_print: bool = True):
        """
        Initialize the model manager.
        
        Args:
            source: Source identifier for the model. Can be a URL, local path,
                   or a model ID (which will be resolved as a "snippet").
            auto_print: Whether to automatically print model information upon loading.
                        Defaults to True.
        
        Raises:
            ValueError: If the source cannot be resolved or the model cannot be loaded.
        """
        self.scheme = get_scheme(source)
        self.module = None

        # Prepend repository URL if source is a snippet reference
        if self.scheme == "snippet":
            source = f"{ISP_REPO_URL}{source}"
            
        self.source = source
        self.item = load_stac_item(self.source)

        if auto_print:
            self.print_schema()        

    def print_schema(self) -> None:
        """
        Prints a visually appealing schema of the model.
        
        Automatically detects if running in a Jupyter/Colab notebook or terminal
        and formats the output accordingly.
        """
        # Check if running in notebook environment
        in_notebook = 'ipykernel' in sys.modules
        
        # Gather model details
        model_id = self.item.id
        framework = self.item.properties.get("mlm:framework", "Not specified")
        architecture = self.item.properties.get("mlm:architecture", "Not specified")
        tasks = self.item.properties.get("mlm:tasks", [])
        dependencies = self.item.properties.get("dependencies", "Not specified")
        
        # Convert file size from bytes to MB if available
        file_size = self.item.properties.get("file:size", 0)
        file_size_mb = f"{file_size / (1024 * 1024):.2f} MB" if file_size else "Unknown"
        
        if in_notebook:
            from IPython.display import display, HTML
            # Rich display for notebooks
            html_content = f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 5px solid #007bff;">
                <h3 style="color: #007bff; margin-top: 0;">📜 MLSTAC Model Schema</h3>
                <hr style="border-top: 1px solid #e9ecef;">
                <p><b>🆔 Model ID:</b> {model_id}</p>
                <p><b>🌍 Source:</b> {self.source}</p>
                <p><b>📡 Scheme:</b> {self.scheme}</p>
                <p><b>🛠️ Framework:</b> {framework}</p>
                <p><b>👁️‍🗨️ Dependencies:</b> {dependencies}</p>
                <p><b>🏗️ Architecture:</b> {architecture}</p>
                <p><b>📊 Tasks:</b> {', '.join(tasks) if tasks else 'None specified'}</p>                
                <p><b>📦 Size:</b> {file_size_mb}</p>
            </div>
            """
            display(HTML(html_content))
        else:
            # Terminal-friendly output with borders and spacing
            border = "-" * 50
            print(f"{border}")
            print("📜 MLSTAC Model Schema")
            print(f"{border}")
            print(f"🆔 Model ID:      {model_id}")
            print(f"🌍 Source:        {self.source}")
            print(f"📡 Scheme:        {self.scheme}")
            print(f"🛠️ Framework:     {framework}")
            print(f"👁️‍🗨️ Dependencies:  {dependencies}")
            print(f"🏗️ Architecture:  {architecture}")
            print(f"📊 Tasks:         {', '.join(tasks) if tasks else 'None specified'}")
            print(f"📦 Size:          {file_size_mb}")
            print(f"{border}")

    def download(
        self,
        output_dir: Path | str,
        trainable_model: bool = True,
        compiled_model: bool = True,
        example_data: bool = True,
        model_metadata: bool = True,
        model_loader: bool = True
    ) -> Path:
        """
        Download model files to the specified directory.
        
        Args:
            output_dir: Target directory for downloaded files
            trainable_model: Whether to download the trainable model weights
            compiled_model: Whether to download the compiled model
            example_data: Whether to download example data for testing
            model_metadata: Whether to download model metadata
            model_loader: Whether to download the model loader script
        
        Returns:
            Path object pointing to the output directory
        
        Raises:
            RuntimeError: If any of the specified files fail to download
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Define model artifacts to download with their suffixes
        artifacts_map = {
            "trainable_model": ("/model.safetensor", trainable_model),
            "compiled_model": ("/model.jit", compiled_model),
            "model_metadata": ("/mlm.json", model_metadata),
            "model_loader": ("/load.py", model_loader),
            "example_data": ("/example_data.safetensor", example_data)
        }
        
        # Download selected files
        downloaded_files = []
        for name, (suffix, should_download) in tqdm(artifacts_map.items(), desc="Downloading files"):
            if should_download:
                try:
                    file_path = download_file(
                        source=self.source,
                        snippet_suffix=suffix,
                        outpath=output_dir
                    )
                    downloaded_files.append(file_path)
                except Exception as e:
                    raise RuntimeError(f"Failed to download {name}: {str(e)}") from e

        # Update source and reload model info
        self.source = str(output_path)
        self.scheme = "local"
        
        if model_metadata:
            self.item = self._load()
            
        return output_path

    def _load(self) -> pystac.Item:
        """
        Load and update model metadata from local storage.
        
        Returns:
            Updated STAC item with local file references
        
        Raises:
            FileNotFoundError: If the metadata file doesn't exist
            ValueError: If the metadata file is invalid or corrupted
        """
        metadata_path = f"{self.source}/mlm.json"
        
        try:
            with fsspec.open(metadata_path, "r") as f:
                mlm_data = json.load(f)
                
                # Update asset paths to absolute local paths
                asset_files = {
                    "trainable": "/model.safetensor",
                    "compile": "/model.jit",
                    "example_data": "/example_data.safetensor"
                }
                
                for asset_key, filename in asset_files.items():
                    if asset_key in mlm_data.get("assets", {}):
                        mlm_data["assets"][asset_key]["href"] = str(Path(f"{self.source}{filename}").absolute())
                    
            return pystac.item.Item.from_dict(mlm_data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Model metadata file not found at {metadata_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid model metadata format: {str(e)}") from e
    
    def example_data(self) -> Any:
        """
        Load example data for model testing.
        
        Returns:
            Processed example data in the format expected by the model
        
        Raises:
            FileNotFoundError: If example data file doesn't exist
            ValueError: If model hasn't been downloaded locally
        """
        self._verify_local_access()
        
        try:
            # Ensure module is loaded
            if self.module is None:
                self.module = load_python_module(self.source)
                
            with fsspec.open(f"{self.source}/example_data.safetensor", "rb") as f:
                tensor_data = f.read()
                
            numpy_data = safetensors.numpy.load(tensor_data)
            return self.module.load_example(numpy_data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Example data file not found at {self.source}/example_data.safetensor")
        except AttributeError:
            raise AttributeError("Model loader module doesn't implement 'load_example' function")
    
    def trainable_model(self) -> Any:
        """
        Load the trainable version of the model for fine-tuning.
        
        Returns:
            Trainable model instance
            
        Raises:
            ValueError: If model hasn't been downloaded locally
            FileNotFoundError: If trainable model file doesn't exist
            AttributeError: If model loader doesn't implement required functions
        """
        self._verify_local_access()
        self.item = self._load()

        # Load the Python module containing model loading functions
        if self.module is None:
            self.module = load_python_module(self.source)

        try:
            return self.module.load_trainable(self.item.assets["trainable"].href)
        except KeyError:
            raise KeyError("Trainable model asset not found in metadata")
        except AttributeError:
            raise AttributeError("Model loader module doesn't implement 'load_trainable' function")
        except FileNotFoundError:
            raise FileNotFoundError(f"Trainable model file not found at {self.item.assets['trainable'].href}")
    
    def compiled_model(self) -> Any:
        """
        Load the compiled (optimized) version of the model for inference.
        
        Returns:
            Compiled model instance for inference
            
        Raises:
            ValueError: If model hasn't been downloaded locally
            FileNotFoundError: If compiled model file doesn't exist
            AttributeError: If model loader doesn't implement required functions
        """
        self._verify_local_access()
        self.item = self._load()

        # Load the Python module containing model loading functions
        if self.module is None:
            self.module = load_python_module(self.source)

        try:
            return self.module.load_compile(self.item.assets["compile"].href)
        except KeyError:
            raise KeyError("Compiled model asset not found in metadata")
        except AttributeError:
            raise AttributeError("Model loader module doesn't implement 'load_compile' function")
        except FileNotFoundError:
            raise FileNotFoundError(f"Compiled model file not found at {self.item.assets['compile'].href}")
    
    def get_model_summary(self) -> dict[str, Any]:
        """
        Returns a dictionary with key information about the model.
        
        Returns:
            Dictionary containing model metadata
        """
        return {
            "id": self.item.id,
            "source": self.source,
            "scheme": self.scheme,
            "framework": self.item.properties.get("mlm:framework"),
            "architecture": self.item.properties.get("mlm:architecture"),
            "tasks": self.item.properties.get("mlm:tasks", []),
            "dependencies": self.item.properties.get("dependencies"),
            "size_bytes": self.item.properties.get("file:size", 0)
        }
    
    def _verify_local_access(self) -> None:
        """
        Verify model is available locally before attempting to load.
        
        Raises:
            ValueError: If model hasn't been downloaded locally
        """
        if self.scheme != "local":
            raise ValueError(
                "The model must be downloaded locally first. "
                "Run .download(path) to download the model files."
            )
        
    def __repr__(self) -> str:
        """Return string representation of the ModelLoader instance."""
        return f"ModelLoader(source='{self.source}', scheme='{self.scheme}')"
    
    def __str__(self) -> str:
        """Return user-friendly string representation."""
        self.print_schema()
        return f"ModelLoader for '{self.item.id}'"


# For backward compatibility
load = ModelLoader