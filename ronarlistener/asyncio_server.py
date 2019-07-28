import asyncio

async def handle_echo(reader, writer):
    await handle_socket(reader, writer)
    await handle_command()

    print("Close the client socket")
    writer.close()

async def handle_socket(reader, writer):
    data = await reader.read(100)
    message = data
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))

    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()


async def handle_command():
    await asyncio.sleep(5)

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
print('Close the server')
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
print('Closed')