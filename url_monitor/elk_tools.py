from elasticsearch import Elasticsearch
from config import ELK_CLOUD_ID, ELK_API_ID, ELK_API_KEY, EMAIL_QUERY_FILTER, EMAIL_DATA_INDEX, PACKETBEAT_QUERY, PACKETBEAT_INDEX, PACKETBEAT_FIELDS, EMAIL_DATA_FIELDS, ES_SORT_DESC


ES = Elasticsearch(
    cloud_id=ELK_CLOUD_ID
).options(api_key=(ELK_API_ID, ELK_API_KEY))


def fetch_email_data(size=10000):
    try:
        resp = ES.search(index=EMAIL_DATA_INDEX,
                         query=EMAIL_QUERY_FILTER, size=size, fields=EMAIL_DATA_FIELDS, _source=False)
        return resp['hits']['hits']
    except Exception as e:
        print(e)


def fetch_network_data(size=10000):
    try:
        resp = ES.search(index=PACKETBEAT_INDEX, query=PACKETBEAT_QUERY, size=size,
                         fields=PACKETBEAT_FIELDS, _source=False)
        return resp['hits']['hits']
    except Exception as e:
        print(e)


def es_url_lookup(url, recipient, size=1):
    try:
        query = {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "must": [
                                {
                                    "multi_match": {
                                        "type": "phrase",
                                        "query": f"{url}",
                                        "lenient": True
                                    }
                                },
                                {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "header.to": f"{recipient}"
                                                }
                                            }
                                        ],
                                        "minimum_should_match": 1
                                    }
                                }
                            ]
                        }
                    }
                ],
                "filter": [],
                "should": [],
                "must_not": []
            }
        }
        resp = ES.search(index=EMAIL_DATA_INDEX, query=query,
                         size=size, sort=ES_SORT_DESC)
        return resp['hits']['hits']
    except Exception as e:
        print(e)


def es_traffic_lookup(url, hostname, size=1):
    try:
        query = {
            "bool": {
                "must": [],
                "filter": [
                    {
                        "bool": {
                            "filter": [
                                {
                                    "multi_match": {
                                        "type": "best_fields",
                                        "query": f"{url}",
                                        "lenient": True
                                    }
                                },
                                {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "host.name": f"{hostname}"
                                                }
                                            }
                                        ],
                                        "minimum_should_match": 1
                                    }
                                }
                            ]
                        }
                    }
                ],
                "should": [],
                "must_not": []
            }
        }
        resp = ES.search(index=PACKETBEAT_INDEX, query=query, fields=[
                         '@timestamp'], size=size, _source=False, sort=ES_SORT_DESC)
        return resp['hits']['hits'][0]['fields']['@timestamp'][0]
    except Exception as e:
        print(e)
