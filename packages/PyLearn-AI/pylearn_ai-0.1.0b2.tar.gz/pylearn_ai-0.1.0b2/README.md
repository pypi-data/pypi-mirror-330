# PyLearn-AI

**PyLearn-AI** is a pure-Python machine learning and deep learning framework built entirely with the Python standard library. No external dependencies required.

## Features
- No dependencies (NO NumPy, SciPy, or Pandas), just Python 3.10
- Supports basic machine learning and deep learning models
- Includes custom matrix and tensor operations
- Educational and easy to understand, encouraging users to learn the underlying functionality of modern ML/DL libraries

*Note: The dependencies listed in requirements.txt are only for documentation, testing, and package publishing.*

## Novelty

Before starting this project, I searched for similar packages and was not surprised to find a handful of them, many of which use NumPy at the core of their framework.

What makes this project stand out is that **PyLearn-AI** does not use NumPy or any other external libraries.

At the core of the package is the `UnitFrame` data structure, which assists with common matrix operations performed in modern ML/DL libraries. It serves a similar purpose as a NumPy array or a pandas DataFrame.

The compromise with this approach is speed, efficiency, and computation.

This package is not intended to be used to train, optimize, or build the next machine learning model. It is intended as a learning experience to remove as much abstraction as possible.

## Work in Progress

To my surprise, **PyLearn-AI** was available in the Python Package Index. To secure the name, I published the package prematurely. I will be releasing beta versions as development continues.

## Installation

```bash
pip install pylearn-ai
```

## Usage

```python
from pylearn.core.unitframe import UnitFrame

uf = UnitFrame([[1, 2], [3, 4]])
print(uf)
```

## Project Structure

```plaintext
PyLearn-AI/
├── core/           
├── neural/         
├── reinforcement/  
├── supervised/     
├── unsupervised/   
├── utils/          
```

- core: Core algorithms, structures, and tensor class
- neural: Deep learning models (MLP, CNN, GNN)
- reinforcement: Reinforcement learning (Q-learning, policy optimization)
- supervised: Supervised learning (regression, classification)
- unsupervised: Clustering, dimensionality reduction
- utils: Activations, losses, metrics, and preprocessing

## License

[MIT License](/LICENSE)