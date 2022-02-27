from elasticsearch import Elasticsearch
from config import ELK_CLOUD_ID, ELK_API_ID, ELK_API_KEY, ELK_INDEX_NAME


es = Elasticsearch(
    cloud_id=ELK_CLOUD_ID
)
auth_client = es.options(
    api_key=(ELK_API_ID, ELK_API_KEY)
)


def send_to_elk(data: dict()):
    try:
        auth_client.index(
            index=ELK_INDEX_NAME,
            document=data
        )
    except Exception as e:
        print(e)
