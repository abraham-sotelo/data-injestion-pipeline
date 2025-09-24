FROM ubuntu:24.04
LABEL Name="Sensor Data Collection Pipeline" \
      Author="Abraham Sotelo"
ARG USERNAME
ARG UID
ARG GID
ARG TZ_PATH

RUN groupadd -g ${GID} ${USERNAME} && \
  useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USERNAME}
RUN ln -fs ${TZ_PATH} /etc/localtime

RUN apt update && apt install -y\
  tzdata \
  sudo \
  git \
  curl \
  python3 \
  unzip \
  wget

RUN wget https://github.com/Wilfred/difftastic/releases/download/0.60.0/difft-x86_64-unknown-linux-gnu.tar.gz &&\
  tar xvf difft-x86_64-unknown-linux-gnu.tar.gz &&\
  mv difft /usr/local/bin/