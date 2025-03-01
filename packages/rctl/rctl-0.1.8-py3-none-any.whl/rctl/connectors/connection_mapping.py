# boto3 を dest とする変換定義(fsspec.key は boto3.aws_access_key_id にマップされる)
dests = {
    "boto3": {
        "fsspec": {
            "protocol[s3]": "service_name",
            "key": "aws_access_key_id",
            "secret": "aws_secret_access_key",
        }
    }
}
