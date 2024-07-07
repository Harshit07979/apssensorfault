
# from sensor.pipeline.training_pipeline import start_training_pipeline
# from sensor.pipeline.batch_prediction import start_batch_prediction

# file_path="/config/workspace/aps_failure_training_set1.csv"

from sensor.exception import SensorException

try:
    # Code that might raise an exception
    raise ValueError("This is a test error")
except ValueError as e:
    raise SensorException(e, sys)

print(__name__)
if __name__=="__main__":
     try:
          #start_training_pipeline()
          output_file = start_batch_prediction(input_file_path=file_path)
          print(output_file)
     except Exception as e:
          print(e)