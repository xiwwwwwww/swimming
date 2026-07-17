FROM ubuntu:24.04

ARG CI=false
ARG PYTHON_VERSION=3.12
ARG JAVA_VERSION=17
ENV USER="user"
ENV HOME_DIR="/home/"
ENV WORK_DIR="" \
    PATH="/.local/bin:"

RUN apt update -qq > /dev/null && apt install -qq --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

RUN apt update -qq > /dev/null && apt install -qq --yes --no-install-recommends \
    autoconf \
    automake \
    ca-certificates \
    cmake \
    curl \
    gettext \
    git \
    libffi-dev \
    libltdl-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libpython-dev \
    libssl-dev \
    libtool \
    make \
    openjdk--jdk \
    patch \
    pkg-config \
    python \
    python-venv \
    python3-pip \
    sudo \
    unzip \
    xz-utils \
    zip \
    zlib1g-dev

RUN useradd --create-home --shell /bin/bash  && \
    usermod -append --groups sudo  && \
    echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER 
WORKDIR 

RUN python3 -m venv /venv
ENV PATH="/venv/bin:" \
    VIRTUAL_ENV="/venv"

RUN pip install --upgrade buildozer setuptools Cython==0.29.33 cmake

COPY . 
RUN if [ "" = "true" ]; then sed 's/log_level = [0-9]/log_level = 1/' -i buildozer.spec; fi
ENTRYPOINT ["./dockerfiles/start.sh"]