
# APS_FAULT_DETECTION

- This repository contains the code and Docker setup for APS Fault Detection. Follow the instructions below to download and run the Docker image.

- This model is created in modular form to acces each stage of training pipeline differently

- It is a binary-classifier problem where target is `pos` and `neg` for detecting fault in vehicle air-pressure-system {aps}. 

- We are using XGBOOST with SIMPLE IMPUTER MEAN to achieve accuracy of 99.6% after testing and training the model on many different classifier 


## MODEL OVERVIEW AND PIPELINE

![MODEL ARCHITHECT](https://github.com/Harshit07979/apssensorfault/raw/main/notebookSensor/model%20architect.png)

![Training Pipeline](https://github.com/Harshit07979/apssensorfault/raw/main/notebookSensor/training%20pipeline.png)


## DATASET

The dataset consists of data collected from heavy Scania trucks in everyday usage. The system in focus is the “Air Pressure system (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes.” This is a 2-class problem, and the goal is to predict the failure of components in the APS system, given various inputs.

The training set labeled “SMALLER” is present in the Code/Dataset/ folder and has been down-sampled by factor of 3 (stratified), from the complete training set. The test set is also present in the same folder. The dataset has 171 attributes.

- To download the entire training data, visit the link: https://raw.githubusercontent.com/Harshit07979/apssensorfault/main/aps_failure_training_set1.csv

## Deployment
## PREREQUISITE
- Make sure you have Docker installed on your system. You can download Docker from [here](https://www.docker.com/products/docker-desktop).

To pull this project from docker run

```sh
  docker pull harshit00709/apsfaultdetection:latest
```

## RUNNIG DOCKER CONTAINER
- After downloading the image, you can run it using Docker Compose. Create a docker-compose.yaml file with the following content:

  version: '3.8'

  services:

    application:

    image: harshit00709/apsfaultdetection:latest

    container_name: sensor_app

    ports:
      - "8081:8080"

    environment:

      - MONGO_DB_URL=${MONGO_DB_URL}
    command:  ["python", "sensor/main.py"]

    volumes:

      - ./data:/app/data


## RUNNIG
```sh
docker-compose up
```


## NOTE

Please replace YOUR $(MONGO_DB_URL) with your MONGO url and 
/app/aps_fualt_detection_set1.csv is used for docker to to test .

