from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re

class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique = True)    
    password_hash = pw.TextField(null=False)
    password = None

    def validate(self):
        # check if email is unique
        existing_user_email = User.get_or_none(User.email == self.email)
        if existing_user_email:
            self.errors.append(f"User with {self.email} already exists.")
        
        # check if username is unique
        existing_user_username = User.get_or_none(User.username == self.username)
        if existing_user_username:
            self.errors.append(f"User with {self.username} already exists.")

        # Password Validation
            # check if password contains more than 6
        if len(self.password) <= 6:
            self.errors.append("Password is less than 6 characters")
            
            # lower, uppercase
        has_lower = re.search(r"[a-z]", self.password)
        has_upper = re.search(r"[A-Z]", self.password)
        has_special = re.search(r"[\[ \] \! \@ \# \$ \% \^ \& \* \( \)]", self.password)

        if has_lower and has_upper and has_special:
            self.password_hash = generate_password_hash(self.password)
        else:
            self.errors.append("Password should contain lowercase, uppercase and special characters")
         
