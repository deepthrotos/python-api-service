from src.config.s3_config import s3_client


def validate_folder(bucket_name: str, token: str):
    if token in s3_client.list_objects_v2(Bucket=bucket_name, Prefix=token)["Contents"][0]["Key"].split("/"):
        return True


def validate_depth_frames(bucket_name: str, token: str):
    if "depth-frames" not in s3_client.list_objects_v2(Bucket=bucket_name, Prefix=token)["Contents"][0]["Key"].split(
        "/"
    ):
        return True
