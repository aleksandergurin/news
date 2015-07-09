from flask.ext.wtf import Form
from webapp.models import User
from wtforms import StringField, PasswordField, SubmitField, ValidationError, HiddenField, TextAreaField
from wtforms.validators import length, email, regexp, equal_to, required, optional

usernname_validators = [
    required(),
    length(User.const.username_min_len, User.const.username_max_len),
    regexp(User.const.username_regex, 0, "Please use only letters, numbers, underscores, and periods.")
]

password_validators = [
    required(),
    length(User.const.password_min_len, User.const.password_max_len),
    equal_to("password", message="Password doesn't match the confirmation.")
]

email_validators = [optional(), length(max=User.const.email_max_len), email()]
about_validators = [optional(), length(max=User.const.about_max_len)]


class Signup(Form):
    username = StringField("Username", validators=usernname_validators)
    password = PasswordField("Password", validators=[required()])
    password_again = PasswordField("Password confirmation", validators=password_validators)
    email = StringField("Email", validators=email_validators)   # optional field
    submit = SubmitField("Create an account")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already registered.")


class Login(Form):
    next_page = HiddenField()
    username_or_email = StringField("Username or login", validators=[required()])
    password = PasswordField("Password", validators=[required()])
    submit = SubmitField("Login")


class Profile(Form):
    username = StringField("Username")  # read-only
    email = StringField("Email", validators=email_validators)
    about = TextAreaField("About", validators=about_validators)
    update = SubmitField("Update")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user and user.username != self.username.data:
            raise ValidationError("Email already registered.")


class DeleteAccount(Form):
    delete = SubmitField("Delete my account")


class ChangePassword(Form):
    old_password = PasswordField("Old password", validators=[required()])
    password = PasswordField("New password", validators=[required()])
    password_again = PasswordField("Confirm new password", validators=password_validators)
    submit = SubmitField("Change password")
