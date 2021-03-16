# Dynamic-Pattern-ROS
* [開發的作業環境]()
* [問題]()
1. [工作流程]()
2. [如何在Docker使用]()
#### 開發的作業環境
* Ubuntu 20.04
* Docker 20.10.5
* Docker-compose 1.28.5

## 工作流程
![](https://i.imgur.com/iLG90EX.png)
* Step 1.使用UI來產生json
![](https://i.imgur.com/EkquMT8.png)
* Step 2.取得json產生圖檔
![](https://i.imgur.com/EqVozE8.png)
* Step 3.取得圖檔並顯示
![](https://i.imgur.com/SyoCrib.png)

## 如何在Docker使用

1. ```
    git clone https://github.com/U07157135/Dynamic-Pattern-ROS.git
   ```
2. ```
    cd Dynamic-Pattern-ROS 
   ```
3. ```
    docker-compose up
   ```
4. ```
    sudo aptitude install remmina
   ```
5. 設定Remmina
![](https://i.imgur.com/129DVGI.png)
![](https://i.imgur.com/tAMAswf.png)
* service的ip固定為127.0.0.1，port為```docker-compose.yml```中設定的port，在本範例control_node跟show_node port分別為5655跟5656
* Username在control_node跟show_node都是lab103
* Password在control_node跟show_node都是lab103
* Resolution可以自訂
6. 連線進入control_node跟show_node的桌面
![](https://i.imgur.com/WJ54OIT.png)
7. control_node的桌面
    1. ```
       sudo su 
       ```
    2. ```
       cd /root/dev_ws/src
       ```
    3. ```
       . install/setup.bash
       ```
    4. ```
       python3 control_pattern_node/control_pattern_node/UI.py
       ```
8. show_node的桌面
    1. ```
       sudo su 
       ```
    2. ```
       cd /root/dev_ws/src
       ```
    3. ```
       . install/setup.bash
       ```
    4. ```
       ros2 run show_pattern_node show
       ```