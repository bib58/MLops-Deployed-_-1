# Vehicle Insurance Customer Interest Prediction
## 🛠️ End-to-End Production-Grade MLOps Pipeline

[![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139.0-green.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-emerald.svg?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20ECR%20%7C%20EC2-orange.svg?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-darkred.svg?style=flat&logo=github-actions&logoColor=white)](https://github.com/features/actions)

An enterprise-grade, end-to-end MLOps pipeline designed to predict customer interest in vehicle insurance. The project demonstrates standard software engineering best practices applied to Machine Learning, covering remote data fetching, validation schemas, class imbalance resolution, model performance-based promotion, S3 model registry, Docker packaging, and automated CI/CD deployment onto AWS EC2 using a GitHub self-hosted runner.

---

## 📸 Screenshots & UI Previews

Below are visual proofs of the pipeline components, system execution logs, database entries, and live server deployments.

<img src="Screenshot%202026-07-18%20144754.png">

<img src="Screenshot%202026-07-18%20202523.png">

<img src="Screenshot%202026-07-18%20205851.png">

---

## ✨ Features & Best Practices

*   **Robust Data Architecture:** Data is dynamically extracted from a remote **MongoDB Atlas** cluster and partitioned into stratified training and testing sets.
*   **Dynamic Data Validation:** An automated pipeline checks the schema, column count, and types against a definition file.
*   **Imbalanced Data Handling:** Implements **SMOTEENN** (Synthetic Minority Over-sampling Technique + Edited Nearest Neighbors) to balance the minority class (interested customers) and remove noisy data boundary points.
*   **Pipeline Serialization:** Uses the **Dill** library to serialize the custom model wrapper containing both the preprocessing transformer (`ColumnTransformer` utilizing `StandardScaler` and `MinMaxScaler`) and the trained `RandomForestClassifier` into a single deployable object.
*   **Promotional Evaluation (Model Registry):** Evaluates newly trained models against the active production model in **AWS S3** on a test dataset. Pushes the new model to S3 *only* if it outperforms the production model by a configured threshold.
*   **REST API Layer:** Built on **FastAPI** with template integration. Provides an interactive UI for single predictions and a `/train` endpoint to trigger the entire training pipeline on demand.
*   **Continuous Integration & Deployment (CI/CD):** Configured via GitHub Actions to build a **Docker image**, push it to **AWS ECR**, connect to a self-hosted runner on **AWS EC2**, and spin up a hot-reloaded Docker container mapped to the public port.

---

## Local Setup & Development

Follow these steps to configure and run the project locally.

### 1. Prerequisites & Environment Setup

Ensure you have [Conda](https://docs.anaconda.com/anaconda/install/) installed.

```bash
conda create -n vehicle_proj python=3.10 -y
conda activate vehicle_proj

pip install -r requirements.txt

pip install -e .
```

### 2. Configure Environment Variables
```env
MONGODB_URL="your-mongodb-connection-string"
DATABASE_NAME="vehicle-insurance"
COLLECTION_NAME="customer-data"
AWS_ACCESS_KEY_ID="your-aws-access-key"
AWS_SECRET_ACCESS_KEY="your-aws-secret-access-key"
AWS_DEFAULT_REGION="us-east-1"
S3_bucket="your-model-bucket-name"
ECR_REPO="your-aws-ecr-repository-uri"
APP_HOST="0.0.0.0"
APP_PORT=5000
```

### 3. Launching the App Locally

Start the FastAPI application server:

```bash
python app.py
```

*   **Prediction Frontend:** Navigate to `http://localhost:5000` to interact with the prediction UI.
*   **Trigger Model Training:** Send a GET request to `http://localhost:5000/train` to download fresh data from MongoDB and run the full training pipeline.

---

## 🚀 production CI/CD & Deployment Guide

This section outlines the automated pipeline built to serve models in production.

### AWS Infrastructure Setup

1.  **IAM Security User:**
    *   Create an IAM user with `AdministratorAccess`.
    *   Generate **Access Keys** for CLI use and note down the access key ID and secret access key.
2.  **AWS S3 Bucket:**
    *   Create an S3 bucket in your region (e.g. `us-east-1`) to serve as the remote model registry.
3.  **Amazon ECR Repository:**
    *   Create a private repository (e.g. named `vehicle_proj`) to host the Docker images. Keep the repository URI handy.
4.  **AWS EC2 Instance:**
    *   Launch an EC2 Ubuntu Server instance (Ubuntu 24.04 LTS).
    *   Ensure the security group allows **Inbound TCP Traffic** on port `5080`.


### Configure the self-hosted GitHub actions runner:
1.  Go to your GitHub repository -> **Settings** -> **Actions** -> **Runners** -> **New self-hosted runner**.
2.  Select **Linux** as runner OS.
3.  Execute the configuration steps generated by GitHub on the EC2 terminal (leave runner group and labels default, or name the runner `self-hosted`).
4.  Start the runner on the server:
    ```bash
    ./run.sh
    ```

### GitHub Secrets Configuration

Add these variables under **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**:

| Secret Key | Description |
| :--- | :--- |
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
| `AWS_DEFAULT_REGION` | The region of your ECR and S3 bucket (e.g., `us-east-1`) |
| `ECR_REPO` | The ECR repository name only (excluding registry URL) |
| `MONGODB_URL` | The MongoDB Atlas connection string |

Once these are set, pushing a commit to `main` will automatically trigger the CI/CD pipeline, building the Docker image, pushing it to ECR, and prompting the self-hosted runner to launch the updated app container on port `5080` (`-p 5000:5000` mapping internal container port `5000` outwards).
