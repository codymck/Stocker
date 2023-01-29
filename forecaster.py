import yfinance as yf
from datetime import date, datetime
import boto3

file = ""
ticker = ""


###### Get and Parse Stock CSV #######
def formatData(t):
    ticker = t

    try:
        data = yf.Ticker(ticker)
    except:
        return

    today = date.today()

    yearAgo = today.day.__str__()
    yearAgo += today.month.__str__()
    yearAgo += (today.year - 1).__str__()

    begin = datetime.strptime(yearAgo, '%d%m%Y').date()

    df = data.history(start=begin, end=today, interval="1d")

    df.insert(0, 'timestamp', df.index)
    df['timestamp'] = df['timestamp'].dt.date

    df.pop('Dividends')
    df.pop('Stock Splits')
    df.insert(0, 'item_id', ticker)

    cols = list(df.columns.values)
    df = df[cols[0:5] + [cols[-1]] + [cols[5]]]

    df = df.rename({'Open': 'Open2', 'Close': 'target_value'}, axis=1)

    file = ticker + ".csv"
    df.to_csv(file, index=False)


###### Connect to AWS ########
def AWSconnect():
    bucket_name = 'stocks-lpl-hackathon'

    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id='AKIAZDYPP63FRVBZ27EH',
        aws_secret_access_key='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'
    )

    s3.Bucket('stocks-lpl-hackathon').upload_file(Filename=file, Key=file)

    client = boto3.client(
        service_name='forecast',
        region_name='us-east-1',
        aws_access_key_id='AKIAZDYPP63FY5U5IGQD',
        aws_secret_access_key='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'
    )

    DATA_VERSION = 1
    DATASET_FREQUENCY = "D"
    TIMESTAMP_FORMAT = "yyyy-MM-dd"
    role_name = "ForecastRole-Basic"
    role_arn = "arn:aws:iam::626560857803:role/service-role/AmazonForecast-ExecutionRole-1674939032534"

    dataset_group = f"{ticker}_{DATA_VERSION}"
    print(f"Dataset Group Name = {dataset_group}")

    dataset_arns = []
    create_dataset_group_response = \
        client.create_dataset_group(Domain="CUSTOM",
                                    DatasetGroupName=dataset_group,
                                    DatasetArns=dataset_arns)

    dataset_group_arn = create_dataset_group_response['DatasetGroupArn']

    client.describe_dataset_group(DatasetGroupArn=dataset_group_arn)

    ts_schema = {
        "Attributes": [
            {
                "AttributeName": "item_id",
                "AttributeType": "string"
            },
            {
                "AttributeName": "timestamp",
                "AttributeType": "timestamp"
            },
            {
                "AttributeName": "Open2",
                "AttributeType": "string"
            },
            {
                "AttributeName": "High",
                "AttributeType": "string"
            },
            {
                "AttributeName": "Low",
                "AttributeType": "string"
            },
            {
                "AttributeName": "Volume",
                "AttributeType": "string"
            },
            {
                "AttributeName": "target_value",
                "AttributeType": "float"
            }
        ]
    }

    ts_dataset_name = f"{ticker}_{DATA_VERSION}_dataset11"
    # print(ts_dataset_name)

    response = \
        client.create_dataset(Domain="CUSTOM",
                              DatasetType='TARGET_TIME_SERIES',
                              DatasetName=ts_dataset_name,
                              DataFrequency=DATASET_FREQUENCY,
                              Schema=ts_schema
                              )

    ts_dataset_arn = response['DatasetArn']

    client.describe_dataset(DatasetArn=ts_dataset_arn)

    dataset_arns = []
    dataset_arns.append(ts_dataset_arn)
    client.update_dataset_group(DatasetGroupArn=dataset_group_arn, DatasetArns=dataset_arns)

    ts_s3_data_path = "s3://" + bucket_name + "/" + file
    # print(f"S3 URI for your data file = {ts_s3_data_path}")

    ts_dataset_import_job_response = \
        client.create_dataset_import_job(DatasetImportJobName=dataset_group,
                                         DatasetArn=ts_dataset_arn,
                                         DataSource={
                                             "S3Config": {
                                                 "Path": ts_s3_data_path,
                                                 "RoleArn": role_arn
                                             }
                                         },
                                         TimestampFormat=TIMESTAMP_FORMAT)

    ts_dataset_import_job_arn = ts_dataset_import_job_response['DatasetImportJobArn']
    ts_dataset_import_job_arn

##### Start Predictor ########
# FORECAST_LENGTH = 60;
#
# create_predictor_response = \
#     client.create_predictor(PredictorName=f"{ticker}_predictor",
#                               ForecastHorizon=FORECAST_LENGTH,
#                               PerformAutoML=True,
#                               PerformHPO=False,
#                               InputDataConfig= {"DatasetGroupArn": dataset_group_arn},
#                               FeaturizationConfig= {"ForecastFrequency": DATASET_FREQUENCY}
#                              )
