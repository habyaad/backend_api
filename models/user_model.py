class User():
    def __init__(self, id, first_name, email, password) -> None:
        self.id = id
        self.first_name = first_name
        self.email = email
        self.password = password

    def updateUser(self, new_id, new_first_name, new_email, new_password):
        self.id = new_id
        self.first_name = new_first_name
        self.email = new_email
        self.password = new_password

    def serialize(self):
        return {
            "id": self.id,
            "name": self.first_name,
            "email": self.email,
            "password": self.password
        }