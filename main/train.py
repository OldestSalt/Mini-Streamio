import argparse
import os
from minio import S3Error
from ultralytics import YOLO, settings
from minio_utils import get_client, download_file, upload_file
import shutil
import mlflow

def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, help='Dataset address in minio')
    parser.add_argument('--model', type=str, help='Model name')
    args = parser.parse_args()
    print(f'Training model {args.model} on dataset {args.dataset}')

    endpoint = os.getenv('MINIO_ENDPOINT')
    access_key = os.getenv('MINIO_ROOT_USER')
    secret_key = os.getenv('MINIO_ROOT_PASSWORD')
    bucket = 'main-bucket'

    client = get_client(access_key, secret_key, endpoint)

    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)

    model_path = f'/models/{args.model}.pt'
    if not os.path.exists(f'.{model_path}'):
        try:
            print('Model not found locally, downloading')
            download_file(bucket, model_path, f'.{model_path}', client)
        except S3Error:
            raise ValueError(f'Model {args.model} not found')

    dataset_zip = f'/datasets/{args.dataset}.zip'
    if not os.path.exists(f'.{dataset_zip}'):
        try:
            print('Dataset not found locally, downloading')
            download_file(bucket, dataset_zip, f'.{dataset_zip}', client)
        except S3Error:
            raise ValueError(f'Dataset {args.dataset} not found')
    shutil.unpack_archive(f'.{dataset_zip}', f'./datasets/{args.dataset}')

    settings.update({'mlflow': True})

    model = YOLO(f'/app/{model_path}')
    model.train(data=f'/app/datasets/{args.dataset}/data.yaml', epochs=1, batch=16, imgsz=416, device='cpu', pretrained=True, project='YOLO experiment', name=f'training_{args.model}')
    model.save(f'/app/models/trained_{args.model}.pt')
    upload_file(bucket, f'/models/trained_{args.model}.pt', f'./models/trained_{args.model}.pt', client)

if __name__ == '__main__':
    train()