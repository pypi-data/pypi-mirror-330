import logging
from timeit import default_timer as timer
from src.utils.get_connections import tiny_db_connection
import numpy as np


class GenerateLivePredictions():
    def __init__(self):
        logging.info("Started Binary Performance score Generation")

    def get_live_prob_scores(self, live_data=None, predictor=None, model=None, collection=None, problem_type="binary"):

        for data in live_data:

            start_time = timer()
            logging.getLogger().setLevel(logging.INFO)
            if problem_type == "binary":
                probability_scores = predictor.get_proba_scores(X_data=data.to_numpy(), model=model)

                data["probability_score"] = probability_scores

            elif problem_type == "multiclass":
                probability_scores = predictor.get_proba_scores(X_data=data.to_numpy(), model=model)

                for i in range(probability_scores.shape[1]):
                    data["pred_proba_scores" + "_" + str(i)] = probability_scores[:, i]

                data["pred_proba_scores"] = data[
                    [column for column in data.columns if
                     column.startswith("pred_proba_scores")]].apply(
                    lambda x: list(x), axis=1)
                data.drop(columns=[column for column in data.columns if
                                   column.startswith(
                                       "pred_proba_scores") and column != "pred_proba_scores"], inplace=True)
            else:
                regression_values = predictor.get_scores(X_data=data.to_numpy(), model=model)
                data["regression_values"] = regression_values

            yield {"data": data.to_dict(orient='records')}

    def run(self, config=None, live_data=None, predictor=None, model=None, problem_type="binary"):

        start_time = timer()

        # db = tiny_db_connection(config["db_path"])
        # live_predictions_collection = db.table(config["live_prediction_values_collection"])
        # live_predictions_collection.update({'latest_record_ind': 'N'})

        live_list = list(
            self.get_live_prob_scores(live_data=live_data, predictor=predictor, model=model, problem_type=problem_type))

        # live_predictions_df = pd.concat(live_predictions,axis=0)

        logging.info("Live Predictions Generation : " + str(round(timer() - start_time, 5)) + " sec")

        return live_list
