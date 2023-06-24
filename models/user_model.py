class User():
    def __init__(self, id, first_name, email, password, public_id) -> None:
        self.id = id
        self.first_name = first_name
        self.email = email
        self.password = password
        self.public_id = public_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.first_name,
            "email": self.email,
            "password": self.password,
            "public_id": self.public_id
        }