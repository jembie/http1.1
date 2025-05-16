import socket


def do_GET(path: str) -> str:
    body = f"<html><body><h1>You requested: {path}</h1></body></html>"
    headers = {"Content-Type": "text/html; charset=utf-8", "Content-Length": str(len(body)), "Connection": "close"}
    return build_response(status_code="HTTP/1.1 200 OK", headers=headers, body=body)


def do_POST(path: str) -> str: ...


def make_response(method: str, path):
    match method:
        case "GET":
            return do_GET(path=path)

        case _:
            return "HTTP/1.1 405 Method Not Allowed\r\n" "Connection: close\r\n" "\r\n"


def build_response(status_code: str, headers: dict, body: str) -> str:
    header_lines = [f"{key}: {value}" for key, value in headers.items()]
    response = f"{status_code}\r\n" + "\r\n".join(header_lines) + "\r\n\r\n" + body
    return response


def bad_request() -> str:
    return build_response(
        status_code="HTTP/1.1 400 Bad Request", headers={"Connection": "close"}, body="<html><body><h1>400 Bad Request</h1></body></html>"
    )


def main():

    HOST = "127.0.0.1"
    PORT = 8080

    #                                    use ipv4        use TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Serving HTTP on {HOST} port {PORT} ...")

    while True:
        client_connection, client_address = server_socket.accept()
        request = client_connection.recv(1024).decode("utf-8")
        print(request)

        try:
            request_line = request.splitlines()[0]
            method, path, version = request_line.split()
        except ValueError:
            response = bad_request()
            client_connection.sendall(response.encode("utf-8"))
            client_connection.close()
            continue

        response = make_response(resp=method, path=path)

        client_connection.sendall(response.encode("utf-8"))
        client_connection.close()


if __name__ == "__main__":
    main()
