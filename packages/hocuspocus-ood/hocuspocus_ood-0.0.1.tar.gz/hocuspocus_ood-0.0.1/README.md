<!-- OPTIONAL: Project Logo
<p align="center">
  <img src="[OPT FILL: Path/link to logo image]" alt="Logo" style="width: 15%; display: block; margin: auto;">
</p>
-->

<h1 align="center"> HocusPOCUS Collection </h1>

<p align="center">
  <a href="[OPT FILL: Path/link to paper]"><img src="https://img.shields.io/badge/arXiv-2405.01535-b31b1b.svg" alt="arXiv"></a>
  <a href="https://github.com/stan-hua/hocuspocus/blob/main/LICENSE"><img src="https://img.shields.io/license-MIT-blue/license-MIT-blue.svg" alt="License"></a>
  <a href="[OPT FILL: Path/link to PyPI project]"><img src="https://img.shields.io/pypi/v/hocuspocus.svg" alt="PyPI version"></a>
</p>

<p align="center">
  ⚡ An OOD benchmark for point-of-care ultrasound 🚀 ⚡ <br>
</p>

---

## 💴 About the Data

|                | **Description**                                    | **Train/Val/Test**  |
|----------------|----------------------------------------------------|---------------------|
| **HP-Atlas**   | Crowd-sourced POCUS videos from 11 different views | 176/217/461 videos  |
| **HP-Quality** | Pairs of POCUS vs. non-POCUS images                | 426/520/1154 images |
| **HP-Noise**   | Generated images with different foreground shapes  | 480/480/960 images  |

---

## 🔧 Installation

**(Automatic) Installation:**

```shell
# Option 1. Available on PyPI
pip install hocuspocus_ood

# Option 2. Local Pip Install
git clone https://github.com/stan-hua/hocuspocus
pip install -e .
```

## 🏃 Quickstart

**Load HocusPOCUS Datasets:**
```python
from hocuspocus_ood import HocusPocusDataset, load_hocuspocus_metadata

# Parameters
dataset_name = "atlas"          # or "quality" or "noise"

# Optional parameters
hparams = {
    "transform": ...                # Torchvision transforms
    "load_image_func": ...,         # Custom calling function to load image given image path
    "load_image_kwargs": ...,       # Keyword arguments for custom image loading function
    "img_mode": 3,                  # 3 = RGB, 1 = Grayscale
    "img_size": (224, 224),         # Image size to resize to
    "scale": True,                  # If True, perform min-max normalization
}

# 1. HP-Atlas dataset               # NOTE: Both the extracted foreground and background are loaded
dataset = HocusPocusDataset("atlas", **hparams)
# 1.1. HP-Atlas dataset with background details kept
# dataset = HocusPocusDataset("atlas", separate_background=False, **hparams)
print(dataset[0])
# {
#   'id': 'pocus_atlas-renal-3-1',
#   'video_id': 'pocus_atlas-renal-3',
#   'img': tensor([[[0.0000, 0.0000, 0.0000,  ..., 0.0000, 0.0157, 0.1569]]]),
#   'background_img': tensor([[[0.0118, 0.0118, 0.0118,  ..., 0.0118, 0.0078, 0.0000]]]),
#   'label': 'renal',
# }

# 2. HP-Quality dataset
dataset = HocusPocusDataset("quality", **hparams)
print(dataset[0])
# {
#   'id': '0001-0',
#   'img': tensor([[[0.4235, 0.4510, 0.5020,  ..., 0.4627, 0.4471, 0.4549]]]),
#   'label': 'thyroid',
#   'quality': 'low_quality',
# }

# 3. HP-Noise dataset
dataset = HocusPocusDataset("noise", **hparams)
print(dataset[0])
# {
#   'id': 'hp_noise-1',
#   'img': tensor([[[0., 0., 0.,  ..., 0., 0., 0.]]]),
#   'label': 'noise-solid',
# }
```

## 🔧 Additional Utilities

### A. Transformations
1. **SquarePad** - zero pads image to 1:1 aspect ratio
```python
from hocuspocus_ood import SquarePad

# Example 1. On image
img = ...
transform = SquarePad()
img_padded = transform(img)

# Example 2. In a composed transform
import torchvision
transforms = torchvision.transforms.Compose([SquarePad(), ...])
```

### B. Augmentations
1. **MixBackground** - shuffles and overlays batch of foreground and background images (assuming images are the same size)
```python
from hocuspocus_ood import MixBackground

# Example 1. On batches of images
foreground_imgs = ...
background_imgs = ...
transform = MixBackground()
overlayed_imgs = transform(foreground_imgs, background_imgs)
```

2. **IgnoreEmptyRandomResizedCrop** - crops in a region where >= 50% of pixels are non-zero
```python
from hocuspocus_ood import IgnoreEmptyRandomResizedCrop

# Example 1. In a composed transform
import torchvision
transforms = torchvision.transforms.Compose([IgnoreEmptyRandomResizedCrop(), ...])
```

### C. Data Samplers
1. **ImbalancedDatasetSampler** - samples data points equally from each class in each batch
```python
from torch.utils.data import DataLoader
from hocuspocus_ood import ImbalancedDatasetSampler

# Example 1. Given a Dataset object
dataset = ...
sampler = ImbalancedDatasetSampler(dataset)
dataloader = DataLoader(dataset, sampler=sampler, shuffle=False)
```

2. **InfiniteBatchSampler** - samples batches infinitely from the dataset
```python
from torch.utils.data import DataLoader
from hocuspocus_ood import ImbalancedDatasetSampler

# Example 1. Given a Dataset object
dataset = ...
batch_size = 32
batch_sampler = InfiniteBatchSampler(dataset, batch_size=batch_size)
dataloader = DataLoader(dataset, batch_sampler=batch_sampler, shuffle=False)
```


## ⭐ Advanced

**Re-create HocusPOCUS datasets:**

```python
from hocuspocus_ood.scripts.create_dataset import *

# (Optional) Change save directory
save_dir = None

# 1. HP-Atlas (scrape from POCUS Atlas then process video)
download_pocus_atlas(save_dir)
process_pocus_atlas_dataset(save_dir, save_dir, extract_background=False)

# 2. HP-Quality (manually download from GrandChallenge - USEnhance 2023)
download_pocus_quality(save_dir)
create_pocus_quality_metadata(save_dir)

# 3. HP-Noise (generate data)
create_pocus_noise_dataset(save_dir)
```

## 👏 Acknowledgements

**Team Members**:
1. [Stanley Hua](mailto:stanley.z.hua@gmail.com)
2. Lauren Erdman

**Collaborators**:
1. SickKids, Urology Clinic
2. Stanford Health Lucille Packard Children's, Urology Clinic
3. Sinai Health, Maternal-Fetal Clinic
4. Ontario Fetal Centre


## Citation

If you find our work useful, please consider citing our paper!

```bibtex
@article{YourName,
  title={Your Title},
  author={Your team},
  journal={Location},
  year={Year}
}
``
