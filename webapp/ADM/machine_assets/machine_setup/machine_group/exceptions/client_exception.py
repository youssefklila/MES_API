


class ClientNotFoundError(Exception):
    def __init__(self, client_id: int):
        super().__init__(f"Client with ID {client_id} not found.")
        self.client_id = client_id
