# SANNO
The official implementation for "SANNO".

## Table of Contents
- [Datasets](#datasets)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Tutorial](#tutorial)  
- [Citation](#citation)  

---

## Datasets
We provide preprocessed datasets for easy reproduction.  

Download datasets from: [Dataset Link]()

---

## Installation
To use {Project Name}, follow these steps:  

1. Create a conda environment:  
    ```
    conda create -n {SANNO} python=3.7
    conda activate {SANNO}
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Install [PYG](https://pytorch-geometric.readthedocs.io/en/latest/index.html) and [Pytorch](https://pytorch.org/) according to the CUDA version, take torch-1.13.1+cu117 (Ubuntu 20.04.4 LTS) as an example:
    ```
    conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia
    pip install torch_geometric==2.3.0 # must be this version
    pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-1.13.1+cu117.html
    ```

## Usage
### Data Preprocessing

In order to run SANNO, we need to first create anndata from the raw data.

We require two types of datasets for this project: **reference data** and **query data**. Both datasets should be provided in `.h5ad` format, with cells stored in `obs` and genes/features stored in `var`.

#### Reference Data
- **Format**: `.h5ad`
- **Content**:
  - `obs`: Cell metadata, including a mandatory `cell_type` column indicating the true cell type labels.
  - `var`: Gene/feature metadata.
  - `obsm`: Spatial coordinates stored under the key `pos`, representing the relative positions of cells as a 2D numpy array (`n_cells x 2`).

#### Query Data
- **Format**: `.h5ad`
- **Content**:
  - `obs`: Cell metadata (cell type labels are not required).
  - `var`: Gene/feature metadata.
  - `obsm`: Spatial coordinates stored under the key `pos`, representing the relative positions of cells as a 2D numpy array (`n_cells x 2`).

### Cell Type Annotation
The processed data are used as input to SANNO and a reference genome is provided to extract the embedding and anootation incorporating reference Spatial Transcriptomics information:

```
cd SANNO/SANNO

python main_xy_adj.py   --gpu_index 3 # GPU index
                        --type st2st \ # project type
                        --dataset Project name \ # project name
                        --train_dataset path/to/train_adata.h5ad \ # reference data
                        --test_dataset path/to/test_adata.h5ad \ # query data
                        --log log \ # log path
```

The `project type` must be selected based on the nature of the reference and query datasets. The following modes are supported:

- `st2st` – For cases where both the reference and query datasets are spatial transcriptomics.
- `st2sc` – For cases where the reference dataset is spatial transcriptomics, and the query dataset is single-cell transcriptomics.
- `sc2sc` – For cases where both the reference and query datasets are single-cell transcriptomics.

Running the above command will generate three output files in the output path:

- `acc.csv`: Contains the overall accuracy of the query data and SANNO predictions.
- `embedding.h5ad`: An AnnData file storing the embeddings extracted by SANNO.
- `Reports`: A set of logs recorded during the training process.

## Tutorial 教程

### Tutorial 1: Cell annotations within samples (HubMap CL A & HubMap CL B)

1. Install the required environment according to [Installation](#installation).
2. Download the datasets from [HubMap CL](datasets/Hubmap_CL_intra/raw/).
3. Preprocess the datasets according to the [Data Preprocessing](#data-preprocessing) standards.
4. For more detailed information, run the tutorial [HubMap_CL_intra.ipynb](Toturial/Toturial1_intra_dataset.ipynb) for how to do data preprocessing and training.

### Tutorial 1: Cell annotations cross samples (Tonsil & BE)

1. Install the required environment according to [Installation](#installation).
2. Download the datasets from [Tonsil_BE](datasets/Tonsil_BE_cross/raw/).
3. Preprocess the datasets according to the [Data Preprocessing](#data-preprocessing) standards.
4. For more detailed information, run the tutorial [HubMap_CL_intra.ipynb](Toturial/Toturial2_cross_dataset.ipynb) for how to do data preprocessing and training.

## Citation
If you use SANNO in your research, please cite:

```
@article{yourcitation,
  title={{Your Paper Title}},
  author={Your Name, Coauthor Name},
  journal={Journal Name},
  volume={00},
  pages={1--10},
  year={2024}
}
```