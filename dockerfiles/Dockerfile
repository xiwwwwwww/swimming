FROM ubuntu:24.04

ARG CI=false
ARG PYTHON_VERSION=3.12
ARG JAVA_VERSION=17
ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}" \
    PATH="${HOME_DIR}/.local/bin:${PATH}"

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
    libssl-dev \
    libtool \
    make \
    openjdk-${JAVA_VERSION}-jdk \
    patch \
    pkg-config \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    sudo \
    unzip \
    xz-utils \
    zip \
    zlib1g-dev

RUN useradd --create-home --shell /bin/bash ${USER} && \
    usermod -append --groups sudo ${USER} && \
    echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER ${USER}
WORKDIR ${WORK_DIR}

RUN python3 -m venv ${HOME_DIR}/venv
ENV PATH="${HOME_DIR}/venv/bin:${PATH}" \
    VIRTUAL_ENV="${HOME_DIR}/venv"

RUN pip install --upgrade buildozer setuptools Cython==0.29.33 cmake

COPY . ${WORK_DIR}
RUN if [ "${CI}" = "true" ]; then sed 's/log_level = [0-9]/log_level = 1/' -i buildozer.spec; fi
ENTRYPOINT ["./dockerfiles/start.sh"]