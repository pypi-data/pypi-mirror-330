# sigmasms

Module provides an interface for https://sigmasms.ru/api/http/.

## Usage

```python
from sigmasms import AsyncClient

# instantiate client
client = AsyncClient(username='login', password='password')

# authorize
await client.auth()
print(client.token)

# send message
resp = await client.send_message('TestSender', '+79999999999', 'text', 'sms')
print(resp)

# check message status
msg_id = resp['id']
status = await client.check_status(msg_id)
print(status)

# check balance
balance = await client.get_balance()
print(balance)

# close client 
await client.close()

```
