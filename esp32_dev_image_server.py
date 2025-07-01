import socket

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Listening on http://{}/".format('192.168.0.179'))

while True:
    cl, addr = s.accept()
    print("Client connected from", addr)

    try:
        request = cl.recv(1024)
        request = request.decode("utf-8")
        print("Request:", request)

        if "GET / " in request or "GET /fb.raw" in request:
            with open("fb.raw", "rb") as f:
                cl.send(b"HTTP/1.1 200 OK\r\n")
                cl.send(b"Content-Type: application/octet-stream\r\n")
                cl.send(b"Content-Disposition: attachment; filename=fb.raw\r\n")
                cl.send(b"\r\n")

                while True:
                    chunk = f.read(512)
                    if not chunk:
                        break
                    cl.send(chunk)
        else:
            cl.send(b"HTTP/1.1 404 Not Found\r\n\r\nFile not found.")

    except Exception as e:
        print("Error:", e)

    cl.close()