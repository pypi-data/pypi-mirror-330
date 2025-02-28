from qcloud_cos import CosConfig, CosS3Client
import time
from qcloud_cos.cos_exception import CosClientError, CosServiceError
from src.config_manager import ConfigManager
import os
from pathlib import Path


class COSClient:
    def __init__(self, config_name):
        self.config_manager = ConfigManager()
        config = self.config_manager.get_config(config_name)
        if not config:
            raise ValueError("配置不存在")

        self.client = CosS3Client(
            CosConfig(
                Region=config['cos_region'],
                SecretId=config['cos_secret_id'],
                SecretKey=config['cos_secret_key']
            )
        )
        self.bucket = config['cos_bucket']
        self.prefix = config['prefix']
        self.region = config['cos_region']

    def list_objects(self):
        try:
            response = self.client.list_objects(
                Bucket=self.bucket,
                Prefix=self.prefix,
                MaxKeys=1000
            )
            contents = response.get('Contents', [])
            return [{
                'Key': content['Key'],
                'Size': content['Size'],
                'LastModified': content['LastModified'],
                'ETag': content['ETag']
            } for content in response.get('Contents', [])]
        except (CosClientError, CosServiceError) as e:
            raise RuntimeError(f"COS操作失败: {e}")

    def delete_object(self, key):
        try:
            self.client.delete_object(
                Bucket=self.bucket,
                Key=key
            )
            return True
        except (CosClientError, CosServiceError) as e:
            raise RuntimeError(f"删除失败: {e}")

    def download_object(self, key, download_path, progress_callback=None):
        try:
            download_dir = Path(download_path)
            download_dir.mkdir(parents=True, exist_ok=True)
            filename = os.path.basename(key)
            local_path = download_dir / filename

            # 获取文件总大小
            head_response = self.client.head_object(
                Bucket=self.bucket,
                Key=key
            )
            total_size = int(head_response['Content-Length'])

            # 分块下载
            downloaded = 0
            response = self.client.get_object(
                Bucket=self.bucket,
                Key=key,
            )
            stream = response['Body']

            with open(local_path, 'wb') as f:
                while True:
                    chunk = stream.read(1024 * 1024)  # 1MB chunks
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    # 计算进度
                    if progress_callback:
                        progress_callback(total=total_size, value=downloaded)

            return local_path
        except (CosClientError, CosServiceError) as e:
            raise RuntimeError(f"下载失败: {e}")

    def get_object(self, key):
        try:
            response = self.client.head_object(
                Bucket=self.bucket,
                Key=key
            )
            # 获取对象标签
            tags_response = self.client.get_object_tagging(
                Bucket=self.bucket,
                Key=key
            )

            tag_set = tags_response.get('TagSet', [])
            if tag_set:
                tags = {tag['Key']: tag['Value'] for tag in tag_set['Tag']}
            else:
                tags = {}

            return {
                'Key': key,
                'Size': response['Content-Length'],
                'LastModified': response['Last-Modified'],
                'ETag': response['ETag'],
                'Location': f"https://{self.bucket}.cos.{self.region}.myqcloud.com/{key}",
                'Tags': tags
            }
        except (CosClientError, CosServiceError) as e:
            raise RuntimeError(f"获取对象详情失败: {e}")
