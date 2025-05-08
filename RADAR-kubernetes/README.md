# RADAR-Kubernetes

The Kubernetes stack of RADAR-base platform. The current repository is modified for testing purposes. It is currently being used for a TFM.

## Status

RADAR-Kubernetes is one of the youngest project of RADAR-base and will be the **long term supported form of deploying the platform**. Even though, RADAR-Kubernetes is being used in few production environments, it is still in its early stage of development. We are working on improving the set up and documentation to enable RADAR-base community to make use of the platform.

### Compatibility

Currently RADAR-Kubernetes is tested and supported on following component versions:
| Component | Version |
| ---- | ------- |
| Kubernetes | v1.23 to v1.26 |
| K3s | v1.23.17+k3s1 to v1.26.3+k3s1 |
| Kubectl | v1.23 to v1.26 |
| Helm | v3.11.3 |
| Helm diff | v3.6.0 |
| Helmfile | v0.152.0 |
| YQ | v4.33.3 |


## Prerequisites

### Hosting Infrastructure

| Component          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                | Required |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| Kubernetes cluster | An infrastructure with working installation of Kubernetes services. Read [this article](https://radar-base.atlassian.net/wiki/spaces/RAD/pages/2744942595?draftShareId=e09429e8-38c8-4b71-955d-5df8de94b694) for available options. Minimum requirements for a single node: 8 vCPU's, 32 GB memory, 200 GB storage. Minimum requirements for a cluster: 3 nodes with 3 vCPUs, 16 GB memory, 100 GB storage each and 200 GB shared storage. | Required |
| DNS Server         | Some applications are only accessible via HTTPS and it's essential to have a DNS server via providers like GoDaddy, Route53, etc                                                                                                                                                                                                                                                                                                           | Required |
| SMTP Server        | RADAR-Base needs an SMTP server to send registration email to researchers and participants.                                                                                                                                                                                                                                                                                                                                                | Required |
| Object storage     | An external object storage allows RADAR-Kubernetes to backup cluster data such as manifests, application configuration and data via Velero to a backup site. You can also send the RADAR-Base output data to this object storage, which can provider easier management and access compared to bundled Minio server inside RADAR-Kubernetes.                                                                                                | Optional |
| Managed services   | RADAR-Kubernetes includes all necessary components to run the platform as a standalone application. However, you can also opt to use managed services such as with the platform, e.g. Confluent cloud for Kafka and schema registry, Postgres DB for storage, Azure blob storage or AWS S3 instead of minio.                                                                                                                               | Optional |

### Local machine

The following tools should be installed in your local machine to install the RADAR-Kubernetes on your Kubernetes cluster.

| Component                                                          | Description                                                                                                                                                                                                      |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Git](https://git-scm.com/downloads)                               | RADAR-Kubernetes uses Git-submodules to use some third party Helm charts. Thus Git is required to properly download and sync correct versions of this repository and its dependent repositories                  |
| [Java](https://openjdk.java.net/install/)                          | The installation setup uses Java Keytools to create Keystore files necessary for signing access tokens.                                                                                                          |
| [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) | Kubernetes command-line tool, kubectl, allows you to run commands against Kubernetes clusters                                                                                                                    |
| [helm 3](https://github.com/helm/helm#install)                     | Helm Charts are used to package Kubernetes resources for each component                                                                                                                                          |
| [helmfile](https://github.com/helmfile/helmfile#installation)      | RADAR-Kubernetes uses helmfiles to deploy Helm charts.                                                                                                                                                           |
| [helm-diff](https://github.com/databus23/helm-diff#install)        | A dependency for Helmfile.                                                                                                                                                                                       |
| [yq](https://github.com/mikefarah/yq#install)                      | Used to run `init`, `generate-secrets` and `chart-updates` scripts.                                                                                                                                              |
| openssl                                                            | Used in `init` and `generate-secrets` scripts to generate secret for Prometheus Nginx authentication. This binary is in `openssl` package for Ubuntu, it's also easily available on other distributions as well. |

**Once you have a working installation of a Kubernetes cluster, please [configure Kubectl with the appropriate Kubeconfig](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#verify-kubectl-configuration) to enable Kubectl to find and access your cluster. Then proceed to the installation section.**

## Installation

> The following instructions on this guide are for local machines which runs on Linux operating systems. You can still use the same instructions with small to no changes on a MacOS device as well.

### Prepare

1. Clone the repository to your local machine by using following command.

   ```shell
   git clone https://github.com/RADAR-base/RADAR-Kubernetes.git
   ```

2. Run the initialization script to create basic configuration files.

   ```shell
   cd RADAR-Kubernetes
   bin/init
   ```

It is recommended make a private clone of this repository, if you want to version control your configurations and/or share with other people.

**You must keep `etc/secrets.yaml` secure and confidential once you have started installing the platform** and the best practice to share your platform configurations is by **sharing the encrypted version of `etc/secrets.yaml`**.

### Configure

#### Project Structure

- [/bin](bin): Contains initialization scripts
- [/etc](etc): Contains configurations for some Helm charts.
- [/secrets](secrets): Contains secrets configuration for helm charts.
- [/helmfile.d](helmfile.d): Contains Helmfiles for modular deployment of the platform
- [environments.yaml](environments.yaml): Defines current environment files in order to be used by helmfile. Read more about `bases` [here](https://github.com/roboll/helmfile/blob/master/docs/writing-helmfile.md).
- `etc/production.yaml`: Production helmfile template to configure and install RADAR-base components. Inspect the file to enable, disable and configure components required for your use case. The default helmfile enables all core components that are needed to run RADAR-base platform with pRMT and aRMT apps. If you're not sure which components you want to enable you can refer to wiki for [an overview and breakdown on RADAR-Base components and their roles](https://radar-base.atlassian.net/wiki/spaces/RAD/pages/2673967112/Component+overview+and+breakdown).
- `etc/production.yaml.gotmpl`: Change setup parameters that require Go templating, such as reading input files
- `etc/secrets.yaml`: Passwords and client secrets used by the installation.

1. Configure the [environments.yaml](environments.yaml) to use the files that you have created by copying the template files.
   ```shell
   nano environments.yaml # use the files you just created
   ```
2. Configure the `etc/production.yaml`. Optionally, you can also enable or disable other components that are configured otherwise by default.

   ```shell
   nano etc/production.yaml  # Change setup parameters and configurations
   ```

   When doing a clean install, you are advised to change the `postgresql`, `radar_appserver_postgresql` `radar_upload_postgresql` image tags to the latest PostgreSQL version. Likewise, the timescaledb image tag should use the latest timescaledb version. PostgreSQL passwords and major versions cannot easily be updated after installation.

3. In `etc/production.yaml.gotmpl` file, change setup parameters that require Go templating, such as reading input files and selecting an option for the `keystore.p12`

   ```shell
   nano etc/production.yaml.gotmpl
   ```

4. In `etc/secrets.yaml` file, change any passwords, client secrets or API credentials like for Fitbit or Garmin Connect.
   ```shell
   nano etc/secrets.yaml
   ```

### Install

Once all configuration files are ready, the RADAR-Kubernetes can be deployed on a Kubernetes cluster.

#### Install RADAR-Kubernetes on your cluster.

```shell
helmfile sync --concurrency 1
```

## Uninstall

If you want to remove the RADAR-base from your cluster you and use following command to delete the applications from cluster:

```shell
helmfile destroy
```

Some configurations can still linger inside the cluster. Try using following commands to purge them as well.

```shell
kubectl delete crd prometheuses.monitoring.coreos.com prometheusrules.monitoring.coreos.com servicemonitors.monitoring.coreos.com alertmanagers.monitoring.coreos.com podmonitors.monitoring.coreos.com alertmanagerconfigs.monitoring.coreos.com probes.monitoring.coreos.com thanosrulers.monitoring.coreos.com
kubectl delete psp kube-prometheus-stack-alertmanager kube-prometheus-stack-grafana kube-prometheus-stack-grafana-test kube-prometheus-stack-kube-state-metrics kube-prometheus-stack-operator kube-prometheus-stack-prometheus kube-prometheus-stack-prometheus-node-exporter
kubectl delete mutatingwebhookconfigurations prometheus-admission
kubectl delete ValidatingWebhookConfiguration prometheus-admission

kubectl delete crd certificaterequests.cert-manager.io certificates.cert-manager.io challenges.acme.cert-manager.io clusterissuers.cert-manager.io issuers.cert-manager.io orders.acme.cert-manager.io
kubectl delete pvc --all
kubectl -n cert-manager delete secrets letsencrypt-prod
kubectl -n default delete secrets radar-base-tls
kubectl -n monitoring delete secrets radar-base-tls
```
