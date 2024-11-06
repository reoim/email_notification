## Set configuration.yaml
configurationl.yaml 파일은 Cloud Run Job 에서 사용할 이메일 설정을 저장합니다. 다음의 각 설정 항목 설명을 참고하여 설정합니다.

EmailConfig:

- **Sender**: 발신자의 Gmail 주소를 입력합니다.
- **Password**: Gmail app password를 입력합니다. 발신자 gmail의 자격증명 획득을 위해 app password 가 사용됩니다. [Gmail app password 생성 방법](https://support.google.com/accounts/answer/185833)을 참고하여 생성합니다.
- **Subject**: 이메일 제목을 입력합니다.
- **Body**: 이메일 본문을 입력합니다. 여러 줄의 텍스트를 입력하려면 | 기호를 사용하고, 각 줄은 들여쓰기를 유지해야 합니다.
- **DefaultRecipients**: 기본적으로 이메일을 받을 수신자 목록을 입력합니다. 여러 명일 경우 - 기호를 사용하여 각 수신자를 나열합니다.


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