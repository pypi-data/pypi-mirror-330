# Recurrent Neural Networks for Dynamic VWAP Execution: An Adaptive Trading Strategy with Temporal Kolmogorov-Arnold Networks

This repository presents Aplo's latest research on dynamic VWAP execution and contains the code discussed in the paper [Recurrent Neural Networks for Dynamic VWAP Execution: An Adaptive Trading Strategy with Temporal Kolmogorov-Arnold Networks]().

> **Note:** This version includes only the TKAN-based dynamic VWAP model for simplicity in serialization. An LSTM-based version can be implemented by modifying the code accordingly.

## Model Overview

The dynamic VWAP model is implemented as a Keras model compatible with any backend (TensorFlow, JAX, or PyTorch). We recommend using JAX for optimal performance. 

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the package:**

   ```bash
   pip install .
   ```

   Alternatively, using [Poetry](https://python-poetry.org/):

   ```bash
   poetry install
   ```

## Usage

Below is a minimal example demonstrating how to use the dynamic VWAP model:

```python
from dynamic_vwap import DynamicVWAP, quadratic_vwap_loss, absolute_vwap_loss, volume_curve_loss
from dynamic_vwap.data_formater import full_generate
import pandas as pd

# Parameters
lookback = 120   # Number of past time steps used as input
n_ahead = 12     # Number of future time steps to predict
target_asset = 'AAPL'
BATCH_SIZE = 128
N_MAX_EPOCHS = 1000

# Load your data (here using Parquet files)
volumes = pd.read_parquet('path_to_your_volume_data.parquet')
notionals = pd.read_parquet('path_to_your_notionals_data.parquet')

# Generate training and testing datasets
X_train, X_test, y_train, y_test = full_generate(
    volumes, 
    notionals, 
    target_asset,
    lookback=lookback, 
    n_ahead=n_ahead, 
    test_split=0.2, 
    autoscale_target=True
)

# Initialize the dynamic VWAP model
model = DynamicVWAP(
    lookback=lookback, 
    n_ahead=n_ahead, 
    hidden_size=100, 
    hidden_rnn_layer=2
)

# Compile the model with a VWAP-specific loss function
model.compile(optimizer='adam', loss=quadratic_vwap_loss)

# Train the model
history = model.fit(
    X_train, y_train, 
    batch_size=BATCH_SIZE, 
    epochs=N_MAX_EPOCHS, 
    validation_split=0.2, 
    shuffle=True, 
    verbose=False
)

# Make predictions
predictions = model.predict(X_test, verbose=False)
```

### Model Parameters

- **lookback**: Number of past time steps used as input.
- **n_ahead**: Number of future time steps for which the dynamic volume curve is predicted.
- **hidden_size**: Number of units in the hidden layers of the internal RNN.
- **hidden_rnn_layer**: Number of TKAN layers in the internal RNN.

*Note:* The input data matrix must have a sequence length of `lookback + n_ahead - 1` time steps. This format ensures that the model receives the necessary ahead inputs during training. For real-time applications, appropriate padding may be needed.

### Loss Functions

The package provides the following loss functions to effectively minimize the deviation between the achieved VWAP and the market VWAP:

- `quadratic_vwap_loss`
- `absolute_vwap_loss`
- `volume_curve_loss`


## Data Formatting

The model expects inputs in matrix format rather than a dictionary. The expected shapes are:

- **Features Input**: A NumPy array of shape `(num_samples, lookback + n_ahead - 1, num_features)`.
- **Targets**: A NumPy array of shape `(num_samples, n_ahead, 2)`, where the first element (along the last dimension) corresponds to volume allocations and the second corresponds to prices.

The provided helper function `full_generate` in `data_formater.py` facilitates the creation of training and testing datasets. For example:

```python
import pandas as pd
from dynamic_vwap.data_formater import full_generate

volumes = pd.read_parquet('path_to_your_volume_data.parquet')
notionals = pd.read_parquet('path_to_your_notionals_data.parquet')

X_train, X_test, y_train, y_test = full_generate(
    volumes, 
    notionals, 
    target_asset='AAPL', 
    lookback=120, 
    n_ahead=12, 
    test_split=0.2, 
    autoscale_target=True
)
```

## Example and Results

For detailed examples, including reproduction of experimental results and graphs from the paper, please refer to the `example_and_results` folder.

## License

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/  
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png  
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
