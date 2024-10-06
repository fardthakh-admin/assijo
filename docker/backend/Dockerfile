FROM python:3.9

WORKDIR /home/backend

ADD ./requirements.txt /home/backend


# COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# # running migrations
# RUN python manage.py migrate

ADD ./ /home/backend

# gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
RUN ["chmod", "+x", "/home/backend/docker/backend/wsgi_entrypoint.sh"]
