import yaml
import pickle
import logging
import numpy as np
import pandas as pd
from timeit import default_timer as timer
import os
from src.extendables.get_data import GetData


class GenericGetData(GetData):
    def __init__(self, yaml_path=None):
        super().__init__()
        self.yaml_path = yaml_path

    def get_data(self):
        logging.getLogger().setLevel(logging.INFO)

        start_time = timer()

        with open(self.yaml_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)

        if config["categorical_features_indexes"] == [None]:
            config["categorical_features_indexes"] = []
        #
        with open(config["validation_raw_path"], "rb") as x_valid:
            validation_data = pickle.load(x_valid)

        with open(config["train_raw_path"], "rb") as x_train:
            x_train_data = pickle.load(x_train)

            # x_train_data=pd.read_csv(config["train_raw_path"])
            # validation_data = pd.read_csv(config["validation_raw_path"])

            y_val = validation_data[config["target_label_column"]]

        if config["target_label_column"]:
            x_train_data.drop(columns=[config["target_label_column"]], axis=1, inplace=True)

        if config["id_column"]:
            x_train_data.drop(columns=[config["id_column"]], axis=1, inplace=True)

        if isinstance(x_train_data, np.ndarray):
            x_train_data = x_train_data[~np.isnan(x_train_data).any(axis=1), :]
        elif isinstance(x_train_data, pd.DataFrame):
            x_train_data.dropna(inplace=True)
            x_train_data.to_numpy()

        else:

            raise TypeError("Train Data neither Pandas Dataframe nor Numpy Array")

        if isinstance(validation_data, np.ndarray):
            validation_data = validation_data[~np.isnan(validation_data).any(axis=1), :]
            validation_data_new = pd.DataFrame(validation_data, columns=config["feature_names"])
        elif isinstance(validation_data, pd.DataFrame):
            validation_data.dropna(inplace=True)
            validation_data_new = validation_data
        else:
            raise TypeError("Validation Data neither Pandas Dataframe nor Numpy Array")
        if config["target_label_column"]:
            validation_data_new.drop(columns=[config["target_label_column"]], axis=1, inplace=True)

        if config["id_column"]:
            validation_data_new_moified = validation_data_new.drop(columns=[config["id_column"]], axis=1)
        else:
            validation_data_new_moified = validation_data_new

        validation_data_new.dropna(inplace=True)
        logging.info(config["feature_names"])
        logging.info("Data Prep Time : " + str(round(timer() - start_time, 5)) + " sec")
        live_data_new_moified_lt = []
        for file in os.listdir(config["live_data_path"]):
            # print(os.path.join(config["live_data_path"],file))
            with open(os.path.join(config["live_data_path"], file), "rb") as live:
                live_data = pickle.load(live)

            if isinstance(live_data, np.ndarray):
                live_data = live_data[~np.isnan(validation_data).any(axis=1), :]
                live_data_new = pd.DataFrame(live_data, columns=config["feature_names"])
            elif isinstance(live_data, pd.DataFrame):
                live_data.dropna(inplace=True)
                live_data_new = live_data
            else:
                raise TypeError("Live Data neither Pandas Dataframe nor Numpy Array")

            if config["id_column"]:
                live_data_new_moified = live_data_new.drop(columns=[config["id_column"]], axis=1)
            else:
                live_data_new_moified = live_data_new
            if config["target_label_column"]:
                try:
                    live_data_new_moified.drop(columns=[config["target_label_column"]], axis=1, inplace=True)
                except KeyError:
                    pass

            live_data_new_moified_lt.append(live_data_new_moified)

        with open(config["prediction_model_path"], "rb") as model_file:
            model = pickle.load(model_file)

        logging.info("Data Prep Time : " + str(round(timer() - start_time, 5)) + " sec")

        return np.concatenate((x_train_data, validation_data_new_moified.to_numpy()),
                              axis=0), validation_data_new_moified, validation_data_new, live_data_new_moified_lt,\
               y_val, model, config, x_train_data
