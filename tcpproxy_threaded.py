import socket
from _thread import *
import threading
from proxymodules.deye import Module

def xfer(s_from, s_to, direction, lock):
    m = Module()
    print('From socket:', s_from)
    print('To socket:', s_to)
    while True:
        try:
            #  print('Try to set data from recv')
            data = s_from.recv(1024)
            if direction == 'clnt->srv':
                m.execute(data)
            print(f'recv {direction}: {data.hex()}')
        except socket.timeout:
            #  print(f'Socket recv timed out, retrying {direction}')
            continue
        except socket.error:
            print(f'Socket recv, socket no longer alive {direction}')
            break
        except Exception as e:
            print(f'Unhandled exception {direction} {e}')
            break
        if not data:
            break
        try:
            s_to.sendall(data)
        except Exception as e:
            print(f'Cannot send data in {direction} with {e}')
            break
    lock.release()
    print(f'Thread {direction} ends.')

def controller_thread(server_address, server_port, client):
    continue_lock = threading.Lock()
    print('First lock acquire in thread', threading.current_thread().name)
    continue_lock.acquire()

    srv_a = (server_address, server_port)
    srv_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_s.settimeout(5.0)
    try:
        print(f'Connect to remote server: {server_address}:{server_port}')
        srv_s.connect(srv_a)
    except Exception as e:
        print(f'Failed to connect with {e}')
        client.close()
        return

    print(client)
    print(srv_s)
    w = threading.Thread(target=xfer, args=(client, srv_s, 'clnt->srv', continue_lock, ))
    r = threading.Thread(target=xfer, args=(srv_s, client, 'srv->clnt', continue_lock, ))
    w.start()
    r.start()
    # Waiting for one thread to terminate
    print('Second lock acquire in thread', threading.current_thread().name)
    continue_lock.acquire()
    print('After second lock acquire in thread', threading.current_thread().name)
    # connection closed, that will also bring the other thread to a halt
    client.close()
    srv_s.close()
    print('Controller thread ends, client socket closed')


def Main():
    listen_host = "0.0.0.0"
    listen_port = 10000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(True)
    s.bind((listen_host, listen_port))
    print("socket bound to port", listen_port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        c, addr = s.accept()
        print(f'Connected to: {addr[0]}:{addr[1]}')

        # Start a new thread and return its identifier
        start_new_thread(controller_thread, ('5406.deviceaccess.host', 10000, c,))


if __name__ == '__main__':
    Main()
