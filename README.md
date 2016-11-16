# greenfield-flask
Dockerized test management tool using Flask, SQLAlchemy, Jinja2 and Bootstrap

Clone repo `git clone https://github.com/maciejd/greenfield-flask.git`

Chande directory `cd greenfield-flask`

Build image `docker build -t greenfield .` 
  
Run container in detached mode and publish port 5000 `docker run -d -p 5000:5000 greenfield`
  
App should be accessible on port 5000 `http://localhost:5000`
