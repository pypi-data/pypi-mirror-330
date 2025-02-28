## EazyML Responsible-AI: XAI
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.65-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

![EazyML](https://github.com/EazyML/eazyml-docs/raw/refs/heads/master/EazyML_logo.png)

`eazyml-xai` is a python package designed to make machine learning predictions more transparent and interpretable. It provides human-readable explanations for predictions.

### Features
- Gain insights into **local feature importance and global feature impacts**.
- Understand **why a specific prediction was made**.
- Evaluate predictions with **explainability scores**.    

`eazyml-xai` is a key tool for building trust in AI systems by providing clear, actionable explanations.

## Installation
To use the explainable ai, ensure you have Python installed on your system.
### User installation
The easiest way to install EazyML Explainable AI is using pip:
```bash
pip install -U eazyml-xai
```
### Dependencies
This package requires:
- pandas,
- scikit-learn,
- werkzeug,
- Unidecode,
- pydot,
- numpy,
- pyyaml

## Usage
Here's an example of how you can use the APIs from this package.
```python
from eazyml_xai import ez_init, ez_explain

# initialize: setup book-keeping, access_key if required 
_ = ez_init()

response = ez_explain(
                train_data(`DataFrame/str`) = 'train_dataframe/train_data_path',
                outcome(`str`) = 'target',
                test_data(`DataFrame/str`) = 'test_dataframe/test_data_path',
                model(`Bytes/object`) = 'Encripted model_info from ez_build_model response or the trained model'
                options(`dict`) = {
                    "record_number"(`list of integer`): "Specify the record number of test data in the list on which you want to get the explanations"
                    "scaler"(`object`): "Trained scaler object"
                    "preprocessor"(`object`): "Trained preprocessor object"
            }
        )

explanations = response['explanations']
```
You can find more information in the [documentation](https://eazyml.readthedocs.io/en/latest/packages/eazyml_xai.html).


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
