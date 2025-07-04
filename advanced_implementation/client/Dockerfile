FROM centos:7

# Install Python 3 and pip
RUN yum update -y && \
    yum install -y epel-release && \
    yum install -y python3 python3-pip && \
    yum clean all

# Install Twisted
RUN pip3 install twisted

# Create work diretory
WORKDIR /app

# Copy Client files
COPY client.py .

# Command to run the client
CMD ["python3", "client.py"]