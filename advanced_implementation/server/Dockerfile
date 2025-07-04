FROM centos:7

# Install Python 3 e pip
RUN yum update -y && \
    yum install -y epel-release && \
    yum install -y python3 python3-pip && \
    yum clean all

# Install Twisted
RUN pip3 install twisted

# Create work diretory
WORKDIR /app

# Copy server files
COPY server.py .
COPY logic.py .
COPY schemas.py .

EXPOSE 5678

# Comand to run server
CMD ["python3", "server.py"]