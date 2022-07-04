FROM ubuntu:22.10

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get -y install fzf

RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"