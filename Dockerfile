FROM --platform=linux/amd64 ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York


# Dependencies for glvnd and X11.
RUN apt-get update \
  && apt-get install -y -qq --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libxext6 \
    libx11-6 \
    freeglut3-dev \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
  && apt-get install -y -qq --no-install-recommends \
  cmake libx11-dev xorg-dev libglu1-mesa-dev freeglut3-dev libglu1-mesa libglu1-mesa-dev libgl1-mesa-glx libgl1-mesa-dev libglfw3-dev libglfw3 libglew2.2 libglew-dev

# RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    zip \
    unzip \
    cmake \
    bzip2 \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    gcc \
    perl \
    python3 \
    python2.7 \
    python3-distutils \
    automake \
    build-essential \
    libz-dev

RUN apt install -y --reinstall python3-pkg-resources python3-setuptools

# install porechop from github
RUN wget -q https://github.com/rrwick/Porechop/archive/refs/tags/v0.2.4.zip \
    && unzip v0.2.4.zip \
    && rm v0.2.4.zip \
    && cd Porechop-0.2.4 \
    && python3 setup.py install

# install necat
RUN wget -q https://github.com/xiaochuanle/NECAT/releases/download/v0.0.1_update20200803/necat_20200803_Linux-amd64.tar.gz \
    && tar xzvf necat_20200803_Linux-amd64.tar.gz
RUN cd NECAT/Linux-amd64/bin \
    && cp -r /NECAT/Linux-amd64/bin/* /usr/local/bin


# Inspector installation
RUN wget https://github.com/Maggi-Chen/Inspector/archive/refs/tags/v1.0.2.zip \
    && unzip v1.0.2.zip \
    && cd Inspector-1.0.2 \
    && cp -r * /usr/local/bin

# Download and install Miniconda for Python 2.7
RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh && \
    bash Miniconda2-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda2-latest-Linux-x86_64.sh && \
    /opt/conda/bin/conda init bash

# Add Miniconda to the PATH
ENV PATH="/opt/conda/bin:$PATH"

ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# Pull the environment name out of the environment.yml
RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH


WORKDIR /app

ENTRYPOINT ["python3", "./scripts/fhgaon.py"]
