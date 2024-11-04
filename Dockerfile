FROM python:3.12

# Set work directory
WORKDIR /usr/src

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev wget make && \
    rm -rf /var/lib/apt/lists/*

# Install a newer version of SQLite (3.31 or higher)
# RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3420000.tar.gz && \
#     tar xvfz sqlite-autoconf-3420000.tar.gz && \
#     cd sqlite-autoconf-3420000 && \
#     ./configure && make && make install && \
#     cd .. && rm -rf sqlite-autoconf-3420000*

# Confirm SQLite version
# RUN sqlite3 --version

# Install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY ./src /usr/src/
