import argparse
from minio_utils import get_client

def main():
    print('Using: \n\tTo start training model use "python train.py --dataset=minio_address --model=model_name"\n\tIf specified model will not be found, its weights will be downloaded\n\t')

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--access-key', type=str, help='Minio access key')
    # parser.add_argument('--secret-key', type=str, help='Minio secret key')
    # parser.add_argument('--endpoint', type=str, help='Minio endpoint')
    # parser.add_argument('--bucket', type=str, help='Minio bucket name')
    # args = parser.parse_args()



if __name__ == '__main__':
    main()