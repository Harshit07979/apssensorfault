import os
from sensor.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME, MODEL_FILE_NAME, TARGET_ENCODER_OBJECT_FILE_NAME
from glob import glob
from typing import Optional
import logging

#to read , loacte and save models
class ModelResolver:
    """
    A class to resolve the latest model, transformer, and target encoder paths and to save new ones.

    Attributes:
    ----------
    model_registry : str
        The directory where models are stored.
    transformer_dir_name : str
        The directory name for the transformer object.
    target_encoder_dir_name : str
        The directory name for the target encoder object.
    model_dir_name : str
        The directory name for the model object.

    Methods:
    -------
    get_latest_dir_path() -> Optional[str]
        Returns the path of the latest directory in the model registry.
    get_latest_model_path() -> str
        Returns the path of the latest model file.
    get_latest_transformer_path() -> str
        Returns the path of the latest transformer file.
    get_latest_target_encoder_path() -> str
        Returns the path of the latest target encoder file.
    get_latest_save_dir_path() -> str
        Returns the path for saving a new model, transformer, and target encoder.
    get_latest_save_model_path() -> str
        Returns the path for saving a new model file.
    get_latest_save_transformer_path() -> str
        Returns the path for saving a new transformer file.
    get_latest_save_target_encoder_path() -> str
        Returns the path for saving a new target encoder file.
    """

    def __init__(self, model_registry: str = "saved_models", transformer_dir_name: str = "transformer", 
                 target_encoder_dir_name: str = "target_encoder", model_dir_name: str = "model"):
        """
        Constructs all the necessary attributes for the ModelResolver object.

        Parameters:
        ----------
        model_registry : str
            The directory where models are stored (default is "saved_models").
        transformer_dir_name : str
            The directory name for the transformer object (default is "transformer").
        target_encoder_dir_name : str
            The directory name for the target encoder object (default is "target_encoder").
        model_dir_name : str
            The directory name for the model object (default is "model").
        """
        self.model_registry = model_registry
        os.makedirs(self.model_registry, exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.target_encoder_dir_name = target_encoder_dir_name
        self.model_dir_name = model_dir_name
        logging.info(f"Initialized ModelResolver with model registry: {self.model_registry}")

    def get_latest_dir_path(self) -> Optional[str]:
        """
        Returns the path of the latest directory in the model registry.

        Returns:
        -------
        Optional[str]
            The path of the latest directory or None if no directories exist.
        """
        try:
            #we have models storedd like in 0,1,2,3 subfolder for every new model
            dir_names = os.listdir(self.model_registry)
            if len(dir_names) == 0:
                logging.warning("No directories found in the model registry.")
                return None
            #mapping model.pkl file present in 0,1,2,3 subfolder in integer form
            dir_names = list(map(int, dir_names))
            #sorting the list of directories in ascending order
            #and taking the latest as lates will have maximum integer
            latest_dir_name = max(dir_names)
            logging.info(f"Latest directory found: {latest_dir_name}")
            return os.path.join(self.model_registry, f"{latest_dir_name}")
        except Exception as e:
            logging.error(f"Error occurred while fetching the latest directory path: {e}")
            raise e

    def get_latest_model_path(self) -> str:
        """
        Returns the path of the latest model file.

        Returns:
        -------
        str
            The path of the latest model file.
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                logging.error("Model is not available.")
                raise Exception("Model is not available")
            model_path = os.path.join(latest_dir, self.model_dir_name, MODEL_FILE_NAME)
            logging.info(f"Latest model path: {model_path}")
            return model_path
        except Exception as e:
            logging.error(f"Error occurred while fetching the latest model path: {e}")
            raise e

    def get_latest_transformer_path(self) -> str:
        """
        Returns the path of the latest transformer file.

        Returns:
        -------
        str
            The path of the latest transformer file.
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                logging.error("Transformer is not available.")
                raise Exception("Transformer is not available")
            transformer_path = os.path.join(latest_dir, self.transformer_dir_name, TRANSFORMER_OBJECT_FILE_NAME)
            logging.info(f"Latest transformer path: {transformer_path}")
            return transformer_path
        except Exception as e:
            logging.error(f"Error occurred while fetching the latest transformer path: {e}")
            raise e

    def get_latest_target_encoder_path(self) -> str:
        """
        Returns the path of the latest target encoder file.

        Returns:
        -------
        str
            The path of the latest target encoder file.
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                logging.error("Target encoder is not available.")
                raise Exception("Target encoder is not available")
            target_encoder_path = os.path.join(latest_dir, self.target_encoder_dir_name, TARGET_ENCODER_OBJECT_FILE_NAME)
            logging.info(f"Latest target encoder path: {target_encoder_path}")
            return target_encoder_path
        except Exception as e:
            logging.error(f"Error occurred while fetching the latest target encoder path: {e}")
            raise e

    def get_latest_save_dir_path(self) -> str:
        """
        Returns the path for saving a new model, transformer, and target encoder.

        Returns:
        -------
        str
            The path for saving a new model, transformer, and target encoder.
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                save_dir_path = os.path.join(self.model_registry, f"{0}")
                logging.info(f"Latest save directory path: {save_dir_path}")
                return save_dir_path
            latest_dir_num = int(os.path.basename(latest_dir))
            save_dir_path = os.path.join(self.model_registry, f"{latest_dir_num + 1}")
            logging.info(f"Latest save directory path: {save_dir_path}")
            return save_dir_path
        except Exception as e:
            logging.error(f"Error occurred while fetching the latest save directory path: {e}")
            raise e

    def get_latest_save_model_path(self) -> str:
        """
        Returns the path for saving a new model file.

        Returns:
        -------
        str
            The path for saving a new model file.
        """
        try:
            latest_save_dir = self.get_latest_save_dir_path()
            model_save_path = os.path.join(latest_save_dir, self.model_dir_name, MODEL_FILE_NAME)
            logging.info(f"Latest save model path: {model_save_path}")
            return model_save_path
        except Exception as e:
            logging.error(f"Error occurred while fetching the latest save model path: {e}")
            raise e

    def get_latest_save_transformer_path(self) -> str:
        """
        Returns the path for saving a new transformer file.

        Returns:
        -------
        str
            The path for saving a new transformer file.
        """
        try:
            latest_save_dir = self.get_latest_save_dir_path()
            transformer_save_path = os.path.join(latest_save_dir, self.transformer_dir_name, TRANSFORMER_OBJECT_FILE_NAME)
            logging.info(f"Latest save transformer path: {transformer_save_path}")
            return transformer_save_path
        except Exception as e:
            logging.error(f"Error occurred while fetching the latest save transformer path: {e}")
            raise e

    def get_latest_save_target_encoder_path(self) -> str:
        """
        Returns the path for saving a new target encoder file.

        Returns:
        -------
        str
            The path for saving a new target encoder file.
        """
        try:
            latest_save_dir = self.get_latest_save_dir_path()
            target_encoder_save_path = os.path.join(latest_save_dir, self.target_encoder_dir_name, TARGET_ENCODER_OBJECT_FILE_NAME)
            logging.info(f"Latest save target encoder path: {target_encoder_save_path}")
            return target_encoder_save_path
        except Exception as e:
            logging.error(f"Error occurred while fetching the latest save target encoder path: {e}")
            raise e
