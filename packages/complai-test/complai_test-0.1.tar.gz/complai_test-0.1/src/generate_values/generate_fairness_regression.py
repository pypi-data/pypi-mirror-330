import pandas as pd
import numpy as np
import logging
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier


class GenerateFairnessRegression():
    def __init__(self):
        logging.info("Started Regression Fairness Generation")

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

    def run(self,config=None,numerical_features=None,db=None):

        try:

            validation_counterfactuals_collection = db.table(config["validation_generated_values_collection"])

            validation_counterfactuals_data = validation_counterfactuals_collection.all()

            validation_counterfactuals_data_list = [
                {k: v for k, v in item.items() if
                 k in config["feature_names"] + ["regression_value", "nearest_synthetic_counterfactual_sparsity"]} for item
                in
                validation_counterfactuals_data]
            validation_counterfactuals_data_df = pd.DataFrame(validation_counterfactuals_data_list)
            prediction_label_cf = np.where(
                (validation_counterfactuals_data_df["regression_value"] >= config["prefered_class_lower_limit"]) & (
                        validation_counterfactuals_data_df["regression_value"] <= config["prefered_class_upper_limit"]),
                1, 0)
            synthethic_df = validation_counterfactuals_data_df["nearest_synthetic_counterfactual_sparsity"].apply(pd.Series)
            synthethic_df["regression_value"] = prediction_label_cf
            validation_counterfactuals_data_df.drop(columns=["nearest_synthetic_counterfactual_sparsity"], inplace=True)
            validation_data = pd.concat([validation_counterfactuals_data_df, synthethic_df])

            # dask.config.set(pool=Pool(multiprocessing.cpu_count() - 1))
            # validation_data_new_dd = dd.from_pandas(validation_data,
            #                                         npartitions=3 * (multiprocessing.cpu_count() - 1))

            fairness_score_dict = {"fairness_info": {}}
            di_score_dict = {"di_info": {}}

            for column in config["protected_attributes"]:

                X_mad_dict = {i: (np.sum(abs(validation_data.values[:, i] - np.mean(validation_data.values[:, i]))) /
                                  validation_data.values[:, i].shape[0]) for i in numerical_features}

                fin_df_normalized = self.normalize_fn(X_mad_dict=X_mad_dict, numerical_features=numerical_features,
                                                      df=validation_data)

                for cls in validation_data[column].unique():
                    total_count = validation_data.loc[
                        validation_data[column] == cls, column].count()
                    favoured_count = validation_data.loc[
                        (validation_data[column] == cls) & (
                                validation_data["prediction_label"] == config["prefered_class"]), column].count()
                    knn_clf = self.train_knn_model(X_df=fin_df_normalized[fin_df_normalized[column] != cls],
                                                   numerical_features=numerical_features,
                                                   categorical_features=config["categorical_features_indexes"])

                    f_plus = np.count_nonzero(knn_clf.predict(
                        fin_df_normalized[
                            (fin_df_normalized[column] == cls) & (fin_df_normalized["regression_value"] != config["prefered_class"])]))
                    f_minus = np.count_nonzero(knn_clf.predict(
                        fin_df_normalized[
                            (fin_df_normalized[column] == cls) & (fin_df_normalized["regression_value"] == config["prefered_class"])]) == 0)

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
            return fairness_score_dict,di_score_dict


        except Exception as error_message:
            logging.error(str(error_message))
            raise error_message
