import os
from base64 import b64decode
from src.base_model.base_model import PostResponse, PutResponse, GetResponse
from src.config.router_config import router
from src.config.s3_config import bucket_name, s3_client
from fastapi import HTTPException, UploadFile, File
from src.actions_with_s3.s3_count_files import count_processed_files, count_original_files
from src.actions_with_s3.s3_validate_folders import validate_folder, validate_depth_frames
from src.actions_with_s3.validate_content_type import content_type
from src.actions_with_s3.s3_token_generation import generate_token
from src.config.url import depth_map_url
import shutil
from typing import List
from src.kafka_producer_config.kafka_producer import producer


@router.post("/depth-map", response_model=PostResponse, status_code=201)
async def generate_token_and_folder():
    generated_token = generate_token()
    s3_client.put_object(Bucket=bucket_name, Key=generated_token + "/")

    response = PostResponse
    response.data = {"token": generated_token}
    response.meta = {
        "validUntil": int(b64decode(generated_token).decode("ascii").split(":")[1]) + 43200,
        "_next": {"method": "PUT", "link": depth_map_url + generated_token},
    }

    return response


@router.put("/depth-map/{token}", response_model=PutResponse)
async def file_and_folder_validation_with_upload(token: str, frames: List[UploadFile] = File(...)):
    try:
        if validate_folder(bucket_name, token) is True:
            pass
    except:
        raise HTTPException(404, detail="Not Found")
    else:
        for downloaded_file in frames:
            if downloaded_file.content_type not in content_type:
                raise HTTPException(400, detail="Bad Request")
        else:
            for img in frames:
                with open(f"{img}", "wb") as buffer:
                    shutil.copyfileobj(img.file, buffer)
                    s3_client.upload_file(buffer.name, bucket_name, f"{token}" + "/" + "frames/" + img.filename)
                    os.remove(buffer.name)

            producer.send(topic="plugin.video.depthMap", key=token.encode("utf-8"), value={f"jobName": token})
            response = PutResponse
            response.data = {"jobId": token}
            response.meta = {
                "validUntil": int(b64decode(token).decode("ascii").split(":")[1]) + 43200,
                "_next": {"method": "GET", "link": depth_map_url + token + "/status"},
            }

            return response


@router.get("/depth-map/{token}/status", response_model=GetResponse)
async def get_files(token: str):
    try:
        if validate_depth_frames(bucket_name, token) is True:
            pass
    except:
        raise HTTPException(404, detail="Not Found")
    else:

        response = GetResponse
        response.data = []
        print(count_original_files(bucket_name, token))
        response.meta = {
            "count": count_processed_files(bucket_name, token),
            "originalFilesCount": count_original_files(bucket_name, token),
            "percentDone": 0,
        }

        return response
