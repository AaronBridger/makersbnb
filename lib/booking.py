
from datetime import datetime, date


class Booking:
    def __init__(self, id, listing_id, user_id, check_in, check_out, status):
        self.id = id
        self.listing_id = listing_id
        self.user_id = user_id
        self.check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
        self.check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
        self.status = status

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Booking({self.id}, {self.listing_id}, {self.user_id}, {self.check_in}, {self.check_out}, {self.status})"
    
    def is_valid(self):
        if self.check_in < datetime.now().date():
            return False

        if self.check_out <= self.check_in:
            return False
        
        # add some overlapping booking functionality/check
        
        return True


    def generate_errors(self):
        errors = []
        if self.check_in < datetime.now().date():
            errors.append("Start date cannot be in the past!")
        elif self.check_out <= self.check_in:
            errors.append("End date must be after your start date!")
        elif self.check_in == None:
            errors.append("Please enter a start date!")
        elif self.check_out == None:
            errors.append("Please enter a end date!")
        elif self.check_in == None and self.check_out == None:
            errors.append("Please enter a start and end date!")

        return errors
