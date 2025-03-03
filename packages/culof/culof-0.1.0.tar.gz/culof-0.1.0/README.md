# cuLOF: CUDA-Accelerated Local Outlier Factor

A CUDA-accelerated implementation of the Local Outlier Factor (LOF) algorithm for anomaly detection. This implementation is designed to be compatible with scikit-learn's LOF interface while providing significant speedups for larger datasets.

## Installation

### Prerequisites

- CUDA Toolkit 11.0+
- Python 3.6+
- NumPy
- scikit-learn (for comparison)
- C++14 compliant compiler
- CMake 3.18+

### Installing from PyPI

The source distribution is available on PyPI:

```bash
pip install culof
```

**Note**: Since this is a CUDA extension, you must have the CUDA toolkit installed on your system before installing the package. The PyPI package is a source distribution that will be compiled during installation.

If you encounter compilation errors, follow the "Installing from Source" instructions below.

### Installing from Source

```bash
# Clone the repository
git clone https://github.com/Aminsed/cuLOF.git
cd cuLOF

# Option 1: Development installation
pip install -e .

# Option 2: Build from source
python setup.py install
```

### Conda Installation (Alternative)

If you're having trouble with the PyPI installation, consider using conda:

```bash
# Install dependencies
conda install -c conda-forge numpy scikit-learn cmake cudatoolkit>=11.0

# Install culof from source
pip install git+https://github.com/Aminsed/cuLOF.git
```

## Troubleshooting Installation

If you encounter issues during installation:

1. Ensure CUDA toolkit is properly installed and in your PATH
2. Check that your CUDA version is 11.0 or higher
3. Verify you have a modern C++ compiler (gcc 7+, MSVC 19.14+, clang 5+)
4. Make sure CMake 3.18+ is installed
5. For specific errors, check the project issues or create a new one at our [GitHub repository](https://github.com/Aminsed/cuLOF/issues)

## Usage

Basic Python usage:

```python
import numpy as np
from sklearn.datasets import make_blobs
from culof import LOF

# Generate sample data
X, _ = make_blobs(n_samples=1000, centers=1, random_state=42)
outliers = np.random.uniform(low=-10, high=10, size=(5, 2))
X = np.vstack([X, outliers])

# Create and configure LOF detector
lof = LOF(k=20)

# Fit and predict
# Returns 1 for inliers and -1 for outliers
results = lof.fit_predict(X)

# Get raw anomaly scores
scores = lof.score_samples(X)
```

## Performance

This CUDA implementation achieves significant speedups compared to scikit-learn's implementation, especially for larger datasets:

| Dataset Size | scikit-learn (s) | CUDA LOF (s) | Speedup |
|--------------|------------------|--------------|---------|
| 1,050        | 0.007614         | 0.049126     | 0.15x   |
| 2,065        | 0.022725         | 0.008887     | 2.56x   |
| 4,065        | 0.075397         | 0.020063     | 3.76x   |
| 8,002        | 0.261650         | 0.048288     | 5.42x   |
| 15,750       | 0.931842         | 0.137987     | 6.75x   |

Note: Performance may vary depending on your GPU and system configuration. The CUDA implementation has some overhead for small datasets but provides significant speedups for larger datasets.

## API Reference

### LOF Class

```python
class LOF:
    """Local Outlier Factor implementation accelerated with CUDA.
    
    Parameters
    ----------
    k : int, default=20
        Number of neighbors to use for LOF computation.
    normalize : bool, default=False
        Whether to normalize the input data before computation.
    contamination : float, default=0.1
        The proportion of outliers in the data set. Used when calling fit_predict.
    """
```

#### Methods

- `fit(X)`: Fit the LOF model.
- `predict(X=None)`: Predict outliers based on fitted LOF scores.
- `fit_predict(X)`: Fit the model and predict outliers in one step.
- `score_samples(X=None)`: Return the LOF scores for samples.

## Requirements

- CUDA Toolkit 11.0+
- CMake 3.18+
- C++14 compliant compiler
- Python 3.6+ with NumPy and scikit-learn (for comparison and testing)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The LOF algorithm was originally proposed by Breunig et al. in "LOF: Identifying Density-Based Local Outliers" (2000).
- This implementation builds upon ideas from the scikit-learn implementation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request to our [GitHub repository](https://github.com/Aminsed/cuLOF). 