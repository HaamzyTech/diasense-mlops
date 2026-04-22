from prometheus_client import Counter

REQUEST_COUNTER = Counter("diasense_requests_total", "Total requests", ["endpoint"])
