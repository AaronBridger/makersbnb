class Listing:
    def __init__(self, id, name, description, price, user_id):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.user_id = user_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Listing({self.id}, {self.name}, {self.description}, {self.price}, {self.user_id})"

    def is_valid(self):
        if self.name is None or self.name == "":
            return False
        if self.description is None or self.description == "":
            return False
        if self.price is None or not isinstance(self.price, int):
            return False
        return True

    def generate_errors(self):
        errors = []
        if self.name is None or self.name == "":
            errors.append("Please add a name")
        if self.description is None or self.description == "":
            errors.append("Please add a description")
        if self.price is None or not isinstance(self.price, int):
            errors.append("Please ad a nightly price")
        if len(errors) == 0:
            return None
        else:
            return ", ".join(errors)
