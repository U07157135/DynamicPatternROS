FROM s415018/ros:foxy-desktop

WORKDIR /root/dev_ws/src

COPY requirements.txt ./requirements.txt
COPY src ./


RUN \
  apt-get update &&\
  apt-get upgrade -y &&\
  apt-get install python3-pip -y &&\
  pip3 install -r requirements.txt &&\
  rm requirements.txt &&\
  apt-get install python3-colcon-common-extensions -y &&\
  sh -c "echo source /opt/ros/foxy/setup.bash" >> /root/.bashrc
  

RUN . /opt/ros/foxy/setup.sh && \
    colcon build


