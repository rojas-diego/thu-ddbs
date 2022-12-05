from articles import ArticlesRepository
import os

if __name__ == "__main__":
    minio_addr = os.environ["DBMS_MINIO_ADDR"]
    minio_user = os.environ["DBMS_MINIO_USER"]
    minio_password = os.environ["DBMS_MINIO_PASSWORD"]
    minio_bucket_name = os.environ["DBMS_MINIO_BUCKET_NAME"]

    articles_repo = ArticlesRepository(minio_addr, minio_user, minio_password, minio_bucket_name)

    # articles_repo.get_article("business/001.txt")
    # articles_repo.get_image("0.jpg")
    # articles_repo.get_video("video1.flv")
