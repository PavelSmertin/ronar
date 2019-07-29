import asyncio


async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('', 32001,
                                                   loop=loop)

    loop.create_task(request_queue(writer, message))

    while True:
        data = await reader.read(1024)
        print('Received: %r' % data)
        if not data:
            break  # EOF
    
    print('Close the socket')
    writer.close()

async def request_queue(writer, message):
    print('Send: %r' % message)
    writer.write(message)

    await asyncio.sleep(1)
    print('Send: %r' % message)
    writer.write(message)

    await asyncio.sleep(5)
    print('Send: %r' % message)
    writer.write(message)

message = bytes.fromhex('11 61 3a 00 2b 16 11 11 00 00 00 00 12 34 56 78 9a bc de f0 12 34 56 78 9a bc de f0 00 00 24 00 13 01 15 02 20 19 3b 0e 64 00 31 01 00 00 00 00 00 00 00 00 00 00 7f 00 00 00 00 00 ec 5b 90 99')
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()
