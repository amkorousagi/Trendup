FROM ubuntu:latest

# install tools
RUN apt update
RUN apt install -y python3
RUN apt install -y git

# download code
RUN mkdir example
WORKDIR /example
RUN git clone https://github.com/amkorousagi/Trendup.git

# environment
EXPOSE 5001/tcp
EXPOSE 5002/tcp
EXPOSE 5003/tcp

# when run builded image
# CMD
ENTRYPOINT /bin/bash
