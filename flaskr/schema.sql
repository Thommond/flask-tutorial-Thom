DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS comment;

--creating the user table
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

--creating the post table
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
--Searches for title of posts
--we need info as the post_id to connect the search table to the post table
--a function is needed to update the database
--in the function a db connection will be added
--conditional to prevent breaking in the code
--button in the html
--that form will be the search result
--redirecting to the page in a return
--select s.id, s.post_id, s.title_searched from
--search posts then need to be ordered by the searched title

--creating comment table
CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  user_username TEXT UNIQUE NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  body TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
  FOREIGN KEY (user_username) REFERENCES user (username)
  FOREIGN KEY (post_id) REFERENCES post (id)
)
