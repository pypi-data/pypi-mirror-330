## EazyML Responsible-AI: Modeling
![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.60-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

![EazyML](https://github.com/EazyML/eazyml-docs/raw/refs/heads/master/EazyML_logo.png)

`eazyml-automl` is a comprehensive python package designed to simplify machine learning workflows for data scientists, engineers, and developers. With **AutoML capabilities**, EazyML enables automated feature selection, model training, hyperparameter optimization, and cross-validation, all with minimal code. The package trains multiple models in the background, ranks them by performance metrics, and recommends the best model for your use case.

### Features
- **Global Feature Importance**: Get insights into the most impactful features in your dataset.
- **Confidence Scoring**: Enhance predictive reliability with confidence scores.

`eazyml-automl` is perfect for users looking to streamline the development of robust and efficient machine learning models.

## Installation
### User installation
The easiest way to install EazyML modeling is using pip:
```bash
pip install -U eazyml-automl
```
### Dependencies
EazyML Modeling requires :
- werkzeug,
- unidecode,
- pandas,
- scikit-learn,
- nltk,
- pyyaml,
- requests

## Usage
Initialize and build a predictive model based on the provided dataset and options. 
Perform prediction on the given test data based on model options.

```python
import pandas as pd
import pickle
from eazyml import ez_init, ez_build_model, ez_predict

# Initialize the EazyML library with the access key.
_ = ez_init()

# Load the training data (make sure the file path is correct).
train_file_path = "path_to_your_training_data.csv"  # Replace with the correct file path
train_data = pd.read_csv(train_file_path)

# Define the outcome (target variable) for the model
outcome = "target"  # Replace with your actual target variable name

# Set the options for building the model
build_options = {"model_type": "predictive"}

# Call the eazyml function to build the model
build_response = ez_build_model(train_data, outcome, options=build_options)

# build_response is a dictionary. Note: Do not print/view the response as it contains sensitive or encrypted model information in model_info.
build_response.keys()

# Expected output (this will vary depending on the data and model):            
# dict_keys(['success', 'message', 'model_performance', 'global_importance', 'model_info'])

# Save the response for later use (e.g., for predictions with ez_predict)
build_model_response_path = 'model_response.pkl'
pickle.dump(build_response, open(build_model_response_path, 'wb'))

# Load test data.
test_file_path = "path_to_your_test_data.csv"
test_data = pd.read_csv(test_file_path)

# Load output from ez_build_model. This should be the pickle file where model information is stored.
build_model_response_path = 'model_response.pkl'
build_model_response = pickle.load(open(build_model_response_path, 'rb'))
model_info = build_model_response["model_info"]

# Choose the model to use for prediction from the available performance options in the response.
pred_options = {"model": "Random Forest with Information Gain"}

# Call the eazyml function to predict
pred_response = ez_predict(test_data, model_info, options=pred_options)

# Check the keys of the prediction response. It will be a dictionary.
pred_response.keys()

# Example Output Keys(this will vary depending on your model and data):
# dict_keys(['success', 'message', 'pred_df'])

```
You can find more information in the [documentation](https://eazyml.readthedocs.io/en/latest/packages/eazyml_model.html).


## Useful links, other packages from EazyML family
- [Documentation](https://docs.eazyml.com)
- [Homepage](https://eazyml.com)
- If you have questions or would like to discuss a use case, please contact us [here](https://eazyml.com/trust-in-ai)
- Here are the other packages from EazyML suite:

    - [eazyml-automl](https://pypi.org/project/eazyml-automl/): eazyml-automl provides a suite of APIs for training, optimizing and validating machine learning models with built-in AutoML capabilities, hyperparameter tuning, and cross-validation.
    - [eazyml-data-quality](https://pypi.org/project/eazyml-data-quality/): eazyml-data-quality provides APIs for comprehensive data quality assessment, including bias detection, outlier identification, and drift analysis for both data and models.
    - [eazyml-counterfactual](https://pypi.org/project/eazyml-counterfactual/): eazyml-counterfactual provides APIs for optimal prescriptive analytics, counterfactual explanations, and actionable insights to optimize predictive outcomes to align with your objectives.
    - [eazyml-insight](https://pypi.org/project/eazyml-insight/): eazyml-insight provides APIs to discover patterns, generate insights, and mine rules from your datasets.
    - [eazyml-xai](https://pypi.org/project/eazyml-xai/): eazyml-xai provides APIs for explainable AI (XAI), offering human-readable explanations, feature importance, and predictive reasoning.
    - [eazyml-xai-image](https://pypi.org/project/eazyml-xai-image/): eazyml-xai-image provides APIs for image explainable AI (XAI).

## License
This project is licensed under the [Proprietary License](https://github.com/EazyML/eazyml-docs/blob/master/LICENSE).

---

Maintained by [EazyML](https://eazyml.com)  
© 2025 EazyML. All rights reserved.
