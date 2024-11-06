# Email Notification
This repository provides sample python code to send email using Gmail SMTP server. It includes a sample script and instructions for deploying it as a Cloud Run Job, enabling automated or scheduled email notifications.

## Set configuration.yaml
This YAML file stores the email settings to be used in the Cloud Run Job. Please refer to the description of each setting item below for configuration.

EmailConfig:

- **Sender**: Enter the sender's Gmail address.
- **Password**: Enter the Gmail app password. An app password is used to obtain the sender's Gmail credentials. Refer to the [Gmail app password creation](https://support.google.com/accounts/answer/185833) and create one.
- **Subject**: Enter the email subject.
- **Body**: Enter the email body text. To enter multiple lines of text, use the | symbol, and each line must maintain indentation.
- **DefaultRecipients**: Enter the list of recipients who will receive the email by default. If there are multiple recipients, list each recipient using the - symbol.


## Set Env variables
```
export PROJECT_ID=[YOUR PROJECT ID]
export REGION=asia-northeast3
export CLOUD_RUN_JOB_NAME=email-noti-job
export SERVICE_ACCOUNT_NAME=[Your service account name]
export SERVICE_ACCOUNT_EMAIL=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com
```

## Gcloud init
```
gcloud auth login

gcloud config set project $PROJECT_ID
```


## Enable Cloud Run Admin API and Cloud Build API
```
gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com
```

## Create a service account for cloud run job
```
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
  --description="Email Notification Job SA" 
```

## Assign IAM roles to the service account
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$SERVICE_ACCOUNT_EMAIL \
    --role=roles/cloudbuild.builds.builder

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$SERVICE_ACCOUNT_EMAIL \
    --role=roles/run.sourceDeveloper
```


## Cloud Run Job Deployment

```
gcloud run jobs deploy $CLOUD_RUN_JOB_NAME \
    --source . \
    --project $PROJECT_ID \
    --region $REGION \
    --service-account $SERVICE_ACCOUNT_EMAIL
```

## Cloud Run Job Excution
```
gcloud run jobs execute $CLOUD_RUN_JOB_NAME \
    --region=$REGION \
    --args='--recipient=[Recipient Email Address]'
```