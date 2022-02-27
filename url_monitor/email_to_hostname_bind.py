# In order to confirm that the employee has accessed certain URL that he received via the email channel, we need to bind the email address to the endpoint, this can be easily done via querying some inventory management system or EDR, and build a lookup table / DB.

# For this I'm using a generic hard coded example of the payload

# Let's say I query the inventory management system / EDR to fetch the most up-to-date endpoint information.

# example for entry: HOSTNAME:EMAIL
MONGO_DB_ENTRY = {
    'SOME_ENDPOINT_HOSTNAME': 'USER@DOMAIN.COM'
}


def email_to_hostname(hostname: str()):
    try:
        # search for email in DB and get the hostname.
        return MONGO_DB_ENTRY.get(hostname)
    except Exception as e:
        print(e)
