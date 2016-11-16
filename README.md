# greenfield-flask
Dockerized test management tool using Flask, SQLAlchemy, Jinja2 and Bootstrap

1. Clone repo `git clone https://github.com/maciejd/greenfield-flask.git`

2. Chande directory `cd greenfield-flask`

3. Build image `docker build -t greenfield .` 
  
4. Run container in detached mode and publish port 5000 `docker run -d -p 5000:5000 greenfield`
  
5. App should be accessible on port 5000 `http://localhost:5000`

Admin credentials: admin/admin


