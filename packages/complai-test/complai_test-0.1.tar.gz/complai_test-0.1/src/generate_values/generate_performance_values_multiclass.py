from src.utils.performance_common_functions import model_performance_report
from src.utils.get_connections import  tiny_db_connection
from tinydb import Query
import pandas as pd
import numpy as np
import logging
from timeit import default_timer as timer

class GenerateMulticlassPerformanceScore():
    def __init__(self):
        logging.info("Started Multiclass Performance score Generation")


    def run(self,config=None,y_val=None,predictor=None,val_data=None,model=None):
        logging.getLogger().setLevel(logging.INFO)
        start_time=timer()
        db = tiny_db_connection(config["db_path"])
        # validation_counterfactuals_collection = db.table(config["validation_generated_values_collection"])
        # query = Query()
        # data = validation_counterfactuals_collection.search(query.latest_record_ind == "Y")
        # y_pred = pd.Series([item["prediction_label"] for item in data])

        try:
            y_pred=np.argmax(predictor.get_proba_scores(X_data=val_data,model=model),1)
        except ValueError:
            y_pred = np.argmax(predictor.get_proba_scores(X_data=val_data.to_numpy(), model=model), 1)



        performance_dict = model_performance_report(y_val=y_val, y_pred_lab=y_pred,
                                                    performance_metric=config["performance_metric"])
        logging.info("Performance Score Generation : " + str(round(timer() - start_time, 5)) + " sec")

        return performance_dict

