FROM mickahell/quantum_lab_qiskit:latest

# Var for labels
ARG GITHUB_ACTOR
ARG GITHUB_REPOSITORY
ARG GITHUB_REF

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

LABEL org.opencontainers.image.title="q-kernel-ops" \
      org.opencontainers.image.authors=${GITHUB_ACTOR} \
      org.opencontainers.image.vendor=${GITHUB_REPOSITORY} \
      org.opencontainers.image.source="https://github.com/Travis-S-IBM/q-kernel-ops" \
      org.opencontainers.image.url="https://github.com/Travis-S-IBM/q-kernel-ops" \
      org.opencontainers.image.description="Games" \
      org.opencontainers.image.os="q-kernel-ops" \
      org.opencontainers.image.version=${GITHUB_REF}

RUN apt-get update -yq && apt-get dist-upgrade -yq

RUN mkdir /opt/experiments

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install Jinja2

VOLUME /opt/experiments

COPY docker/start.sh .

CMD ./start.sh
