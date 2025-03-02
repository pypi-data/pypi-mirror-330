# **SceneProgDatasets**

**SceneProgDatasets** is a easy to use retriver that sources assets from popular datasets based on a simple textual description. 

---

## **Features**
1. **Supported Datasets**
    - 3D-FUTURE
    - HSSD

## **Installation**
To install the package and its dependencies, use the following command:
```bash
pip install sceneprogdatasets
```

For proper usage, export the respective variables
```bash
export FUTURE_PATH= PATH/TO/3D-FUTURE/DATASET
export HSSD_PATH= PATH/TO/HSSD/DATASET
```

## **Getting Started**
Importing the Package
```python
from sceneprogdatasets import AssetRetriever
```

## **Usage Examples**
```python
retriever = AssetRetriver()
dataset, path = retriever("A simple dining table")
dataset, path = retriever("A sandwitch maker")
```
