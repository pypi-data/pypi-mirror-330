import pandas as pd
import numpy as np
from nice.explainers import NICE
import logging
import dask.dataframe as dd
import multiprocessing
from multiprocessing.pool import Pool
import dask
from src.utils.counterfactual_common_functions import get_robustness_score, get_feature_change, nearest_real_counterfactual, \
    rowFun
from timeit import default_timer as timer
from src.utils.get_connections import tiny_db_connection


class GenerateCounterfactualsRegressor():
    def __init__(self):
        logging.info("Started Regression Counterfactual Generation")

    def pred_lambda(self, x, **kwargs):

        boston_obj_new = kwargs["predictor"]
        regressor_value = boston_obj_new.get_scores(X_data=x, model=kwargs["model"])
        return_list = []
        for val in regressor_value:
            if ((val >= kwargs["x_target"] - kwargs["thershold"]) and (
                    val <= kwargs["x_target"] + kwargs["thershold"])):
                return_list.append([0, 1])
            else:
                return_list.append([1, 0])
        return np.array(return_list)

    def get_nearest_synthetic_counterfactual(self, predictor, feature_names, model, instance, x_train,
                                             threshold, categorical_features, numerical_features,
                                             numerics=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']):
        try:
            instance = instance.values.reshape((1, len(feature_names)))
            boston_obj_new = predictor
            regressor_value = boston_obj_new.get_scores(X_data=instance, model=model)
            NICE_model = self.train_nearest_synthetic_counterfactual(x_train=x_train, threshold=threshold, model=model,
                                                                     categorical_features=categorical_features,
                                                                     numerical_features=numerical_features,
                                                                     x_target=regressor_value, predictor=predictor,
                                                                     method="Sparsity")

            CF = NICE_model.explain(instance)
            cf_df = pd.DataFrame(data=CF, columns=feature_names)
            numeric = cf_df.select_dtypes(include=numerics)
            numeric = numeric.apply(pd.to_numeric)
            non_numeric = cf_df.select_dtypes(include='object')
            cf_df_fin = pd.concat([numeric, non_numeric], axis=1)
            return_obj = cf_df_fin.to_dict(orient='records')[0]
        except ValueError:
            return_obj = {}

        return return_obj

    def train_nearest_synthetic_counterfactual(self, x_train, threshold, model, categorical_features, x_target,
                                               predictor, numerical_features,
                                               method="Sparsity"):
        """
        Provided Training data of model, pretrained model and input instance, this function returns nearest synthetic
        counterfactual datapoint having opposite label.
        method: 'sparsity', 'proximity', 'plausibility'
        """
        if method == 'Sparsity':
            method = 'sparsity'
        elif method == 'Proximity':
            method = 'proximity'
        elif method == 'Plausibility':
            method = 'plausibility'

        prediction_function = lambda x: self.pred_lambda(x=x, model=model, thershold=threshold,
                                                         x_target=x_target, predictor=predictor)

        NICE_model = NICE(optimization=method, justified_cf=False)
        NICE_model.fit(X_train=x_train,
                       predict_fn=prediction_function,
                       y_train=None,
                       cat_feat=categorical_features,
                       num_feat=numerical_features)
        return NICE_model

    def run(self, x_train_data, validation_data_new_moified, validation_data_new, model, config, predictor=None,
            y_val=None):
        try:
            logging.getLogger().setLevel(logging.INFO)

            start_time = timer()

            boston_obj = predictor
            numerical_features = [i for i in range(0, x_train_data.shape[1]) if
                                  i not in config["categorical_features_indexes"]]
            X_mad_dict = {i: (
                    np.sum(
                        abs(validation_data_new_moified.values[:, i] - np.mean(
                            validation_data_new_moified.values[:, i]))) /
                    validation_data_new_moified.values[:, i].shape[0]) for i in numerical_features}

            regression_values = boston_obj.get_scores(X_data=validation_data_new_moified.to_numpy(), model=model)
            validation_data_new["regression_value"] = regression_values

            logging.info("Prediction Label Time :" + str(round(timer() - start_time, 5)) + " sec")
            start_time = timer()
            dask.config.set(pool=Pool(multiprocessing.cpu_count() - 1))
            validation_data_new_dd = dd.from_pandas(validation_data_new,
                                                    npartitions=3 * (multiprocessing.cpu_count() - 1))

            validation_data_new_dd["idx"] = validation_data_new_dd.map_partitions(
                lambda df: df.apply(lambda row: rowFun(row), axis=1)).compute(scheduler='processes')

            try:
                validation_data_new_dd["nearest_counterfactual_l1"] = validation_data_new_dd.map_partitions(
                    lambda df: df.apply(lambda row: nearest_real_counterfactual(x_data=validation_data_new[
                        [column for column in
                         validation_data_new.columns if
                         column not in [config["id_column"],
                                        "nearest_counterfactual_l1",
                                        "nearest_counterfactual_l2",
                                        "nearest_synthetic_counterfactual_sparsity",
                                        "regression_value", "idx"]]], x_mad=X_mad_dict, index=row["idx"].astype('int'),
                                                                                y_pred_label=validation_data_new[
                                                                                    "regression_value"],
                                                                                distance_method="l1"), axis=1),
                    meta=('object')).compute(
                    scheduler='processes')
            except AttributeError:
                validation_data_new_dd["nearest_counterfactual_l1"] = validation_data_new_dd.map_partitions(
                    lambda df: df.apply(lambda row: nearest_real_counterfactual(x_data=validation_data_new[
                        [column for column in
                         validation_data_new.columns if
                         column not in [config["id_column"],
                                        "nearest_counterfactual_l1",
                                        "nearest_counterfactual_l2",
                                        "nearest_synthetic_counterfactual_sparsity",
                                        "regression_value", "idx"]]], x_mad=X_mad_dict, index=row["idx"],
                                                                                y_pred_label=validation_data_new[
                                                                                    "regression_value"],
                                                                                distance_method="l1"), axis=1),
                    meta=('object')).compute(
                    scheduler='processes')


            # validation_data_new_dd["nearest_counterfactual_l2"] = validation_data_new_dd.map_partitions(
            #     lambda df: df.apply(lambda row: nearest_real_counterfactual(x_data=validation_data_new[
            #         [column for column in
            #          validation_data_new.columns if
            #          column not in [config["id_column"],
            #                         "nearest_counterfactual_l1",
            #                         "nearest_counterfactual_l2",
            #                         "nearest_synthetic_counterfactual_sparsity",
            #                         "regression_value", "idx"]]] ,index=row["idx"],
            #                                                                 y_pred_label=validation_data_new[
            #                                                                     "regression_value"],
            #                                                                 distance_method="l2"), axis=1)).compute(
            #     scheduler='processes')

            validation_data_new_dd["nearest_synthetic_counterfactual_sparsity"] = validation_data_new_dd.map_partitions(
                lambda df: df.apply(lambda row: self.get_nearest_synthetic_counterfactual(
                    feature_names=config["feature_names"], categorical_features=config["categorical_features_indexes"],
                    model=model, predictor=predictor, x_train=x_train_data, numerical_features=numerical_features,
                    threshold=config["regression_threshold"],
                    instance=row[[column for
                                  column in validation_data_new.columns if
                                  column not in [config["id_column"],
                                                 "nearest_counterfactual_l1",
                                                 "nearest_counterfactual_l2",
                                                 "regression_value",
                                                 "nearest_synthetic_counterfactual_sparsity", "idx"]]]),
                                    axis=1), meta=('object')).compute(
                scheduler='processes')
            logging.info("Nice Explain Time : " + str(round(timer() - start_time, 5)) + " sec")
            start_time = timer()
            feature_changes = validation_data_new_dd.map_partitions(lambda df: df.apply(
                lambda row: get_feature_change(instance=row[[column for
                                                             column in
                                                             validation_data_new.columns
                                                             if
                                                             column not in [
                                                                 config[
                                                                     "id_column"],
                                                                 "nearest_counterfactual_l1",
                                                                 "nearest_counterfactual_l2",
                                                                 "nearest_synthetic_counterfactual_sparsity",
                                                                 "regression_value",
                                                                 "idx"]]],
                                               dictionary=row[["nearest_synthetic_counterfactual_sparsity"]]),
                axis=1), meta=('object')).compute(scheduler='processes')

            num_feature_changes = feature_changes.apply(lambda x: len(x))
            changed_features = feature_changes.apply(pd.Series).sum()
            weighted_explainabilities = np.where(num_feature_changes == 1, 1,
                                                 np.where(num_feature_changes == 2, 0.9,
                                                          np.where(num_feature_changes == 3, 0.75,
                                                                   np.where(num_feature_changes == 4, 0.5,
                                                                            np.where(num_feature_changes == 5, 0.2,
                                                                                     0)))))
            explainability_scores = weighted_explainabilities.mean()

            validation_data_new_dd["distance_values"] = validation_data_new_dd.map_partitions(
                lambda df: df.apply(lambda row: get_robustness_score(
                    x_data_std=X_mad_dict,
                    ins=row[[column for
                             column in validation_data_new.columns if
                             column not in [config["id_column"],
                                            "nearest_synthetic_counterfactual_sparsity",
                                            "regression_value", "idx"]]]
                    , cf_np=row[["nearest_synthetic_counterfactual_sparsity"]]), axis=1), meta=('float')).compute(
                scheduler='processes')
            avg_robustness = validation_data_new_dd["distance_values"].sum() / len(validation_data_new_dd)
            validation_data_new_dd["avg_robustness"] = avg_robustness
            validation_data_new_dd = validation_data_new_dd.compute(
                scheduler='processes')
            validation_data_new_dd["explainability_score"] = explainability_scores

            validation_data_new_dd["num_features_changes"] = num_feature_changes
            validation_data_new_dd["feature_importance_cf"] = pd.Series([changed_features.to_dict()])
            validation_data_new_dd["feature_importance_cf"] = validation_data_new_dd["feature_importance_cf"].fillna(
                "NA")
            validation_data_new_dd["ground_truth"] = y_val

            logging.info(
                "Robustness and Explainabilty Scores Generation Time : " + str(round(timer() - start_time, 5)) + " sec")

            return validation_data_new_dd, numerical_features

        except Exception as error_message:
            logging.error(str(error_message))
            raise error_message
        finally:

            logging.info("DB Insert Time : " + str(round(timer() - start_time, 5)) + " sec")
