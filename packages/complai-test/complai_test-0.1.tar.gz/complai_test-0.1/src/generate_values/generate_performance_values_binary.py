from src.utils.get_connections import  tiny_db_connection
from src.utils.performance_common_functions import model_performance_report
import numpy as np
import logging
from timeit import default_timer as timer

class GenerateBinaryPerformanceScore():
    def __init__(self):
        logging.info("Started Binary Performance score Generation")




    def run(self,config=None,y_val=None,predictor=None,val_data=None,model=None):
        logging.getLogger().setLevel(logging.INFO)
        start_time=timer()

        # validation_counterfactuals_collection = db.table(config["validation_generated_values_collection"])
        # query = Query()
        # data = validation_counterfactuals_collection.search(query.latest_record_ind == "Y")
        # y_pred = pd.Series([item["prediction_label"] for item in data])

        probability_scores = predictor.get_proba_scores(X_data=val_data.to_numpy(), model=model)

        y_pred = np.where(
            probability_scores >= config["probability_threshold"], 1, 0)

        performance_dict = model_performance_report(y_val=y_val, y_pred_lab=y_pred,
                                                    performance_metric=config["performance_metric"])
        logging.info("Performance Score Generation : " + str(round(timer() - start_time, 5)) + " sec")

        return performance_dict




