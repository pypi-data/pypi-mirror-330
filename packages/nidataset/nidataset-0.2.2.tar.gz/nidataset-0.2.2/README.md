# 🧠 NIfTI dataset management

This package provides a set of utilities for handling NIfTI datasets, including slice extraction, volume manipulation, and various utility functions to facilitate the processing of medical imaging data.

## 🛠️ Installation
Install the package running:
```bash
pip install nidataset
```

## 🧲 Import
Import the package as:
```python
import nidataset as nid
```

## 📂 Package Organization

### Draw
Handles operations related to drawing and coordinate systems.

- **draw_boxes**: Draws 3D bounding boxes on a NIfTI file based on a provided dataframe.
- **from_2D_to_3D_coords**: Converts box or point coordinates between the 2D and 3D reference systems based on the specified anatomical view.

### Preprocessing
Handles preprocessing operations on NIfTI files.

- **skull_CTA**: Applies thresholding, smoothing, FSL BET, and clipping to remove the skull from a CTA scan.
- **skull_CTA_dataset**: Applies the skull-stripping process to all CTA scans in a dataset folder.
- **mip**: Generates a 3D Maximum Intensity Projection (MIP) from a NIfTI file.
- **mip_dataset**: Generates MIPs from all NIfTI files in a dataset folder.
- **resampling**: Resamples a single NIfTI file to a desired volume size.
- **resampling_dataset**: Resamples all NIfTI files in a dataset folder.
- **register_CTA**: Registers a CTA image to a template using mutual information-based registration.
- **register_CTA_dataset**: Registers all CTA images in a dataset folder to a given template.

### Slices
Handles operations related to extracting 2D slices from 3D NIfTI files.

- **extract_slices**: Extracts slices from a NIfTI file and saves them as image files.
- **extract_slices_dataset**: Extracts slices from all NIfTI files in a dataset folder.
- **extract_annotations**: Extracts annotations from a NIfTI annotation file and saves them as CSV.
- **extract_annotations_dataset**: Extracts annotations from all NIfTI annotation files in a dataset folder and saves them as CSV.

### Utility
Handles metadata extraction and dataset information.

- **dataset_images_info**: Extracts metadata from all NIfTI files in a dataset and saves the results in a CSV file.
- **dataset_annotations_info**: Extracts 3D bounding boxes from all NIfTI annotation files in a dataset and saves the results in a CSV file.

### Volume
Handles operations related to volumetric transformations and bounding box extraction.

- **swap_nifti_views**: Swaps anatomical views in a NIfTI image by swapping axes and applying a 90-degree rotation.
- **extract_bounding_boxes**: Extracts 3D bounding boxes from a segmentation mask and saves them as a NIfTI file.
- **extract_bounding_boxes_dataset**: Extracts 3D bounding boxes from all segmentation masks in a dataset folder.
- **generate_brain_mask**: Generates a brain mask from a brain CTA scan in NIfTI format.
- **generate_brain_mask_dataset**: Generates brain masks for all brain CTA scans in a dataset folder.
- **crop_and_pad**: Finds the minimum bounding box around a CTA scan, resizes it to a target shape, and preserves spatial orientation.
- **crop_and_pad_dataset**: Processes all CTA scans in a dataset folder and applies the `crop_and_pad` operation.

## 📜 Requirements

```
Pillow>=9.4.0
nibabel>=5.1.0
numpy>=1.24.2
scikit-image>=0.19.3
pandas>=1.5.3
SimpleITK>=2.2.1,
scipy>=1.10.0,
tqdm>=4.67.1
```