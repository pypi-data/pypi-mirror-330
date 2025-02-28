class Auth:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    def verify_auth(self):
        response = self.client.post(f'{self.base_url}/public/v1/auth/verify')
        return response.is_success


class AuthAsync:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    async def verify_auth(self):
        response = await self.client.post(f'{self.base_url}/public/v1/auth/verify')
        return response.is_success
