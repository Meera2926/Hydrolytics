class SimpleRateLimiter:
    def __init__(self, max_requests=60):
        self.max_requests = max_requests
        self.requests = {}

    def is_allowed(self, client_ip):
        count = self.requests.get(client_ip, 0)
        if count >= self.max_requests:
            return False
        self.requests[client_ip] = count + 1
        return True
