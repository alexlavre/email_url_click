# Used https://pypi.org/project/eml-parser/

# Remember to Explain about hashing the URL's and the impact on speed & detection.

# Currently I reverted the eml-parser library not to hash but store the url / domain as is, but you should always hash!

# The automation has basically 2 parts.

# 1st part is eml_parser_loader, which receives the .eml file, parses it and ships it to ELK, it can be scallable if we define the "input" to be some shared S3 bucket, and run the dirwatcher on K8S behind ELB which could handle lot's of traffic.

# 2nd part is the url_monitor, which I think is not the greatest, I would do the following changes:

# 1) Instead of fetching IOC's from ES, after parsing the .eml I would send them to Mongo instance, and then load the DB to memcached and query memcached instead.

# 2) If possible, fetch the urls from some email securty system (that already parses the .eml).

# 3) I would fetch email audit logs (as most of the time there is a log about - "url access" and query DNS logs for the endpoint around the time of the url access log) so this way you could connect when user actually clicked on the url from email, and not just browsed to the website.
