FROM s415018/ros:foxy-devel-20.04


COPY src /opt/src
COPY ./ros_entrypoint.sh /
COPY requirements.txt /requirements.txt

RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y python3-pip &&\ 
    pip3 install -r requirements.txt &&\
    apt-get install -y libgl1-mesa-glx &&\
    apt-get install -y python3-colcon-common-extensions

RUN cd /opt/src &&\
    . /opt/ros/foxy/setup.sh &&\
    colcon build

RUN chmod 777 /opt/src/install/setup.bash &&\
    chmod 777 /ros_entrypoint.sh

