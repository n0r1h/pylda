FROM python:3.9.17-buster

WORKDIR /code

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y -q \
    libssl-dev \
    libpq-dev \
    pkg-config \
    build-essential \
    libdbus-1-dev \
    software-properties-common \
    curl \
    gnupg \
    git

RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN apt-get install nodejs -y
ENV NODE_MAJOR=20
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt-get update
RUN apt-get install nodejs -y

RUN git clone https://github.com/vim/vim.git
WORKDIR vim
RUN ./configure --with-features=huge
RUN make
RUN make install

COPY .vim /root/.vim/
COPY .vimrc /root/.vimrc

COPY ./requirements.txt /code
COPY src /code/
WORKDIR /code
RUN pip install -r requirements.txt
