
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

# this is the root route for the flask application
@bp.route('/')
# index function
def index():
    # the variable db is set to equal the get_db function
    db = get_db()

    # posts is set to equal the db.execute() which is a table query
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
        # fetch all is a function which gets all the instances this matches
    ).fetchall()
    # returning the template index.html so the posts will show up on the index page
    return render_template('blog/index.html', posts=posts)

# this the root for an many individual full.html pages
@bp.route('/<int:id>/full', methods=('GET', 'POST'))
# full function which displays the full view
def full(id):
    # post is equal to the function get_post_public which has an argument of id
    post = get_post_public(id)
    # db is set to the get_db fuction so db will be the database info
    db = get_db()
    # comments is equal to the database execute the query below.
    comments = db.execute(
        # selecting the comments records
        'SELECT c.id, c.body, c.created, c.author_id, c.user_id, c.post_id'
        # the data is from the comment table which is joined on user which author id equaling users id
        # and post is also joined to comment on comments post_id is equal to post's id
        ' FROM comment c JOIN user u ON c.author_id = u.id JOIN post p ON c.post_id = p.id'
        # the data is then ordered by when they were created in descending order
        ' ORDER BY c.created DESC'
        # getting all instances of comments
    ).fetchall()
    # conditional which only occurs if request.method is equal to the method of 'POST'
    if request.method == 'POST':
           # the variable createComment is equal to the request.form which has a 'createComment' instance
        createComment = request.form['createComment']
        # the variable is equal to error
        error = None
        # conditional which only occurs if createComment does not exist
        if not createComment:
            # sets the error variable equal to the string below
            error = 'Content is required.'
        # conditional which only occures if the variable error is not equal to None
        if error is not None:
            # error variable is passed to the flash function as an argument
            flash(error)
        # if all passes then the following code will run
        else:
            # db varaible is equal to get_db() function
            db = get_db()
        # then the db executes the query
            db.execute(
                # creating a insert into query which has the columns body, id and author_id
                'INSERT INTO comment (body, post_id, author_id)'
                # the following values will be entered (the user chooses the random values)
                ' VALUES (?, ?, ?)',
                # the createComment variable is set to the body, id to the id and g.user_id (the user id) to author_id
                (createComment, id, g.user['id'])
            )
            # adding the values to the database
            db.commit()
    # taking the user back to the blog.full url
            return redirect(url_for('blog.full'))

    # returning the render template function which has two arguments the path for full.html and setting post=post
    return render_template('blog/full.html', post=post)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


# def get_title(title):
    # get all titles that match the form
#    post = get_db().execute(
#        'SELECT p.id, title'
#        'FROM post p JOIN search s on  = s.post_id'
#        'WHERE p.title = ?'
#        (id, title)
#    ).fetchone()

#    if title is None:
#        abort(404, "Post title {0} doesn't exist")


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


def get_post_public(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return post


# def get_comment(id, check_author=True):
#    post = get_db().execute(
#        'SELECT c.id, body, created, author_id, username'
#        ' FROM comments c JOIN user u ON c.author_id = u.id'
#        'WHERE c.id = ?'
#        (id,)
#    ).fetchone()

#    if comment is None:
#        abort(404, "Comment id {0} doesn't exist".format(id))
#    return comment


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


# bp.route('/<int:id>/full/comments/comment')
# def update_comment(id):

#    comment = get_comment(id)

#    if request.method == 'POST':
#        body = request.form['body']
#        error = None

#        if error is not None:
#            flash(error)

#        else:
#            db = get_db()
#            db.execute(
#                'UPDATE comment SET body = ?'
#                'WHERE id = ?',
#                (id, )
#            )
#            db.commit()
#            return redirect('full/comments/comment')
#        return render_template('blog/full.html', comment=comment)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


#    get_comment(id)
#    db = get_db()
#    db.execute('DELETE FROM comment WHERE id = ?', (id,))
#    db.commit()
#    return redirect(url_for('blog.full'))
