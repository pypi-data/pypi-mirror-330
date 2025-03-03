from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error, median_absolute_error, \
    r2_score
import yaml
from src.utils.get_connections import  tiny_db_connection
from tinydb import Query
import pandas as pd
import logging
from timeit import default_timer as timer

class GenerateRegressionPerformanceScore():
    def __init__(self):
        logging.info("Started Regression Performance score Generation")

    def model_performance_report(self,y_val, y_pred, features):
        '''
        Show Model Performance Report
        Args:
            model (sklearn model): Pretrained Model
            x_val (pandas dataframe): Validation Dataset
            y_val (numpy array): True Labels
            y_pred_lab (numpy array): Predicted Labels
        Returns:
            Displays Streamit Metric Row consisting of All Model performance metric
        '''

        mae = mean_absolute_error(y_val, y_pred)
        mse = mean_squared_error(y_val, y_pred, squared=True)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        #m_log_e = mean_squared_log_error(y_val, y_pred)
        med_abs_er = median_absolute_error(y_val, y_pred)
        r2 = r2_score(y_val, y_pred)
        adjusted_r2 = 1 - ((1 - r2) *(len(y_val) - 1)) / (len(y_val) - len(features) - 1)
        d = {}
        d['Mean Absolute Error'] = mae
        d['Mean Squared Error'] = mse
        d['Root Mean Squared Error'] = rmse
        #d['Mean Squared Log Error'] = m_log_e
        d['Median Absolute Error'] = med_abs_er
        d['R Squared'] = r2
        d['Adjusted R Sqaured'] = adjusted_r2
        d["performance_score"] = adjusted_r2
        return d


    def run(self,config=None,y_val=None,predictor=None,val_data=None,model=None):
        logging.getLogger().setLevel(logging.INFO)
        start_time=timer()

        # query = Query()
        # data = validation_counterfactuals_collection.search(query.latest_record_ind == "Y")
        # y_pred = pd.Series([item["regression_value"] for item in data])

        y_pred = predictor.get_scores(X_data=val_data.to_numpy(), model=model)

        features = config["feature_names"]
        performance_dict = self.model_performance_report(y_val=y_val, y_pred=y_pred, features=features)
        logging.info("Performance Score Generation : " + str(round(timer() - start_time, 5)) + " sec")
        return performance_dict
