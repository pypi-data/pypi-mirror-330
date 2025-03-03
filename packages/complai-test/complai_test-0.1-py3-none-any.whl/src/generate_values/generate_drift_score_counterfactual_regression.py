import logging
import pandas as pd
import numpy as np
from src.utils.get_connections import tiny_db_connection
from src.utils.counterfactual_common_functions import get_feature_change
import dask.dataframe as dd
import multiprocessing
from multiprocessing.pool import Pool
import dask
from tinydb import Query
from nice.explainers import NICE


class GenerateCounterfactualFeatureAttributionRegression():
    def __init__(self):
        logging.info("Started Regression Counterfactual Feature Attribution Generation")

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

    def get_live_feature_attribution_drift(self, live_data_new_moified, config, model, x_train_data,
                                           feature_attribution_validation_df,
                                           predictor=None, numerical_features=None):
        for data in live_data_new_moified:
            dask.config.set(pool=Pool(multiprocessing.cpu_count() - 1))
            data_new_dd = dd.from_pandas(data, npartitions=3 * (multiprocessing.cpu_count() - 1))

            data_new_dd["nearest_synthetic_counterfactual_sparsity"] = data_new_dd.map_partitions(
                lambda df: df.apply(lambda row: self.get_nearest_synthetic_counterfactual(
                    feature_names=config["feature_names"], categorical_features=config["categorical_features_indexes"],
                    model=model, predictor=predictor, x_train=x_train_data, numerical_features=numerical_features,
                    threshold=config["regression_threshold"],
                    instance=row[[column for
                                  column in data_new_dd.columns if
                                  column not in [config["id_column"],
                                                 "nearest_counterfactual_l1",
                                                 "nearest_counterfactual_l2",
                                                 "regression_value",
                                                 "nearest_synthetic_counterfactual_sparsity", "idx"]]]),
                                    axis=1),meta=('object')).compute(
                scheduler='processes')

            feature_changes = data_new_dd.map_partitions(lambda df: df.apply(
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
                                                                 "regression_value",
                                                                 "idx"]]],
                                               dictionary=row[["nearest_synthetic_counterfactual_sparsity"]]),
                axis=1),meta=('object')).compute(scheduler='processes')

            feature_imp_dict = feature_changes.apply(pd.Series).sum()
            num_records = data.shape[0]
            feature_imp_dict = feature_imp_dict.to_dict()

            for key in config["feature_names"]:
                if key not in feature_imp_dict.keys():
                    feature_imp_dict[key] = 0

            feature_attribution_live_df = pd.DataFrame.from_dict(feature_imp_dict, orient="index")

            feature_attribution_live_df = feature_attribution_live_df.reset_index()
            feature_attribution_live_df.rename(columns={"index": "Column_Name", 0: "live_attribution_value"},
                                               inplace=True)
            feature_attribution_live_df["live_attribution_value"] = feature_attribution_live_df[
                                                                        "live_attribution_value"] / num_records
            feature_attribution_live_df = feature_attribution_live_df.sort_values("live_attribution_value",
                                                                                  ascending=False)
            feature_attribution_live_df = feature_attribution_live_df.reset_index(drop=True).reset_index()
            feature_attribution_live_df.rename(columns={"index": "live_rank"}, inplace=True)
            feature_attribution_live_df["live_rank"] = feature_attribution_live_df["live_rank"] + 1

            fin_df = feature_attribution_validation_df.merge(feature_attribution_live_df, on="Column_Name")
            fin_df['DCG'] = fin_df["validation_attribution_value"] / np.log2(fin_df["live_rank"] + 1)

            ndcg_score_day = fin_df['DCG'].sum() / fin_df['iDCG'].sum()
            drift_detected_day = True if ndcg_score_day < 0.9 else False
            fin_df["feature_drifted"] = np.where(fin_df["live_rank"] == fin_df["validation_rank"], 0, 1)
            fin_df["num_features_drifted"] = fin_df["feature_drifted"].sum()
            fin_df = fin_df.loc[:, ["Column_Name", "feature_drifted", "num_features_drifted"]]

            yield {"ndcg_score_day": ndcg_score_day,
                   "drift_detected": drift_detected_day,
                   "live_feature_attribution_df_aggregated": feature_attribution_live_df.to_dict(orient="records"),
                   "drift_info": fin_df.to_dict(orient='records')}

    def run(self, train_data_sampled=None, config=None, numerical_features=None, model=None, predictor=None,
            validation_data=None):

        try:
            logging.getLogger().setLevel(logging.INFO)
            train_data_sampled_df = train_data_sampled
            dask.config.set(pool=Pool(multiprocessing.cpu_count() - 1))
            data_new_dd = dd.from_pandas(train_data_sampled_df,
                                         npartitions=3 * (multiprocessing.cpu_count() - 1))

            data_new_dd["nearest_synthetic_counterfactual_sparsity"] = data_new_dd.map_partitions(
                lambda df: df.apply(lambda row: self.get_nearest_synthetic_counterfactual(
                    feature_names=config["feature_names"], categorical_features=config["categorical_features_indexes"],
                    model=model, predictor=predictor, x_train=train_data_sampled.values,
                    numerical_features=numerical_features,
                    threshold=config["regression_threshold"],
                    instance=row[[column for
                                  column in data_new_dd.columns if
                                  column not in [config["id_column"],
                                                 "nearest_counterfactual_l1",
                                                 "nearest_counterfactual_l2",
                                                 "regression_value",
                                                 "nearest_synthetic_counterfactual_sparsity", "idx"]]]),
                                    axis=1),meta=('object')).compute(
                scheduler='processes')

            feature_changes_train = data_new_dd.map_partitions(lambda df: df.apply(
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
                                                                 "regression_value",
                                                                 "idx"]]],
                                               dictionary=row[["nearest_synthetic_counterfactual_sparsity"]]),
                axis=1),meta=('object')).compute(scheduler='processes')

            feature_imp_dict_train = feature_changes_train.apply(pd.Series).sum()
            num_records_train = train_data_sampled.shape[0]
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

            validation_data_new_dd = dd.from_pandas(validation_data,
                                                    npartitions=3 * (multiprocessing.cpu_count() - 1))

            validation_data_new_dd["nearest_synthetic_counterfactual_sparsity"] = validation_data_new_dd.map_partitions(
                lambda df: df.apply(lambda row: self.get_nearest_synthetic_counterfactual(
                    feature_names=config["feature_names"], categorical_features=config["categorical_features_indexes"],
                    model=model, predictor=predictor, x_train=validation_data.values,
                    numerical_features=numerical_features,
                    threshold=config["regression_threshold"],
                    instance=row[[column for
                                  column in data_new_dd.columns if
                                  column not in [config["id_column"],
                                                 "nearest_counterfactual_l1",
                                                 "nearest_counterfactual_l2",
                                                 "regression_value",
                                                 "nearest_synthetic_counterfactual_sparsity", "idx"]]]),
                                    axis=1),meta=('object')).compute(
                scheduler='processes')

            feature_changes_validation = validation_data_new_dd.map_partitions(lambda df: df.apply(
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
                                                                 "regression_value",
                                                                 "idx"]]],
                                               dictionary=row[["nearest_synthetic_counterfactual_sparsity"]]),
                axis=1),meta=('object')).compute(scheduler='processes')

            feature_changes_validation = feature_changes_validation.apply(pd.Series).sum()
            num_records_train = train_data_sampled.shape[0]
            feature_changes_validation = feature_changes_validation.to_dict()
            for key in config["feature_names"]:
                if key not in feature_changes_validation.keys():
                    feature_changes_validation[key] = 0

            feature_attribution_validation_df = pd.DataFrame.from_dict(feature_changes_validation, orient="index")

            feature_attribution_validation_df = feature_attribution_validation_df.reset_index()
            feature_attribution_validation_df.rename(
                columns={"index": "Column_Name", 0: "validation_attribution_value"},
                inplace=True)
            feature_attribution_validation_df["validation_attribution_value"] = feature_attribution_validation_df[
                                                                                    "validation_attribution_value"] / num_records_train
            feature_attribution_validation_df = feature_attribution_validation_df.sort_values(
                "validation_attribution_value",
                ascending=False)
            feature_attribution_validation_df = feature_attribution_validation_df.reset_index(drop=True).reset_index()
            feature_attribution_validation_df.rename(columns={"index": "validation_rank"}, inplace=True)
            feature_attribution_validation_df["validation_rank"] = feature_attribution_validation_df[
                                                                       "validation_rank"] + 1

            fin_df = feature_attribution_validation_df.merge(feature_attribution_train_df, on="Column_Name")
            fin_df['DCG'] = fin_df["train_attribution_value"] / np.log2(fin_df["validation_rank"] + 1)

            ndcg_score = fin_df['DCG'].sum() / fin_df['iDCG'].sum()
            drift_detected = True if ndcg_score < 0.9 else False
            fin_df["feature_drifted"] = np.where(fin_df["train_rank"] == fin_df["validation_rank"], 0, 1)
            fin_df["num_features_drifted"] = fin_df["feature_drifted"].sum()
            fin_df = fin_df.loc[:, ["Column_Name", "feature_drifted", "num_features_drifted"]]

            feature_attribution_df = pd.DataFrame({"ndcg_score": ndcg_score,
                                                   "drift_detected": drift_detected,
                                                   "validation_feature_attribution_df_aggregated": feature_attribution_validation_df.to_dict(
                                                       orient="records"),
                                                   "drift_info": fin_df.to_dict(orient='records')})

            feature_attribution_aggregated_validation_df = feature_attribution_df.loc[:,
                                                           ["validation_feature_attribution_df_aggregated",
                                                            "drift_info"]]
            #
            feature_attribution_aggregated_df = feature_attribution_df.loc[:, ["ndcg_score", "drift_detected"]].head(1)

            return feature_attribution_train_df, feature_attribution_aggregated_df, feature_attribution_aggregated_validation_df


        except Exception as error_message:
            logging.error(str(error_message))
            raise error_message
