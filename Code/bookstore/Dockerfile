FROM python:3.10.4-alpine3.15

RUN pip install --upgrade pip

# Add temporary virtual environment dependencies
RUN apk add --no-cache \
    gcc \
    git \
    libc-dev \
    libffi-dev \
    openssl-dev \
    py3-pip \
    zlib-dev 

RUN apk add g++ make subversion gcc gfortran ca-certificates python3-dev libpng-dev freetype-dev python3

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN python3 -m pip install reportlab

# These dependency packages cannot be removed because they continue to be used in PyMupdf
RUN apk --no-cache add 	py3-reportlab ocrmypdf
ENV PATH="/home/django/.local/bin:${PATH}"
RUN adduser -D django
USER django
WORKDIR /home/django

COPY . .

COPY --chown=django:django . .

RUN pip install --user -r requeriments.txt

COPY --chown=django:django . .

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]