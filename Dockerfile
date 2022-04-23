FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# Install dependecies
RUN apt update
RUN apt install -y build-essential autotools-dev libdumbnet-dev libluajit-5.1-dev libpcap-dev libpcre3-dev zlib1g-dev pkg-config libhwloc-dev cmake
RUN apt install -y liblzma-dev openssl libssl-dev cpputest libsqlite3-dev
RUN apt install -y libtool git autoconf
RUN apt install -y bison flex wget libcurl4-openssl-dev

# Install Flatbuffers
RUN apt install -y flatbuffers-compiler

# Install safec
RUN wget https://downloads.sourceforge.net/project/safeclib/libsafec-10052013.tar.gz
RUN tar -xzvf libsafec-10052013.tar.gz
RUN cd libsafec-10052013 && ./configure && make && make install

# Install Python 3.+
RUN apt-get install -y python3.6

# Install daq
RUN git clone https://github.com/snort3/libdaq.git
RUN cd libdaq && ./bootstrap && ./configure && make && make install

# Update shared library
RUN ldconfig

# Install snort
RUN wget -O snort3.tar.gz https://github.com/snort3/snort3/archive/master.tar.gz
RUN tar -xvzf snort3.tar.gz
RUN cd snort3-master && ./configure_cmake.sh --prefix=/opt/snort && cd build && make && make install
RUN ln -s /opt/snort/bin/snort /usr/sbin/snort

# Install Flatbuffers
RUN git clone -b v2.0.0 --depth=1 --recursive https://github.com/google/flatbuffers.git
RUN cd flatbuffers && cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release && make && make install

# Install Snort3 Plugin
ADD plugin ./plugin
RUN export PKG_CONFIG_PATH=/opt/snort/lib/pkgconfig/ && cd ./plugin && ./configure_cmake.sh --prefix=/opt/snort && cd build && make && make install

# Install Python
RUN apt-get install -y python3-pip
ADD AnalysisServer ./AnalysisServer
RUN cd AnalysisServer && pip install -r requirements.txt
WORKDIR AnalysisServer
EXPOSE 5000

# Enable plugin
ADD ./plugin/snort.lua /opt/snort/etc/snort/snort.lua
ENV LUA_PATH /opt/snort/include/snort/lua/\?.lua\;\;
ENV SNORT_LUA_PATH /opt/snort/etc/snort

# CMD ["python3", "main.py"]

# ENTRYPOINT [ "snort", "-c", "/opt/snort/etc/snort/snort.lua", "--plugin-path", "/opt/snort/lib/snort/plugins/extra/", "-i", "eth0" ]