from flask import Blueprint, render_template, request, redirect, flash, abort
from flask.ext.login import login_required, current_user
from .forms import SubmitPost, SubmitComment
from ..models import Post, Comment, User
from ..extensions import db

frontend = Blueprint("frontend", __name__, template_folder="../templates")


NUM_OF_PAGES = 30

@frontend.route("/")
def index():
    return new()


@frontend.route("/post/<int:post_id>")
def get_post(post_id):
    return render_template("post.html",
                           post=Post.query.filter_by(id=post_id).first_or_404(),
                           form=SubmitComment(),
                           action="/post/{}".format(post_id))


@frontend.route("/post/<int:post_id>", methods=["POST"])
def submit_comment_for_post(post_id):
    form = SubmitComment()
    post = Post.query.filter_by(id=post_id).first_or_404()

    if not current_user.is_authenticated():
        flash("To add a comment, you must log in.")
    elif form.validate_on_submit():
        comment = Comment()
        form.populate_obj(comment)
        comment.author_id = current_user.id
        comment.post_id = post_id
        post.number_of_comments += 1
        db.session.add(comment)
        db.session.commit()
        return redirect("/post/{}".format(post_id))
    return render_template("post.html", post=post, form=form)


@frontend.route("/comment/<comment_id>")
def get_comment_by_id(comment_id):
    return render_template("comment.html",
                           comment=Comment.query.filter_by(id=comment_id).first_or_404())


@frontend.route("/user/<int:user_id>")
def get_user_info(user_id):
    return render_template("user.html",
                           user=User.query.filter_by(id=user_id).first_or_404())


@frontend.route("/comment/user/<int:user_id>")
def get_comments_by_user(user_id):
    return render_template("comments-by-user.html",
                           user=User.query.filter_by(id=user_id).first_or_404())


@frontend.route("/post/user/<int:user_id>")
def get_posts_by_user(user_id):
    return render_template("posts-by-user.html",
                           user=User.query.filter_by(id=user_id).first_or_404())


@frontend.route("/new")
def new():
    posts, next_page_post = pagination_for_first_item(Post)
    return render_template("posts.html", posts=posts, next=next_page_post, sel="new")


@frontend.route("/new/<int:post_id>")
def posts(post_id):
    posts, prev_page_post, next_page_post = pagination_for(Post, post_id)
    return render_template("posts.html", posts=posts, prev=prev_page_post, next=next_page_post, sel="new")


def pagination_for_first_item(item):
    # item.id is autoincrement integer, so older items have greater id
    result = item.query.order_by(db.desc(item.id)).limit(NUM_OF_PAGES)
    item_for_next_page = None
    if result.count() > 0:
        item_for_next_page = item.query.filter_by(id=result[0].id - NUM_OF_PAGES).first()
    return result, item_for_next_page


def pagination_for(item, item_id):
    result = item.query.order_by(db.desc(item.id)).\
        filter(item.id <= item_id).limit(NUM_OF_PAGES)

    if result.count() == 0:
        abort(404)

    next_page_item = item.query.filter_by(id=item_id - NUM_OF_PAGES).first()
    prev_page_item = item.query.\
        filter(db.and_(item_id < item.id, item.id <= item_id + NUM_OF_PAGES)).\
        order_by(db.desc(item.id)).first()
    return result, prev_page_item, next_page_item


@frontend.route("/comments")
def new_comments():
    comments, next_page_comment = pagination_for_first_item(Comment)
    return render_template("comments.html", comments=comments, next=next_page_comment, sel="comments")


@frontend.route("/comments/<int:comment_id>")
def comments(comment_id):
    comments, prev_page_comment, next_page_comment = pagination_for(Comment, comment_id)
    return render_template("comments.html", comments=comments,
                           prev=prev_page_comment, next=next_page_comment, sel="comments")


@frontend.route("/show")
def show():
    # todo: implement
    return render_template("not_implemented.html", sel="show")


@frontend.route("/ask")
def ask():
    # todo: implement
    return render_template("not_implemented.html", sel="ask")


@frontend.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    form = SubmitPost()
    if request.method == "POST" and form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        post.author_id = current_user.id
        db.session.add(post)
        db.session.commit()
        return redirect("/")
    return render_template("submit.html", form=form, sel="submit")
