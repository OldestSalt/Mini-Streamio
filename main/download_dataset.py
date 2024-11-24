from roboflow import Roboflow
import asyncio
from minio_utils import upload_file, get_client
import os
import shutil

async def download_dataset(api_key: str, workspace: str, project_name: str, version_name: int, model_version: str) -> str:

    rf = Roboflow(api_key="dh1IQQWaRMJr2hLveWqL")
    project = rf.workspace("daniels-magonis-0pjzx").project("valorant-9ufcp")
    version = project.version(3)
    await asyncio.to_thread(version.download, "yolov11", './datasets')

    # await asyncio.to_thread(version.download, model_version, './datasets')

    # print(f'Downloaded dataset {dataset.name}-{version_name} to ./datasets')
    # await asyncio.to_thread(shutil.make_archive, f'./datasets/{dataset.name}-{version_name}', 'zip', f'./datasets/{dataset.name}-{version_name}')
    # return f'./datasets/{dataset.name}-{version_name}.zip'
def upload_dataset(zip_path: str):
    shutil.make_archive(zip_path, 'zip', f'.{zip_path}')
    print('Dataset zipped')
    endpoint = os.getenv('MINIO_ENDPOINT')
    access_key = os.getenv('MINIO_ROOT_USER')
    secret_key = os.getenv('MINIO_ROOT_PASSWORD')
    bucket = 'main-bucket'
    client = get_client(access_key, secret_key, endpoint)

    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
    upload_file(bucket, f'{zip_path}.zip', f'.{zip_path}.zip', client)
    print('Dataset uploaded')
async def main():
    zip_path = await download_dataset("dh1IQQWaRMJr2hLveWqL", "daniels-magonis-0pjzx", "valorant-9ufcp", 3, "yolov11")
    # await upload_dataset(zip_path)

if __name__ == '__main__':
    # asyncio.run(main())
    upload_dataset('/datasets/valorant-3')
    # asyncio.run(download_dataset("dh1IQQWaRMJr2hLveWqL", "daniels-magonis-0pjzx", "valorant-9ufcp", 3, "yolov11"))