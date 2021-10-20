# Importing the relevant libraries
import websockets
import asyncio
import logging
logging.basicConfig(filename='log.log', level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )
logger = logging.getLogger('client')

# Server data
PORT = 3003
logger.info('Server on %s:%s'+str(PORT))

# A set of connected ws clients
connected = set()

# The main behavior function for this server
async def echo(websocket, path):
    logger.debug('A client just connected')
    # Store a copy of the connected client
    connected.add(websocket)
    # Handle incoming messages
    try:
        async for message in websocket:
            logger.debug("Received message from client: " + message)
            # Send a response to all connected clients except sender
            for conn in connected:
                if conn == websocket:
                    await conn.send("Someone said: " + message)
    # Handle disconnecting clients 
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
        logger.debug("A client just disconnected")
    finally:
        connected.remove(websocket)

# Start the server
start_server = websockets.serve(echo, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()