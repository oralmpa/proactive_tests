import os, sys
import pandas as pd
[sys.path.append(os.path.join(os.getcwd(), folder)) for folder in variables.get("dependent_modules_folders").split(",")]
from classes import preprocessing_functions
from helpers.logger import LoggerHelper, logging
import proactive_helper as ph

LoggerHelper.init_logger()
logger = logging.getLogger(__name__)

input_data_folder = variables.get("InputData")
dataset_id = "mevlon_electrical_anomalies_1722420423"
project_id = "mevlon-idekotest-1722419911"
indicator_list = ["f3"]
ph.read_data_from_zenoh(project_id, dataset_id)
#print(dataset_id)
#X, Y = preprocessing_functions.read_data(input_data_folder, indicator_list)
logger.info("Summary of timeseries length %s" %pd.Series([len(x) for x in X]).describe())

print("*****")
print(variables.get("text_to_print"))
print("*****")

#ph.save_datasets(variables, ("X", X), ("Y", Y), ("indicator_list", indicator_list))
