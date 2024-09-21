from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField, TextAreaField, HiddenField, MultipleFileField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField(validators=[Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[Email()])
    password = PasswordField(validators=[DataRequired()])
    password2 = PasswordField("Confirm your password", validators=[DataRequired()])
    submit = SubmitField()


class PortfolioForm(FlaskForm):
    caption = StringField(validators=[DataRequired()])
    type = StringField(validators=[DataRequired()])
    images = MultipleFileField()
    roles = StringField(validators=[DataRequired()])
    text = TextAreaField(validators=[DataRequired()])
    tags = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Publish")


class BlogForm(FlaskForm):
    caption = StringField(validators=[DataRequired()])
    tag = StringField(validators=[DataRequired()])
    heading_image = FileField()
    images = MultipleFileField()
    text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("Publish")


class ContactForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[Email()])
    message = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("send")