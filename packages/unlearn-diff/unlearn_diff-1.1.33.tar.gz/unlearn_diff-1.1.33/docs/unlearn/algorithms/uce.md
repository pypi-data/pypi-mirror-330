# Unified Concept Editing Algorithm for Machine Unlearning

This repository provides an implementation of the unified concept editing algorithm for machine unlearning in Stable Diffusion models. The unified concept editing algorithm allows you to remove specific concepts or styles from a pre-trained model without retraining it from scratch.

### Installation
```
pip install unlearn_diff
```
### Prerequisities
Ensure `conda` is installed on your system. You can install Miniconda or Anaconda:

- **Miniconda** (recommended): [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- **Anaconda**: [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)

After installing `conda`, ensure it is available in your PATH by running. You may require to restart the terminal session:

```bash
conda --version
```
### Create environment:
```
create_env <algorithm_name>
```
eg: ```create_env unified_concept_editing```

### Activate environment:
```
conda activate <environment_name>
```
eg: ```conda activate unified_concept_editing```

The <algorithm_name> has to be one of the folders in the `mu/algorithms` folder.

### Downloading data and models.
After you install the package, you can use the following commands to download.

1. **Dataset**:
  - **i2p**:
    - **Sample**:
     ```
     download_data sample i2p
     ```
    - **Full**:
     ```
     download_data full i2p
     ```
  - **quick_canvas**:
    - **Sample**:
     ```
     download_data sample quick_canvas
     ```
    - **Full**:
     ```
     download_data full quick_canvas
     ```

2. **Model**:
  - **compvis**:
    ```
    download_model compvis
    ```
  - **diffuser**:
    ```
    download_model diffuser
    ```

**Verify the Downloaded Files**

After downloading, verify that the datasets have been correctly extracted:
```bash
ls -lh ./data/i2p-dataset/sample/
ls -lh ./data/quick-canvas-dataset/sample/
```
---

## Usage

To train the Unified Concept Editing algorithm to unlearn a specific concept or style from the Stable Diffusion model, use the `train.py` script located in the `scripts` directory.

## Run Train
Create a file, eg, `my_trainer.py` and use examples and modify your configs to run the file.  

**Example Code**
**Using quick canvas dataset**


```python
from mu.algorithms.unified_concept_editing.algorithm import (
    UnifiedConceptEditingAlgorithm,
)
from mu.algorithms.unified_concept_editing.configs import (
    unified_concept_editing_train_mu,
)

algorithm = UnifiedConceptEditingAlgorithm(
    unified_concept_editing_train_mu,
    ckpt_path="/home/ubuntu/Projects/UnlearnCanvas/UnlearnCanvas/machine_unlearning/models/diffuser/style50/",
    raw_dataset_dir=(
        "/home/ubuntu/Projects/balaram/packaging/data/quick-canvas-dataset/sample"
    ),
    output_dir="/opt/dlami/nvme/outputs",
)
algorithm.run()
```

**Using i2p dataset**

```python
from mu.algorithms.unified_concept_editing.algorithm import (
    UnifiedConceptEditingAlgorithm,
)
from mu.algorithms.unified_concept_editing.configs import (
    unified_concept_editing_train_i2p,
)

algorithm = UnifiedConceptEditingAlgorithm(
    unified_concept_editing_train_i2p,
    ckpt_path="/home/ubuntu/Projects/UnlearnCanvas/UnlearnCanvas/machine_unlearning/models/diffuser/style50/",
    raw_dataset_dir=(
        "/home/ubuntu/Projects/balaram/packaging/data/quick-canvas-dataset/sample"
    ),
    output_dir="/opt/dlami/nvme/outputs",
    use_sample = True # to run on sample dataset
    dataset_type = "i2p",
    template_name = "self-harm",
)
algorithm.run()
```


**Running the Training Script in Offline Mode**

```bash
WANDB_MODE=offline python my_trainer.py
```

**How It Works** 
* Default Values: The script first loads default values from the train config file as in configs section.

* Parameter Overrides: Any parameters passed directly to the algorithm, overrides these configs.

* Final Configuration: The script merges the configs and convert them into dictionary to proceed with the training. 

### Directory Structure

- `algorithm.py`: Implementation of the ScissorHandsAlgorithm class.
- `configs/`: Contains configuration files for training and generation.
- `model.py`: Implementation of the ScissorHandsModel class.
- `scripts/train.py`: Script to train the ScissorHands algorithm.
- `trainer.py`: Implementation of the ScissorHandsTrainer class.
- `utils.py`: Utility functions used in the project.
- `data_handler.py` : Implementation of DataHandler class
---


### Description of Arguments in train_config.yaml
**Training Parameters**

* **train_method**: Specifies the method of training for concept erasure.
    * Choices: ["full", "partial"]
    * Example: "full"

* **alpha**: Guidance strength for the starting image during training.
    * Type: float
    * Example: 0.1

* **epochs**: Number of epochs to train the model.
    * Type: int
    * Example: 10

* **lr**: Learning rate used for the optimizer during training.
    * Type: float
    * Example: 5e-5


**Model Configuration**
* **ckpt_path**: File path to the checkpoint of the Stable Diffusion model.
    * Type: str
    * Example: "/path/to/model_checkpoint.ckpt"

* **config_path**: File path to the Stable Diffusion model configuration YAML file.
    * Type: str
    * Example: "/path/to/config.yaml"

**Dataset Directories**

* **dataset_type**: Specifies the dataset type for the training process.
    * Choices: ["unlearncanvas", "i2p"]
    * Example: "unlearncanvas"

* **template**: Type of template to use during training.
    * Choices: ["object", "style", "i2p"]
    * Example: "style"

* **template_name**: Name of the specific concept or style to be erased.
    * Choices: ["self-harm", "Abstractionism"]
    * Example: "Abstractionism"

**Output Configurations**

* **output_dir**: Directory where the fine-tuned models and results will be saved.
    * Type: str
    * Example: "outputs/erase_diff/finetuned_models"

**Sampling and Image Configurations**

* **use_sample**: Flag to indicate whether a sample dataset should be used for training.
    * Type: bool
    * Example: True

* **guided_concepts**: Concepts to guide the editing process.
    * Type: str
    * Example: "Nature, Abstract"

* **technique**: Specifies the editing technique.
    * Choices: ["replace", "tensor"]
    * Example: "replace"

* **preserve_scale**: Scale for preservation during the editing process.
    * Type: float
    * Example: 0.5

* **preserve_number**: Number of items to preserve during editing.
    * Type: int
    * Example: 10

* **erase_scale**: Scale for erasure during the editing process.
    * Type: float
    * Example: 0.8

* **lamb**: Lambda parameter for controlling balance during editing.
    * Type: float
    * Example: 0.01

* **add_prompts**: Flag to indicate whether additional prompts should be used.
    * Type: bool
    * Example: True

**Device Configuration**

* **devices**: Specifies the CUDA devices to be used for training (comma-separated).
    * Type: str (Comma-separated)
    * Example: "0,1"



