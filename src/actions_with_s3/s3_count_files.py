from src.config.s3_config import s3_client


def count_processed_files(bucket_name: str, token: str):
    try:
        return len(s3_client.list_objects_v2(Bucket=bucket_name, Prefix=token + "/depth-frames/")["Contents"])
    except:
        return 0


def count_original_files(bucket_name: str, token: str):
    try:
        return len(s3_client.list_objects_v2(Bucket=bucket_name, Prefix=token + "/frames/")["Contents"])
    except:
        return 0
