## EazyML Responsible-AI: Counterfactual
![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.54-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

![EazyML](https://github.com/EazyML/eazyml-docs/raw/refs/heads/master/EazyML_logo.png)

`eazyml-counterfactual` is a python package that helps users optimize predictive outcomes by generating counterfactual explanations.
EazyML revolutionizes machine learning by introducing counterfactual inference, automating the process of identifying optimal changes to variables that shift outcomes from unfavorable to favorable. This approach overcomes the limitations of manual "what-if" analysis, enabling models to provide actionable, prescriptive insights alongside their predictions.

Designed for post-prediction analysis, the package answers questions like:
- "What minimal changes to input features can reverse an unfavorable prediction?"
- "How can I achieve a desired outcome by tweaking feature values?"

### Features
- **Counterfactual Explanations**: Identify feature changes required to alter predictions.
- **Prescriptive Analytics**: Generate actionable recommendations to achieve better outcomes.
- It performs feature selection from a training dataset by excluding specific columns and the target outcome column.
- This function builds a machine learning model using a specified training dataset.
- It provides platform to automates counterfactual inference for a test record by calculating the probability of an unfavorable outcome and determining the optimal adjustments to minimize it. It processes input datasets, configuration parameters, and model details to identify actionable changes in features while respecting constraints, enabling prescriptive insights for improved outcomes.

`eazyml-counterfactual` is ideal for scenarios like fraud detection, loan approvals, and customer churn prevention.`

## Installation
### User installation
The easiest way to install counterfactual package is using pip:
```bash
pip install -U eazyml-counterfactual
```
### Dependencies
EazyML Counterfactual requires :
- pandas
- matplotlib
- openpyxl
- scikit-learn
- scipy
- pyyaml

## Usage
Counterfactual can be used by initalizing EazyML and then getting insights for new test data.

```python
from eazyml_counterfactual import ez_init, ez_cf_inference

# initialize: setup book-keeping, access_key if required 
_ = ez_init()

selected_features = ['list of all the selected features in train data']
variants = ['list of features to be varied']

# Defining configurable parameters for counterfactual inference
options = {   
    "variants": variants,
    "outcome_ordinality": "1",    # Desired outcome to transition to, can also specify "minimize" or "maximize"
    "train_data": train_file,
    "preprocessor": preprocessor     # Preprocessor object for transforming input data (used in custom modeling)
}

# Specify the index of the test record for which counterfactual inference will be performed
test_index_no = 0
# pred_df it contains test dataframe with predicted output for outcome in probability term.
test_data = pred_df.loc[[test_index_no]]

result = ez_cf_inference(
                    test_data,
                    outcome,
                    selected_features,
                    model_info,
                    options
                    )
```
You can find more information in the [documentation](https://eazyml.readthedocs.io/en/latest/packages/eazyml_cf.html).

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