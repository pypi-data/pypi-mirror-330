import shap
import numpy as np
import logging


def explainer_create(model, train_data, feature_names, model_type="Tree", validation_data=None,
                     pipeline_predictor=None, pipeline_transformer=None):
    '''
    Function to Create Explainer. Suggested type checking of models and generate appropriate explainers.
    Args:
        model (sklearn model): Model for which Shap explainer is to be created
        train_data (pandas dataframe): Training data to be used as background for calculating shap expectation values
    Returns:
        explainer(shap.explainer object): Shap Explainer Object depending on passed model (can be of different types depending on models)
    '''
    observations = None
    try:
        if (model_type == "Linear"):
            explainer = shap.LinearExplainer(model, train_data,
                                             feature_dependence="interventional",
                                             feature_names=feature_names)
        elif (model_type == "Tree"):
            explainer = shap.TreeExplainer(model, train_data, feature_names=feature_names)

        elif (model_type == "Pipeline-Tree"):

            observations = model[pipeline_transformer].transform(validation_data)

            explainer = shap.TreeExplainer(model[pipeline_predictor])

        elif (model_type == "Pipeline-Linear"):
            observations = model[pipeline_transformer].transform(validation_data)
            explainer = shap.LinearExplainer(model[pipeline_predictor],observations)

        else:
            logging.info("Running Kernel explainer. Will take a lot of time")
            explainer = shap.KernelExplainer(model.predict_proba, train_data, link='logit')
    except Exception:
        logging.info("Defaulted to Kernel explainer. Will take a lot of time")

        explainer = shap.KernelExplainer(model.predict_proba, train_data, link='logit')

    return explainer, observations


def get_shap_values(explainer, data, config=None):
    '''
    Function to get complete shap values (Base, Expected, Data).
    Args:
        explainer (shap.explainer object): SHAP Explainer object for which shap values are to be generated.
                                           Typically obtained from explainer_create(model, train_data) function call.
        data (pandas dataframe): Dataset for which shap values are to be generated (usually validation data)
    Returns:
        shap_values (list of shap values): list of three shap values (base values), (expected values) and (data)
    '''
    try:
        shap_values = explainer.shap_values(data)
    except Exception:
        shap_values = explainer.shap_values(data, check_additivity=False)

    if isinstance(shap_values, list) and (config["model_type"] == "Tree" or config["model_type"] == "Pipeline-Tree"):
        shap_values = shap_values[0]

    elif isinstance(shap_values, list):
        shap_values = np.stack((shap_values), axis=-1)
        shap_values = shap_values[:, :, 0]
        # print(shap_values)
    return shap_values
