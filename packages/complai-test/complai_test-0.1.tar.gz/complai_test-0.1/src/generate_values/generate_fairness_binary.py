import pandas as pd
import numpy as np
import logging
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier
from nice.explainers import NICE
import dask.dataframe as dd
import dask
import multiprocessing
from multiprocessing.pool import Pool


class GenerateFairnessBinary():
    def __init__(self):
        logging.info("Started Binary Fairness Generation")

    def train_knn_model(self, X_df, numerical_features, categorical_features):
        numeric_features_pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='median'))])
        categorical_features_pipeline = Pipeline(steps=[('ohe', OneHotEncoder(handle_unknown='ignore'))])
        cat_feat_columns = [X_df.columns[i] for i in categorical_features]
        num_feat_columns = [X_df.columns[i] for i in numerical_features]
        preprocessor = ColumnTransformer(transformers=[
            ('num', numeric_features_pipeline, num_feat_columns),
            # transformer with name 'num' that will apply 'numeric_features_pipeline' to numeric_features
            ('cat', categorical_features_pipeline, cat_feat_columns)
            # transformer with name 'cat' that will apply 'categorical_features_pipeline' to categorical_features
        ])
        x = X_df.drop(['prediction_label'], axis=1)
        y = X_df['prediction_label']
        knn_clf = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('classifier',
                                   KNeighborsClassifier(n_neighbors=1, metric='manhattan', algorithm="brute"))])
        knn_clf.fit(x, y)
        return knn_clf

    def normalize_fn(self, X_mad_dict, numerical_features, df=None):
        df1 = df.copy()
        for i in numerical_features:
            df1.iloc[:, i] = df1.iloc[:, i].apply(lambda x: x / X_mad_dict[i])
        return df1

    def get_flip_score(self, f_plus, f_minus, n):
        return (abs(f_plus - f_minus) / n)

    def pred_lambda(self, x, **kwargs):
        adult_obj_new = kwargs["predictor"]
        prob_list = adult_obj_new.get_proba_scores(x, kwargs["model"])
        probability_score_series = np.where(prob_list > kwargs["threshold"], 1, 0)

        other_probability_score_series = 1 - probability_score_series

        return_obj = np.stack((probability_score_series, other_probability_score_series), axis=-1)
        return return_obj

    def get_nearest_synthetic_counterfactual(self, feature_names, NICE_model, instance,
                                             numerics=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']):
        try:

            instance = instance.values.reshape((1, len(feature_names)))
            CF = NICE_model.explain(instance)
            cf_df = pd.DataFrame(data=CF, columns=feature_names)
            numeric = cf_df.select_dtypes(include=numerics)
            numeric = numeric.apply(pd.to_numeric)
            non_numeric = cf_df.select_dtypes(include='object')
            cf_df_fin = pd.concat([numeric, non_numeric], axis=1)
            # cf_df = cf_df.apply(pd.to_numeric)
            return_obj = cf_df_fin.to_dict(orient='records')[0]

        except ValueError:
            return_obj = {}

        return return_obj

    def train_nearest_synthetic_counterfactual(self, x_train, method, threshold, numerical_features, model,
                                               categorical_features,
                                               predictor):
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

        prediction_function = lambda x: self.pred_lambda(x, model=model, threshold=threshold,
                                                         predictor=predictor)

        NICE_model = NICE(optimization=method, justified_cf=False)
        NICE_model.fit(X_train=x_train,
                       predict_fn=prediction_function,
                       y_train=None,
                       cat_feat=categorical_features,
                       num_feat=numerical_features)
        return NICE_model

    def run(self, config=None, validation_data=None, numerical_features=None, model=None, predictor=None):

        try:
            fairness_score_dict = {"fairness_info": {}}
            di_score_dict = {"di_info": {}}

            for column in config["protected_attributes"]:
                df_list = []
                for cls in validation_data[column].unique():
                    validation_data_cls = validation_data[validation_data[column] == cls]

                    Nice_obj_cls = self.train_nearest_synthetic_counterfactual(
                        x_train=validation_data_cls.values,
                        model=model, threshold=config["probability_threshold"],
                        predictor=predictor, numerical_features=numerical_features,
                        method="Sparsity", categorical_features=config["categorical_features_indexes"])
                    dask.config.set(pool=Pool(multiprocessing.cpu_count() - 1))
                    validation_data_cls_dd = dd.from_pandas(validation_data_cls,
                                                            npartitions=3 * (multiprocessing.cpu_count() - 1))
                    nearest_synthetic_counterfactual_sparsity_cls = validation_data_cls_dd.map_partitions(
                        lambda df: df.apply(lambda row: self.get_nearest_synthetic_counterfactual(
                            feature_names=config["feature_names"],
                            NICE_model=Nice_obj_cls, instance=row[config["feature_names"]]), axis=1),
                        meta='object').compute(scheduler='processes')
                    nearest_synthetic_counterfactual_sparsity_cls_df = nearest_synthetic_counterfactual_sparsity_cls.apply(
                        pd.Series)

                    validation_data_cls_fin = pd.concat(
                        [validation_data_cls, nearest_synthetic_counterfactual_sparsity_cls_df])
                    df_list.append(validation_data_cls_fin)

                fin_df = pd.concat(df_list)
                fin_df.drop_duplicates(inplace=True)

                X_mad_dict = {
                    i: (np.sum(abs(fin_df.values[:, i] - np.mean(fin_df.values[:, i]))) /
                        fin_df.values[:, i].shape[0]) for i in numerical_features}

                fin_df_normalized = self.normalize_fn(X_mad_dict=X_mad_dict, numerical_features=numerical_features,
                                                      df=fin_df)
                probability_scores = predictor.get_proba_scores(X_data=fin_df.to_numpy(),
                                                                model=model)
                fin_df_normalized["prediction_label"] = np.where(
                    probability_scores >= config["probability_threshold"], 1, 0)
                for cls in validation_data[column].unique():
                    total_count = fin_df_normalized.loc[
                        fin_df_normalized[column] == cls, column].count()

                    favoured_count = fin_df_normalized.loc[
                        (fin_df_normalized[column] == cls) & (
                                fin_df_normalized["prediction_label"] == config["prefered_class"]), column].count()

                    knn_clf = self.train_knn_model(X_df=fin_df_normalized[fin_df_normalized[column] != cls],
                                                   numerical_features=numerical_features,
                                                   categorical_features=config["categorical_features_indexes"])

                    f_plus = np.count_nonzero(knn_clf.predict(
                        fin_df_normalized[
                            (fin_df_normalized[column] == cls) & (
                                        fin_df_normalized["prediction_label"] != config["prefered_class"])]))

                    f_minus = np.count_nonzero(knn_clf.predict(
                        fin_df_normalized[
                            (fin_df_normalized[column] == cls) & (
                                        fin_df_normalized["prediction_label"] == config["prefered_class"])]) == 0)
                    print("Class",cls,"F minus",f_minus)

                    flip_score = self.get_flip_score(f_plus, f_minus,
                                                     fin_df_normalized[(fin_df_normalized[column] == cls)].shape[0])
                    fairness_score = (1 - flip_score)

                    try:
                        fairness_score_dict["fairness_info"][column][str(cls)] = fairness_score
                    except (KeyError, TypeError):
                        fairness_score_dict["fairness_info"].update({column: {str(cls): fairness_score}})

                    try:
                        di_score_dict["di_info"][column][str(cls)] = favoured_count / total_count
                    except (KeyError, TypeError):
                        di_score_dict["di_info"].update({column: {str(cls): favoured_count / total_count}})

            logging.info(fairness_score_dict)
            logging.info(di_score_dict)
            return fairness_score_dict, di_score_dict

        except Exception as error_message:
            logging.error(str(error_message))
            raise error_message
