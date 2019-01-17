

# Trading Card Generator

## Setup

Installation is described on an Ubuntu Server running Nginx.

Clone Repo:

```bash
git clone git@github.com:ramsaut/trading_cards.git
cd trading_cards
```

Virtual Python Environment and install Python packages

```bash
apt-get install python3-venv virtualenvwrapper bdist_wheel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ./manage.py migrate
```

Nodejs and npm

```bash
sudo apt install nodejs npm
npm install
```

Install gunicorn with supervisor

```
pip install django gunicorn psycopg2
apt install supervisor
nano /etc/supervisor/conf.d/gunicorn.conf
```

Content of the file:

```
[program:gunicorn]
directory=/var/www/trading_cards
command=/var/www/trading_cards/venv/bin/gunicorn --workers 3 --bind unix:/var/www/trading_cards/trading_cards/trading_cards.sock trading_cards.wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/gunicorn.out.log
stdout_logfile=/var/log/gunicorn/gunicorn.err.log
user=root
group=www-data
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8

[group:guni]
programs:gunicorn
```



Update supervisor to monitor the gunicorn process we’ve just created by running:

```
supervisorctl reread
supervisorctl update
supervisorctl status
```

Configuring Nginx

nano /etc/nginx/site-available/09-trading-card.conf

```nginx
server {
   listen 80;
    server_name tcg.timo-ramsauer.de;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/trading_cards/;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/trading_cards/trading_cards/trading_cards.sock;
    }
}
```

Enable site:

```bash
ln -s /etc/nginx/sites-available/09-trading-card.conf /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx
```

Install pdflatex:

```
apt install texlive-latex-recommended texlive-generic-extra texlive-latex-extra
```

Install MyriadPro:

https://github.com/sebschub/FontPro

There is an AUR package: https://aur.archlinux.org/packages/texlive-myriadpro-git/

