import httpx

from typing import Optional

__all__ = ['Client', 'AsyncClient', 'SigmaClientError']

_BASE_URL = 'http://online.sigmasms.ru/api'


class SigmaSMSError(Exception):
    pass


class SigmaClientError(SigmaSMSError):

    def __init__(self, reason):
        self.status = 'failed'
        self.reason = str(reason)


class BaseClient:

    def __init__(self, username: str, password: str):
        self.username: str = username
        self.password: str = password
        self.token: Optional[str] = None
        self.user_id: Optional[str] = None

    def prepare_payload(self, sender, recipient, message, mtype):
        return {
            'recipient': recipient,
            'type': mtype,
            'payload': {
                'sender': sender,
                'text': message
            }
        }


class Client(BaseClient):

    def __init__(
        self, username: str, password: str, base_url: str = _BASE_URL
    ):
        super().__init__(username, password)
        self.client: httpx.Client = httpx.Client(base_url=base_url, timeout=60)

    def close(self):
        self.client.close()

    def _request(self, method, path, **kwargs):
        if self.token is not None:
            kwargs['headers'] = {'Authorization': self.token}
        try:
            resp = self.client.request(method, path, **kwargs)
        except httpx.TransportError as exc:
            raise SigmaClientError(exc)
        resp.raise_for_status()
        return resp.json()

    def auth(self):
        if not (self.username or self.password):
            raise SigmaClientError('Username and password are required')
        data = {'username': self.username, 'password': self.password}
        resp = self._request('POST', 'login',  json=data)
        self.user_id = resp['id']
        self.token = resp['token']

    def send_message(self, sender, recipient, message, mtype):
        payload = self.prepare_payload(sender, recipient, message, mtype)
        return self._request('POST', 'sendings', json=payload)

    def check_status(self, message_id):
        return self._request('GET', f'sendings/{message_id}')

    def get_balance(self):
        resp = self._request('GET', f'users/{self.user_id}')
        return resp['balance']


class AsyncClient(BaseClient):

    def __init__(
        self, username: str, password: str, base_url: str = _BASE_URL
    ):
        super().__init__(username, password)
        self.client: httpx.AsyncClient = httpx.AsyncClient(
            base_url=base_url, timeout=60
        )

    async def close(self):
        await self.client.aclose()

    async def _request(self, method, path, **kwargs):
        if self.token is not None:
            kwargs['headers'] = {'Authorization': self.token}
        try:
            resp = await self.client.request(method, path, **kwargs)
        except httpx.TransportError as exc:
            raise SigmaClientError(exc)
        resp.raise_for_status()
        return resp.json()

    async def auth(self):
        if not (self.username or self.password):
            raise SigmaClientError('Username and password are required')
        data = {'username': self.username, 'password': self.password}
        resp = await self._request('POST', 'login',  json=data)
        self.user_id = resp['id']
        self.token = resp['token']

    async def send_message(self, sender, recipient, message, mtype):
        payload = self.prepare_payload(sender, recipient, message, mtype)
        return await self._request('POST', 'sendings', json=payload)

    async def check_status(self, message_id):
        return await self._request('GET', f'sendings/{message_id}')

    async def get_balance(self):
        resp = await self._request('GET', f'users/{self.user_id}')
        return resp['balance']
