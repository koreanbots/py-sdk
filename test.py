import koreanbots
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('koreanbots')
logger.addHandler(logging.StreamHandler())

Client = koreanbots.HTTPClient('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQxNTQwMTQzNzI0NjUyMTM0NCIsImlhdCI6MTU4ODQyNTk3OSwiZXhwIjoxNjE5OTgzNTc5fQ.BxdVXbskx2PZ9AbJu3VLEqEqcomefrmpcaI5RminSZ2cLLSaqvZE9JTxtWrGfdjvQWIUcaWdlQA-FzcVSLv8dXf6LQfk5d5Jenha4XEVamzroChiGN-CITRqVwYAZGewQ0HXGr5337y8cBBW3GTDNYfv6RfThjBcnJzmZVAcaIg')

loop = asyncio.get_event_loop()

for i in range(120):
    try:
        loop.run_until_complete(Client.postGuildCount(253))
    except: pass