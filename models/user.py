from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property

class User(UserMixin, BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique = True)    
    password_hash = pw.TextField(null=False)
    password = None
    image_path=pw.TextField(null=True)

    @hybrid_property
    def full_image_path(self):
        if self.image_path:
            from app import app
            return app.config.get("S3_LOCATION") + self.image_path
        else:
            return ""

    def validate(self):
        # check if email is unique
        existing_user_email = User.get_or_none(User.email == self.email)
        if existing_user_email and existing_user_email.id !=self.id:
            self.errors.append(f"User with {self.email} already exists")
        
        #username should be unique
        existing_user_username = User.get_or_none(User.username == self.username)
        if existing_user_username and existing_user_username.id != self.id:
            self.errors.append(f"User with {self.username} already exists")

        # Password validations
        if self.password:
            if len(self.password) <= 6:
                self.errors.append("Password is less than 6 characters")
            # lowercase characters & uppercase characters
            has_lower = re.search(r"[a-z]", self.password)
            has_upper = re.search(r"[A-Z]", self.password)
            has_special = re.search(r"[\[ \] \@ \$ \* \^ \# \%]", self.password)

            if has_lower and has_upper and has_special:
                self.password_hash = generate_password_hash(self.password)
            else:
                self.errors.append("Password either does not have lower, upper, or special characters")
    