# 📁 radar_social_isolation
RADAR-BASE deployment and ELSA Analytics for Social Isolation

## 📂 Folders

- [**/RADAR-Questionnaire**](./RADAR-Questionnaire)  
  It contains the files necessary to build the mobile app in its beta phase, as well as the instructions for its implementation. The app is based on the app implemented for the RADAR-base platform, which focuses on conducting self-reported surveys.

- [**/RADAR-REDCap-aRMT-Definitions**](./RADAR-REDCap-aRMT-Definitions)  
  This folder contains REDCap Metadata Definition files for questionnaires used in the aRMT (RADAR-Questionnarie), aRMT reformatted payloads and a REDCAP to aRMT convertor. Same, this folder contain all [**questionnaires**](./RADAR-REDCap-aRMT-Definitions/questionnaires)  that implement in the project (UCLA, Girlverld, etc).

- [**/RADAR-Schemas**](./RADAR-Schemas)  
  Avro schemas are organized into several subdirectories within the commons directory, each with a specific purpose: active for active collection schemas (such as questionnaires), catalog for classifying data types, kafka for common keys in Kafka, monitor for application monitoring, passive for data from passive devices (such as wearables), and stream for Kafka Streams. Additionally, the specifications directory defines what data is collected on a device-by-device basis. Java SDKs, located in java-sdk, are automatically generated from these schemas.

- [**/RADAR-aRMT-protocols**](./RADAR-aRMT-protocols)  
  This folder specify each one of protocols or projects defined in the management portal, your version and specific questionnaire that will implement.

- [**/RADAR-Kubernetes**](./RADAR-Kubernetes)  
  The Kubernetes stack of RADAR-base platform, contain all files for implement the cluster of kubernetes with the specifies that the project and describe the characteristics minium that cluster.

- [**/Social-Isolation-Predictions**](./Social-Isolation-Predictions)  
  It contains the implementation of the necessary PDs to include them in the Kubernetes cluster already launched with RADAR-Base, as well as the prediction models built to determine the level of social isolation from ELSA data.

---

✨ Haz clic en cualquier carpeta para navegar directamente.
