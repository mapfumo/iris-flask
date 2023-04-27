# iris-flask

The scikit-learn Iris data-set consists of 3 (Setosa, Versicolour, and Virginica) species (50 samples per species, for a total of 150 samples) of the iris flower. Each sample has four measurements: sepal length, sepal width, petal length, petal width. Given these measurements a machine learning model can predict the iris specie with a high degree of accuracy. Here I demonstrate a machine learning web application using Python, Scikit-Learn machine learning library and Flask web framework.

pip install -r requirements.txt

### To run

    python3 app.py

### Installation & Hosting on Amazon EC2 (Ubuntu Server)

    apt-get install python3 python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y

    apt-get install nginx -y
    systemctl start nginx
    systemctl enable nginx

    git clone <https://github.com/mapfumo/iris-flask.git>
    cd iris-flask
    python3 -m venv iris-flask
    source venv/bin/activate

    pip install -r requirements.txt
    pip install wheel
    pip install gunicorn flask

create wsgi.py
---

    from app import app
    if __name__ == "__main__":
        app.run()

create /etc/systemd/system/iris-flask.service
---

[Unit]
Description=Gunicorn instance to serve iris-flask
After=network.target

[Service]
User=root
Group=www-data

WorkingDirectory=/home/ubuntu/iris-flask
Environment="PATH=/home/ubuntu/iris-flask/venv/bin"
ExecStart=/home/ubuntu/iris-flask/venv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target

## Configuring Nginx to Proxy Requests

create /etc/nginx/sites-available/iris-flask
---
