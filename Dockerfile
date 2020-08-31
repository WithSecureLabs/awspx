FROM neo4j:3.5.13

COPY . /opt/awspx
WORKDIR /opt/awspx

ENV NEO4J_AUTH=neo4j/password
ENV EXTENSION_SCRIPT=/opt/awspx/INSTALL

RUN apt -y update && apt install -y \
        nodejs \
        npm \
        python3-pip \
        procps \
        git \ 
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade \
        argparse \
        awscli-local \
        boto3 \
        configparser \
        git-python \
        neo4j \
        rich \
    && npm install -g npm@latest 

RUN cd /opt/awspx/www && npm install 

VOLUME /opt/awspx/data
EXPOSE 7373 7474 7687 80 
