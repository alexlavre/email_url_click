ELK_CLOUD_ID = ""
ELK_API_ID = ""
ELK_API_KEY = ""
MONITOR_TIMEOUT = 1  # (minutes)
EMAIL_DATA_INDEX = "example-index"
PACKETBEAT_FIELDS = ["host.name", "client.ip", "dns.question.name", "url.full"]
PACKETBEAT_INDEX = "packetbeat-*"
SLACK_TOKEN = ""
SLACK_ALERT_CHANNEL = "#email_url_click"
ES_SORT_DESC = [
    {
        "header.date": {
            "order": "desc",
            "unmapped_type": "boolean"
        }
    }
]
EMAIL_DATA_FIELDS = ["header.header.subject",
                     "header.header.date",
                     "header.from",
                     "header.delivered_to",
                     "body.domain_hash",
                     "body.uri_hash",
                     "body.uri_hash",
                     "header.received_ip",
                     "header.to"]
EMAIL_QUERY_FILTER = {
    "bool": {
        "must": [],
        "filter": [],
        "should": [],
        "must_not": []
    }}
PACKETBEAT_QUERY = {
    "bool": {
        "must": [],
        "filter": [
            {
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "should": [
                                    {
                                        "match_phrase": {
                                            "method": "GET"
                                        }
                                    }
                                ],
                                "minimum_should_match": 1
                            }
                        },
                        {
                            "bool": {
                                "should": [
                                    {
                                        "exists": {
                                            "field": "dns.question.name"
                                        }
                                    }
                                ],
                                "minimum_should_match": 1
                            }
                        }
                    ],
                    "minimum_should_match": 1
                }
            }
        ],
        "should": [],
        "must_not": []
    }
}
