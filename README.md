# MLOps with MLFlow and DVC

# 📋 Workflows

1. Update `config.yaml`
2. Update `schema.yaml` _[For validation]_
3. Update `params.yaml` _[For training]_
4. Update the entity
5. Update the configuration manager in `src/config`
6. Update the components
7. Update the pipeline
8. Update the `main.py`
9. Update the `dvc.yaml`

# 🐶 [Dagshub](https://dagshub.com/)

```
MLFLOW_TRACKING_URI=https://dagshub.com/your_username/your_project_name.mlflow \
MLFLOW_TRACKING_USERNAME=your_username \
MLFLOW_TRACKING_PASSWORD=your_token \
python script.py
```

Run the following commands to export as environment variables:

```bash
export MLFLOW_TRACKING_URI=https://dagshub.com/your_username/your_project_name.mlflow
export MLFLOW_TRACKING_USERNAME=your_username
export MLFLOW_TRACKING_PASSWORD=your_token
```

Or you can create an `.env` file in the root directory:

```env
MLFLOW_TRACKING_URI=https://dagshub.com/your_username/your_project_name.mlflow
MLFLOW_TRACKING_USERNAME=your_username
MLFLOW_TRACKING_PASSWORD=your_token
```

Edit the `.env.example` file and rename it to `env` when done.

# 🌊 [MLFlow](https://mlflow.org/) on [AWS](https://aws.amazon.com)

## 🔧 Set Up

1. Login to AWS Console

2. Create IAM user with policy `AdministratorAccess`

3. Select the user created and head to `Security credentials`

   - Under `Access keys` click on `Create access key` and select the `Command Line Interface` (CLI) option

   - Once the access key has been created, you can download as a `.csv` file which will store your AWS access key and secret access key

4. Ensure you have AWS CLI installed or head to this [installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install according to your OS

5. Run the command `aws configure` and paste the access key and secret access key from step 3

   ```bash
   aws configure

   AWS Access Key ID [None]: # paste access key here
   AWS Secret Access Key [None]: # paste secret access key here
   Default region name [None]: # example: us-east-1
   Default output format [None]: # enter to skip
   ```

6. Create a S3 bucket

   - Ensure the AWS Region is set to the same region you specified in step 5

   - Uncheck `Block all public access` and acknowledge the current settings

7. Create an EC2 machine (Ubuntu)

   - Under `Key pair (login)`, click on `Create new key pair`

   - Next, under `Network settings` check thw following:

     - `Allow HTTPS traffic from the internet`
     - `Allow HTTP traffic from the internet`

8. Click the `Instance ID` of the newly created EC2 instance

   - Select the `Security` tab and click on the link under `Securtiy groups`

   - Click on `Edit inbound rules`

   - `Add rule`

   - Ensure:

     - `Type` is `Custom TCP`,
     - `Port range` is set to `5000` and
     - `CIDR blocks` to `0.0.0.0/0`

9. Head back to the EC2 instance and click on `Connect`

10. Run the following commands in the Ec2 instance:

    ```bash
    sudo update

    sudo apt install python3-pip
    sudp pip3 install pipenv
    sudo pip3 install virtualenv

    mkdir mlflow
    cd mlflow

    pipenv install mlflow
    pipenv install awscli
    pipenv install boto3
    pipenv shell # activate virtual environment

    aws configure # set credentials (see step 5)

    mlflow server -h 0.0.0.0 --default-artifact-root s3://mlflow-bucket-01
    ```

11. Next, in the EC2 instance, open the `Public IPv4 DNS` address in the browser

    - Change the `https` to `http`

    - Add `:5000` to the end of the URI

12. The URI in step 11 will be your `MLFLOW_TRACKING_URI`

    ```bash
    export MLFLOW_TRACKING_URI=http://...amazonaws.com:5000
    ```

    Similarly, you can add it into the `.env` file.

# ⚙️ AWS CI/CD Deployment with GitHub Actions

1.  Login to AWS Console

2.  Create IAM user with policy `AmazonEC2FullAccess` and `AmazonEC2ContainerRegistryFullAccess`

3.  Select the user created and head to `Security credentials`

    - Under `Access keys` click on `Create access key` and select the `Command Line Interface` (CLI) option

    - Once the access key has been created, you can download as a `.csv` file which will store your AWS access key and secret access key

4.  Create Elastic Container Registry (ECR) repository to store/save Docker image

    - Ensure `Visibility settings` is set to `private`

    - Enter your repository name and click on `Create repository`

    - Once created, copy the URI

    ```bash
    797496359327.dkr.ecr.ap-southeast-2.amazonaws.com/name_of_repository
    ```

5.  Create an EC2 machine (Ubuntu)

    - Under `Key pair (login)`, click on `Create new key pair`

    - Next, under `Network settings` check thw following:

      - `Allow HTTPS traffic from the internet`
      - `Allow HTTP traffic from the internet`

6.  Connect to EC2 and install Docker

    - Click the `Instance ID` of the newly created EC2 instance

    - Connect to the instance by clicking on `Connect`

    ```bash
     sudo apt-get update -y
     sudo apt-get upgrade
     curl -fsSL https://get.docker.com -o get-docker.sh
     sudo sh get-docker.sh
     sudo usermod -aG docker ubuntu
     newgrp docker
    ```

    - Verify Docker is installed by running:

    ```bash
    docker --version
    ```

7.  Configure EC2 as self-hosted runner

    - Go to your project GitHub repository

    - Click on `Settings` > `Actions` > `Runners` > `New self-hosted runner`

    - Under `Runner image` select `Linux`

    - Execute the following commands in the EC2 instance:

      **Download**

    ```bash
    # Create a folder
    mkdir actions-runner && cd actions-runner
    # Download the latest runner package
    curl -o actions-runner-linux-x64-2.313.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.313.0/actions-runner-linux-x64-2.313.0.tar.gz
    # Optional: Validate the hash
    echo "56910d6628b41f99d9a1c5fe9df54981ad5d8c9e42fc14899dcc177e222e71c4  actions-runner-linux-x64-2.313.0.tar.gz" | shasum -a 256 -c
    # Extract the installer
    tar xzf ./actions-runner-linux-x64-2.313.0.tar.gz
    ```

    **Configure**

    ```bash
    # Create the runner and start the configuration experience
    ./config.sh --url https://github.com/Wilsven/mlops-with-mlflow-dvc --token APL542DAQXQ2EZ6PH2WYZ5DF35QSC
    ```

    **Note:** Press Enter and type "self-hosted", press Enter when asked for additional labels and finally, press Enter again when asked for name of folder.

    ```bash
    # Last step, run it!
    ./run.sh
    ```

    - When you return to the `Runner` page in GitHub, you should see an `idle` status

8.  Setup GitHub secrets

    - Go to your project GitHub repository

    - Click on `Settings` > `Secrets and variables` > `Actions` > `New repository secret`

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
AWS_ECR_LOGIN_URI=
ECR_REPOSITORY_NAME=
```
