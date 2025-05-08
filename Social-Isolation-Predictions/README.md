# Project: **Social Isolation Prediction**

## 📘 Introduction

The development of the framework consists of 3 parts: RADARBASE which can be found at the following link: https://github.com/ecariel/RADAR-kubernetes, the prediction of social isolation present in this repository and the visualization which is done using Elasticsearch and Kibana.

## 🛠️ Use monitoring predictions

1. Image your-user/modelos-image:latest: Build this image from the models-image/ directory:

   ```shell
   cd modelos-image/
   docker build -t tu-usuario/modelos-image:latest .
   docker push tu-usuario/modelos-image:latest
   cd ..
   ```

2. Image monitoring-prediction:latest:

   ```shell
   docker build -t tu-usuario/monitor-prediccion:latest .
   docker push tu-usuario/monitor-prediccion:latest
   ```

3. Deployment

   ```shell
   kubectl apply -f deployment.yaml
   ```
