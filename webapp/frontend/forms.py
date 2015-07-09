
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import required, length, optional, url
from ..models import Comment, Post

title_validators = [required(), length(Post.const.title_min_len, Post.const.title_max_len)]
url_validators = [optional(), length(max=Post.const.url_max_len), url()]
description_validators = [optional(), length(max=Post.const.description_max_len)]

text_validators = [required(), length(max=Comment.const.test_max_len)]


class SubmitPost(Form):
    title = StringField("Title", validators=title_validators)
    url = StringField("URL", validators=url_validators)
    description = TextAreaField("Description", validators=description_validators)
    submit = SubmitField("Submit")


class SubmitComment(Form):
    text = TextAreaField("Comment", validators=text_validators)
    submit = SubmitField("Add comment")
