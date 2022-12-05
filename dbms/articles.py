from minio import Minio

class ArticlesRepository:
    def __init__(self, minio_addr, minio_user, minio_password, minio_bucket_name) -> None:
        self.minio_addr = minio_addr
        self.minio_user = minio_user
        self.minio_password = minio_password
        self.minio_bucket_name = minio_bucket_name

        self.client = Minio(minio_addr, access_key=minio_user, secret_key=minio_password)

        assert self.client.bucket_exists(minio_bucket_name)

    def get_article(self, path: str):
        return self.client.get_object(self.minio_bucket_name, "bbc_news_texts/"+path)

    def get_video(self, path: str):
        return self.client.get_object(self.minio_bucket_name, "video/"+path)

    def get_image(self, path: str):
        return self.client.get_object(self.minio_bucket_name, "image/"+path)
