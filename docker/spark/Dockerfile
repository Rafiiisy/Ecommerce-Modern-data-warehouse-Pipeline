FROM bitnami/spark:3.4.0

# Switch to root to install dependencies
USER root

# Install required build tools and Python dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gawk \
    bison \
    build-essential \
    manpages-dev \
    python3-pip && \
    apt-get clean

# Install GLIBC 2.32
RUN wget http://ftp.gnu.org/gnu/libc/glibc-2.32.tar.gz && \
    tar -xvzf glibc-2.32.tar.gz && \
    cd glibc-2.32 && \
    mkdir build && cd build && \
    ../configure --prefix=/opt/glibc-2.32 && \
    make -j$(nproc) && \
    make install && \
    cd ../.. && rm -rf glibc-2.32 glibc-2.32.tar.gz

# Update the library path to include the new GLIBC
ENV LD_LIBRARY_PATH=/opt/glibc-2.32/lib:$LD_LIBRARY_PATH

# Install Python dependencies
RUN pip3 install pyspark py4j numpy pandas

# Switch back to non-root user
USER 1001
