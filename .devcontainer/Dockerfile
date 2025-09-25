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
  python3.12-venv \
  unzip \
  wget \
  zip

RUN wget https://github.com/Wilfred/difftastic/releases/download/0.60.0/difft-x86_64-unknown-linux-gnu.tar.gz &&\
  tar xvf difft-x86_64-unknown-linux-gnu.tar.gz &&\
  mv difft /usr/local/bin/

RUN apt update && apt install -y gnupg software-properties-common &&\
  wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null &&\
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list &&\
  apt update && apt install terraform

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" &&\
  unzip awscliv2.zip && ./aws/install