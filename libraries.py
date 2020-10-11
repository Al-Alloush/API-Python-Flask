ACCESS_EXPIRES_m = 15
REFRESH_EXPIRES_d = 30

import redis
'''
for avoid return string in this form b'sting' encoding this text by: .encode('utf-8')
but when we need to use this test we must decoding  the get() return by: .decode('utf-8')
cache.set('var1', 'the test'.encode('utf-8'))
or add charset="utf-8" to connection code '''
revoked_store = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)