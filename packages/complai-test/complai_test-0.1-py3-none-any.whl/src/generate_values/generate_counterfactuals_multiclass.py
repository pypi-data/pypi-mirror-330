import pandas as pd
import numpy as np
from nice.explainers import NICE
import logging
import dask.dataframe as dd
import multiprocessing
from multiprocessing.pool import Pool
import dask
from timeit import default_timer as timer
from src.utils.counterfactual_common_functions import get_robustness_score, get_feature_change, nearest_real_counterfactual, \
    rowFun


class GenerateCounterfactualsMulticlass():
    def __init__(self):
        logging.info("Started Multiclass Counterfactual Generation")

    def get_nearest_synthetic_counterfactual(self, feature_names, NICE_model, instance,
                                             numerics=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']):
        # try:
        instance = instance.values.reshape((1, len(feature_names)))

        CF = NICE_model.explain(instance)
        cf_df = pd.DataFrame(data=CF, columns=feature_names)

        numeric = cf_df.select_dtypes(include=numerics)
        numeric = numeric.apply(pd.to_numeric)
        non_numeric = cf_df.select_dtypes(include='object')
        cf_df_fin = pd.concat([numeric, non_numeric], axis=1)
        # cf_df = cf_df.apply(pd.to_numeric)
        return_obj = cf_df_fin.to_dict(orient='records')[0]
        # except ValueError:
        #     return_obj = {}

        return return_obj

    def pred_lambda(self, x, **kwargs):

        iris_obj_new = kwargs["predictor"]
        other_classes = list(set(kwargs["target_classes"]) - set([kwargs["self_class"]]))
        return_obj = np.array([[max([i[j] for j in other_classes]), i[kwargs["self_class"]]] for i in
                               iris_obj_new.get_proba_scores(X_data=x, model=kwargs["model"])])
        return return_obj

    def train_nearest_synthetic_counterfactual(self, x_train, y_train, method, model, categorical_features,
                                               numerical_features, self_class,
                                               target_classes, predictor):
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

        prediction_function = lambda x: self.pred_lambda(x=x, model=model, self_class=self_class,
                                                         target_classes=target_classes, predictor=predictor)

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
            iris_obj = predictor

            numerical_features = [i for i in range(0, x_train_data.shape[1]) if
                                  i not in config["categorical_features_indexes"]]

            X_mad_dict = {i: (
                    np.sum(
                        abs(validation_data_new_moified.values[:, i] - np.mean(
                            validation_data_new_moified.values[:, i]))) /
                    validation_data_new_moified.values[:, i].shape[0]) for i in numerical_features}

            probability_scores = iris_obj.get_proba_scores(model, validation_data_new_moified.values)

            validation_data_new["probability_score"] = np.max(probability_scores, axis=1)

            validation_data_new["prediction_label"] = np.argmax(probability_scores, axis=1)
            target_classes = config["target_classes"]

            logging.info("Prediction Label Time : " + str(round(timer() - start_time, 5)) + " sec")

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
                                        "probability_score",
                                        "prediction_label", "idx"]]], x_mad=X_mad_dict, index=row["idx"].astype('int'),
                                                                                y_pred_label=validation_data_new[
                                                                                    "prediction_label"],
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
                                        "probability_score",
                                        "prediction_label", "idx"]]], x_mad=X_mad_dict, index=row["idx"],
                                                                                y_pred_label=validation_data_new[
                                                                                    "prediction_label"],
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
            #                         "probability_score",
            #                         "prediction_label", "idx"]]], index=row["idx"],
            #                                                            y_pred_label=validation_data_new["prediction_label"],
            #                                                            distance_method="l2"), axis=1)).compute(
            #     scheduler='processes')

            start_time = timer()

            NICE_obj_dict = {}

            for each in target_classes.values():
                NICE_obj_dict["NICE_obj_" + str(each)] = self.train_nearest_synthetic_counterfactual(
                    x_train=x_train_data,
                    model=model, self_class=each,
                    y_train=None, predictor=iris_obj,
                    target_classes=target_classes.values(),
                    method="Sparsity", categorical_features=config["categorical_features_indexes"],
                    numerical_features=numerical_features)
            logging.info("Nice train Time : " + str(round(timer() - start_time, 5)) + " sec")
            start_time = timer()

            validation_data_new_dd["nearest_synthetic_counterfactual_sparsity"] = validation_data_new_dd.map_partitions(
                lambda df: df.apply(lambda row: self.get_nearest_synthetic_counterfactual(
                    feature_names=config["feature_names"],
                    NICE_model=NICE_obj_dict["NICE_obj_" + str(row["prediction_label"]).split(".")[0]],
                    instance=row[[column for
                                  column in
                                  validation_data_new.columns
                                  if
                                  column not in [
                                      config[
                                          "id_column"],
                                      "nearest_counterfactual_l1",
                                      "nearest_counterfactual_l2",
                                      "nearest_synthetic_counterfactual_sparsity",
                                      "probability_score",
                                      "prediction_label", "idx"
                                  ]]]),
                                    axis=1), meta=('object')).compute(scheduler='processes')

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
                                                                 "probability_score",
                                                                 "prediction_label",
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
                                            "nearest_counterfactual_l1",
                                            "nearest_counterfactual_l2",
                                            "nearest_synthetic_counterfactual_sparsity",
                                            "probability_score",
                                            "prediction_label", "idx"]]]
                    , cf_np=row[["nearest_synthetic_counterfactual_sparsity"]]), axis=1), meta=('float')).compute(
                scheduler='processes')

            for key, each in target_classes.items():
                avg_robustness = np.mean(
                    validation_data_new_dd[validation_data_new_dd["prediction_label"] == each]["distance_values"])
                validation_data_new_dd["avg_robustness_" + str(key)] = avg_robustness

            min_robustness = np.min(validation_data_new_dd[[column for column in validation_data_new_dd.columns if
                                                            column.startswith("avg_robustness_")]], axis=1)
            validation_data_new_dd[
                [column for column in validation_data_new_dd.columns if column.startswith("avg_robustness_")]].min()
            validation_data_new_dd["min_robustness"] = min_robustness

            validation_data_new_dd = validation_data_new_dd.compute(
                scheduler='processes')
            min_idx = np.argmin(validation_data_new_dd[[column for column in validation_data_new_dd.columns if
                                                        column.startswith("avg_robustness_")]].iloc[:1].min())
            min_class_label = \
                [column for column in validation_data_new_dd.columns if column.startswith("avg_robustness_")][
                    min_idx].split(
                    "_")[-1]

            # for k, v in target_classes.items():
            #     if int(v) == int(min_class):
            #         min_class_label = k
            #         break
            proba_scores = iris_obj.get_proba_scores(
                X_data=validation_data_new_dd[[column for
                                               column in validation_data_new.columns if
                                               column not in [config["id_column"],
                                                              "nearest_counterfactual_l1",
                                                              "nearest_counterfactual_l2",
                                                              "nearest_synthetic_counterfactual_sparsity",
                                                              "probability_score",
                                                              "prediction_label", "distance_values",
                                                              "idx"]]].to_numpy(),
                model=model)
            for i in range(proba_scores.shape[1]):
                validation_data_new_dd["pred_proba_scores" + "_" + str(i)] = proba_scores[:, i]

            validation_data_new_dd["pred_proba_scores"] = validation_data_new_dd[
                [column for column in validation_data_new_dd.columns if column.startswith("pred_proba_scores")]].apply(
                lambda x: list(x), axis=1)
            validation_data_new_dd.drop(columns=[column for column in validation_data_new_dd.columns if
                                                 column.startswith(
                                                     "pred_proba_scores") and column != "pred_proba_scores"],
                                        inplace=True)
            validation_data_new_dd["min_class_label"] = min_class_label
            validation_data_new_dd["explainability_score"] = explainability_scores
            validation_data_new_dd["num_features_changes"] = num_feature_changes
            validation_data_new_dd["feature_importance_cf"] = pd.Series([changed_features.to_dict()])
            validation_data_new_dd["feature_importance_cf"] = validation_data_new_dd["feature_importance_cf"].fillna(
                "NA")

            validation_data_new_dd["ground_truth"] = y_val

            logging.info(
                "Robustness and Explainabilty Scores Generation Time : " + str(round(timer() - start_time, 5)) + " sec")
            start_time = timer()
            return NICE_obj_dict, validation_data_new_dd, numerical_features

        except Exception as error_message:
            logging.error(str(error_message))
            raise error_message
        finally:
            logging.info("DB Insert Time : " + str(round(timer() - start_time, 5)) + " sec")
