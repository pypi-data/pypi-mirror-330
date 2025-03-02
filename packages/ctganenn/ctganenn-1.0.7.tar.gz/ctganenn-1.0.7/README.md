# CTGAN-ENN

CTGAN-ENN : Tabular GAN-based Hybrid sampling method.
- A sampling method that combine CTGAN (Conditional Tabular GAN) and ENN(Edited Nearest Neighboor)
- CTGAN is a powerfull oversampling method based on GAN for tabular data
- ENN is an efficient undersampling method to remove overlapped data 

## Installation

Install CTGAN-ENN using pip:

```bash
pip install ctganenn
```

## Usage

### Variables

- minClass: the minority class in the dataset (dataframe).
- majClass: the majority class in the dataset (dataframe).
- genData: how much data that you want generate from minorty class.
- targetLabel: what is your target label name in dataset.

### Example Usage
```bash
from ctganenn import CTGANENN
```

### use the CTGANENN function with 4 variables
```bash
CTGANENN(minClass,majClass,genData,targetLabel)
```
### Output
the output of method are X and y :
- X : all features of your dataset
- y : target label of your dataset

### Classification process
you can process the X and y variable to the next step for classification stage. For example using Decision Tree Classifier:

```bash
model = tree.DecisionTreeClassifier()
classification = model.fit(X, y)
```

## Limitation
CTGAN-ENN on this version only works for binary classification


