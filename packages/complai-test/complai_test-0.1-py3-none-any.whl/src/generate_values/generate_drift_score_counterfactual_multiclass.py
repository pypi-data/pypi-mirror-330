import logging
import pandas as pd
import numpy as np
from src.utils.get_connections import tiny_db_connection
from src.utils.counterfactual_common_functions import get_feature_change
import dask.dataframe as dd
import multiprocessing
from multiprocessing.pool import Pool
import dask
from nice.explainers import NICE
from timeit import default_timer as timer


class GenerateCounterfactualFeatureAttributionMulticlass():
    def __init__(self):
        logging.info("Started Multiclass Counterfactual Feature Attribution Generation")

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

    def run(self, train_data_sampled=None, config=None, numerical_features=None, model=None, predictor=None,
            validation_data=None):
        try:
            logging.getLogger().setLevel(logging.INFO)
            train_data_sampled_df = train_data_sampled
            iris_obj = predictor
            probability_scores_train = iris_obj.get_proba_scores(model, train_data_sampled_df.values)

            train_data_sampled_df["probability_score"] = np.max(probability_scores_train, axis=1)
            train_data_sampled_df["prediction_label"] = np.argmax(probability_scores_train, axis=1)

            dask.config.set(pool=Pool(multiprocessing.cpu_count() - 1))
            data_new_dd = dd.from_pandas(train_data_sampled_df,
                                         npartitions=3 * (multiprocessing.cpu_count() - 1))
            start_time = timer()
            NICE_obj_dict_train = {}
            for each in config["target_classes"].values():
                NICE_obj_dict_train["NICE_obj_" + str(each)] = self.train_nearest_synthetic_counterfactual(
                    x_train=train_data_sampled.loc[:, config["feature_names"]].values,
                    model=model, self_class=each,
                    y_train=None, predictor=iris_obj,
                    target_classes=config["target_classes"].values(),
                    method="Sparsity", categorical_features=config["categorical_features_indexes"],
                    numerical_features=numerical_features)
            logging.info("Nice train Time : " + str(round(timer() - start_time, 5)) + " sec")
            start_time = timer()

            data_new_dd["nearest_synthetic_counterfactual_sparsity"] = data_new_dd.map_partitions(
                lambda df: df.apply(lambda row: self.get_nearest_synthetic_counterfactual(
                    feature_names=config["feature_names"],
                    NICE_model=NICE_obj_dict_train["NICE_obj_" + str(row["prediction_label"]).split(".")[0]],
                    instance=row[[column for
                                  column in
                                  train_data_sampled_df.columns
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
                                    axis=1),meta=('object')).compute(scheduler='processes')

            logging.info("Nice Explain Time : " + str(round(timer() - start_time, 5)) + " sec")
            validation_data = validation_data.loc[:, config["feature_names"]]
            probability_scores_validation = iris_obj.get_proba_scores(model, validation_data.values)

            validation_data["probability_score"] = np.max(probability_scores_validation, axis=1)
            validation_data["prediction_label"] = np.argmax(probability_scores_validation, axis=1)

            validation_data_new_dd = dd.from_pandas(validation_data,
                                                    npartitions=3 * (multiprocessing.cpu_count() - 1))

            NICE_obj_dict_validation = {}
            for each in config["target_classes"].values():
                NICE_obj_dict_validation["NICE_obj_" + str(each)] = self.train_nearest_synthetic_counterfactual(
                    x_train=validation_data.loc[:, config["feature_names"]].values,
                    model=model, self_class=each,
                    y_train=None, predictor=iris_obj,
                    target_classes=config["target_classes"].values(),
                    method="Sparsity", categorical_features=config["categorical_features_indexes"],
                    numerical_features=numerical_features)

            validation_data_new_dd["nearest_synthetic_counterfactual_sparsity"] = data_new_dd.map_partitions(
                lambda df: df.apply(lambda row: self.get_nearest_synthetic_counterfactual(
                    feature_names=config["feature_names"],
                    NICE_model=NICE_obj_dict_validation["NICE_obj_" + str(row["prediction_label"]).split(".")[0]],
                    instance=row[[column for
                                  column in
                                  validation_data.columns
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
                                    axis=1),meta=('object')).compute(scheduler='processes')

            drift_info_dict = {}
            for target, each in config["target_classes"].items():
                train_data_target = data_new_dd[
                    data_new_dd["prediction_label"] == each]
                feature_changes_train = train_data_target.map_partitions(
                    lambda df: df.apply(
                        lambda row: get_feature_change(instance=row[[column for
                                                                     column in
                                                                     data_new_dd.columns
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
                        axis=1),meta=('object')).compute(scheduler='processes')
                feature_imp_dict_train = feature_changes_train.apply(pd.Series).sum()
                num_records_train = train_data_target.shape[0].compute(scheduler='processes')
                feature_imp_dict_train = feature_imp_dict_train.to_dict()
                for key in config["feature_names"]:
                    if key not in feature_imp_dict_train.keys():
                        feature_imp_dict_train[key] = 0

                feature_attribution_train_df = pd.DataFrame.from_dict(feature_imp_dict_train, orient="index")

                feature_attribution_train_df = feature_attribution_train_df.reset_index()
                feature_attribution_train_df.rename(columns={"index": "Column_Name", 0: "train_attribution_value"},
                                                    inplace=True)
                feature_attribution_train_df["train_attribution_value"] = feature_attribution_train_df[
                                                                              "train_attribution_value"] / num_records_train

                feature_attribution_train_df = feature_attribution_train_df.sort_values("train_attribution_value",
                                                                                        ascending=False)
                feature_attribution_train_df = feature_attribution_train_df.reset_index(drop=True).reset_index()
                feature_attribution_train_df.rename(columns={"index": "train_rank"}, inplace=True)
                feature_attribution_train_df["train_rank"] = feature_attribution_train_df["train_rank"] + 1
                feature_attribution_train_df["iDCG"] = feature_attribution_train_df[
                                                           "train_attribution_value"] / np.log2(
                    feature_attribution_train_df["train_rank"] + 1)
                # target_series_train = train_data_sampled_df["prediction_label"].apply(
                #     lambda x: list(config["target_classes"].keys())[int(x)])

                # validation_counterfactuals_df = pd.DataFrame(validation_counterfactuals_data)
                # target_series_validation = validation_counterfactuals_df["prediction_label"].apply(
                #     lambda x: list(config["target_classes"].keys())[int(x)])

                validation_data_target = validation_data_new_dd[
                    validation_data_new_dd["prediction_label"] == each]
                feature_changes_validation = validation_data_target.map_partitions(
                    lambda df: df.apply(
                        lambda row: get_feature_change(instance=row[[column for
                                                                     column in
                                                                     validation_data_new_dd.columns
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
                        axis=1),meta=('object')).compute(scheduler='processes')
                feature_imp_dict_validation = feature_changes_validation.apply(pd.Series).sum()
                num_records_validation = validation_data_target.shape[0].compute(scheduler='processes')
                feature_imp_dict_validation = feature_imp_dict_validation.to_dict()
                for key in config["feature_names"]:
                    if key not in feature_imp_dict_validation.keys():
                        feature_imp_dict_validation[key] = 0

                feature_attribution_validation_target = pd.DataFrame.from_dict(
                    feature_imp_dict_validation, orient="index")
                # feature_attribution_validation_target = feature_attribution_validation_df[
                #     feature_attribution_validation_df["target"] == target]
                feature_attribution_validation_target = feature_attribution_validation_target.reset_index()
                feature_attribution_validation_target.rename(
                    columns={"index": "Column_Name", 0: "validation_attribution_value"},
                    inplace=True)
                feature_attribution_validation_target["validation_attribution_value"] = \
                    feature_attribution_validation_target[
                        "validation_attribution_value"] / num_records_validation
                feature_attribution_validation_target = feature_attribution_validation_target.sort_values(
                    "validation_attribution_value",
                    ascending=False)
                feature_attribution_validation_target = feature_attribution_validation_target.reset_index(
                    drop=True).reset_index()
                feature_attribution_validation_target.rename(columns={"index": "validation_rank"}, inplace=True)
                feature_attribution_validation_target["validation_rank"] = feature_attribution_validation_target[
                                                                               "validation_rank"] + 1

                fin_df = feature_attribution_validation_target.merge(feature_attribution_train_df,
                                                                     on=["Column_Name"])
                fin_df['DCG'] = fin_df["train_attribution_value"] / np.log2(fin_df["validation_rank"] + 1)
                ndcg_score = fin_df['DCG'].sum() / fin_df['iDCG'].sum()
                drift_detected = True if ndcg_score < 0.9 else False
                fin_df["feature_drifted"] = np.where(fin_df["train_rank"] == fin_df["validation_rank"], 0, 1)
                fin_df["num_features_drifted"] = fin_df["feature_drifted"].sum()
                fin_df = fin_df.loc[:, ["Column_Name", "feature_drifted", "num_features_drifted"]]
                # feature_attribution_validation_df["target"] = target_series_validation
                # feature_attribution_train_df["target"] = target_series_train

                feature_attribution_validation_target = feature_attribution_validation_target[
                    feature_attribution_validation_target["Column_Name"].isin(config["feature_names"])]

                feature_attribution_df = pd.DataFrame({"ndcg_score": ndcg_score,
                                                       "drift_detected": drift_detected,
                                                       "validation_feature_attribution_df_aggregated":
                                                           feature_attribution_validation_target.to_dict(
                                                               orient="records"),
                                                       "drift_info": fin_df.to_dict(orient='records')})

                feature_attribution_aggregated_validation_df = feature_attribution_df.loc[:,
                                                               ["validation_feature_attribution_df_aggregated",
                                                                "drift_info"]]
                #
                feature_attribution_aggregated_df = feature_attribution_df.loc[:,
                                                    ["ndcg_score", "drift_detected"]].head(1)
                # # feature_attribution_aggregated_df["Drift_score"] = np.min(
                # #     feature_attribution_aggregated_df["ndcg_score"])
                #

                feature_attribution_train_df["target"] = target

                feature_attribution_aggregated_df["target"] = target

                feature_attribution_aggregated_validation_df["target"] = target

                drift_info_dict[target] = {"feature_attribution_train_df": feature_attribution_train_df,
                                           "feature_attribution_aggregated_df": feature_attribution_aggregated_df,
                                           "feature_attribution_aggregated_validation_df":
                                               feature_attribution_aggregated_validation_df}
                #
            feature_attribution_aggregated_df_fin = pd.concat(
                [v["feature_attribution_aggregated_df"] for v in drift_info_dict.values()])
            feature_attribution_aggregated_validation_df_fin = pd.concat(
                [v["feature_attribution_aggregated_validation_df"] for v in drift_info_dict.values()])
            feature_attribution_train_df_fin = pd.concat(
                [v["feature_attribution_train_df"] for v in drift_info_dict.values()])

            return feature_attribution_aggregated_df_fin, feature_attribution_aggregated_validation_df_fin, \
                   feature_attribution_train_df_fin


        except Exception as error_message:
            logging.error(str(error_message))
            raise error_message
