import time
from datetime import datetime, timedelta
from elk_tools import fetch_network_data, fetch_email_data, es_url_lookup, es_traffic_lookup
from email_to_hostname_bind import email_to_hostname
from config import MONITOR_TIMEOUT, SLACK_ALERT_CHANNEL
from slack_tools import send_slack_alert


def speed_test(func):
    def wrapper():
        ts = time.time()
        results = func()
        te = time.time()
        print(
            f"Function: {func.__name__}, took: {round((te - ts)*1000, 1)} ms")
        return results
    return wrapper


@speed_test
def parse_network_data():
    try:
        out = dict()
        net_data = fetch_network_data()
        for endpoint in net_data:
            hostname = endpoint['fields']['host.name'][0]
            fields = endpoint['fields']
            iocs = fields.get('dns.question.name', fields.get('url.full'))
            if hostname not in out.keys():
                out[hostname] = {
                    'iocs': iocs
                }
            else:
                out[hostname]['iocs'].extend(iocs)
            if not out[hostname].get('email'):
                out[hostname]['email'] = email_to_hostname(hostname)
        for endpoint in out:
            out[endpoint]['iocs'] = set(out[endpoint]['iocs'])
        return out
    except Exception as e:
        print(e)


@speed_test
def parse_email_data():
    try:
        out = dict()
        email_data = fetch_email_data()
        for email in email_data:
            fields = email['fields']
            delivered_to = fields['header.to'][0]
            iocs = fields.get('body.uri_hash')
            iocs.extend(fields.get('body.domain_hash'))
            if delivered_to not in out.keys():
                out[delivered_to] = {
                    'iocs': iocs
                }
            else:
                out[delivered_to]['iocs'].extend(iocs)
        for email in out:
            out[email]['iocs'] = set(out[email]['iocs'])
        return out
    except Exception as e:
        print(e)


# Checking if the network traffic was created after the email was
def check_click_after_email(email_ts, traffic_ts):
    try:
        email_ts = datetime.fromisoformat(email_ts)
        traffic_ts = datetime.strptime(traffic_ts, '%Y-%m-%dT%H:%M:%S.%fZ')
        if email_ts.replace(tzinfo=None) <= (traffic_ts + timedelta(hours=2)):
            return True
    except Exception as e:
        print(e)


def start_monitor():
    print("Starting URL Monitor...")
    reported = list()
    while True:
        network_data = parse_network_data()
        email_data = parse_email_data()
        for endpoint in network_data:
            email = network_data[endpoint].get('email')
            if email in email_data.keys():
                check_matches = set(network_data[endpoint]['iocs']) & set(
                    email_data[email]['iocs'])
            last_seen = dict()
            for url in check_matches:
                email_data = es_url_lookup(url, email)[0]
                if email_data['_source']['header']['date'] not in reported:
                    last_seen[url] = email_data
            for match in last_seen.keys():
                res = es_traffic_lookup(match, endpoint)
                entry = last_seen[match]
                if check_click_after_email(last_seen[match]['_source']['header']['date'], res):
                    print("Sending Slack Alert...")
                    context = f""":exclamation: *User click on url from email alert* :exclamation:\n\n*User (actor):* {email}\n*Hostname:* {endpoint}\n*Email Date:* {entry['_source']['header']['date']}\n*Email Subject:* {entry['_source']['header']['subject']}\n*Email From:* {entry['_source']['header']['from']}\n*MSID:* ```{entry['_source']['header']['header']['message-id'][0]}```\n\n*Related IOC/s:*\n```{match}```"""
                    slack_resp = send_slack_alert(
                        context, {'channel': SLACK_ALERT_CHANNEL, 'ts': ''})
                    print(
                        f"User: {email}, Accessed: {match}, From: {endpoint}")
                    reported.append(entry['_source']['header']['date'])
        time.sleep(MONITOR_TIMEOUT * 60)


if __name__ == "__main__":
    start_monitor()
