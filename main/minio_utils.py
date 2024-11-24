from minio import Minio
def download_file(bucket: str, object_name: str, file_path: str, minio_client: Minio) -> None:
    print('Downloading file from minio')
    minio_client.fget_object(bucket, object_name, file_path)

def upload_file(bucket: str, object_name: str, file_path: str, minio_client: Minio) -> None:
    print('Uploading file to minio')
    minio_client.fput_object(bucket, object_name, file_path)

def get_client(access_key: str, secret_key: str, endpoint: str) -> Minio:
    return Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)