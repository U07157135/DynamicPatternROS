# 20200316 - 動態圖靶ROS節點
1. [老師要求的規格 - 動態圖靶ROS節點](https://hackmd.io/_uznmnqNTrmYzlJ0fYySUQ#%E8%80%81%E5%B8%AB%E8%A6%81%E6%B1%82%E7%9A%84%E8%A6%8F%E6%A0%BC---%E5%8B%95%E6%85%8B%E5%9C%96%E9%9D%B6ROS%E7%AF%80%E9%BB%9E)
2. [解決方案](https://hackmd.io/_uznmnqNTrmYzlJ0fYySUQ#%E8%A7%A3%E6%B1%BA%E6%96%B9%E6%A1%88)
3. [動態圖靶 - 節點架構圖](https://hackmd.io/_uznmnqNTrmYzlJ0fYySUQ#%E5%8B%95%E6%85%8B%E5%9C%96%E9%9D%B6---%E7%AF%80%E9%BB%9E%E6%9E%B6%E6%A7%8B%E5%9C%96)
4. [Step1. UI Node](https://hackmd.io/_uznmnqNTrmYzlJ0fYySUQ#Step1-UI-Node)
5. [ROS資料傳遞: Step1.UI節點 >>> Step2.Make節點](https://hackmd.io/_uznmnqNTrmYzlJ0fYySUQ#ROS%E8%B3%87%E6%96%99%E5%82%B3%E9%81%9E-Step1UI%E7%AF%80%E9%BB%9E-gtgtgt-Step2Make%E7%AF%80%E9%BB%9E)
6. [Step2. Make節點](https://hackmd.io/_uznmnqNTrmYzlJ0fYySUQ#Step2-Make%E7%AF%80%E9%BB%9E)
7. [ROS資料傳遞: Step2.Make節點 >>> Step3.Show節點](https://hackmd.io/_uznmnqNTrmYzlJ0fYySUQ#ROS%E8%B3%87%E6%96%99%E5%82%B3%E9%81%9E-Step2Make%E7%AF%80%E9%BB%9E-gtgtgt-Step3Show%E7%AF%80%E9%BB%9E)
8. [Step3. Show節點](https://hackmd.io/_uznmnqNTrmYzlJ0fYySUQ#Step3-Show%E7%AF%80%E9%BB%9E)
# 老師要求的規格 - 動態圖靶ROS節點

1. 以Json描述圖靶內容  
3. 圖靶內容，可修改：  
>&ensp; a. 每圈半徑大小  
&ensp; b. 每圈中心點位置  
&ensp; c. 每圈顏色  
&ensp; d. 圖靶外觀分為: 方形、圓形  
&ensp; e. 開啟/關閉 十字線  
3. 在Docker上實現ROS架構  
4. 將動態圖靶 建立為1個 獨立的ROS Node  


# 解決方案

我們設計以下3個節點，以完成以上一系列動作：

**Step1. UI 節點：** 設定GUI，產生描述圖把的Json內容  
**Step2. Make 節點：** 將Json內容轉為png圖檔，並儲存  
**Step3. Show 節點：** 讀取 png圖檔，顯示到螢幕上  

最終，當需要修改圖靶時，  
只需要對 **Step2. Make節點** 以**ROS Request**發送Json內容即可改變圖靶。

# 動態圖靶 - 節點架構圖

以下各節點個能說明：

![](https://i.imgur.com/vrn09ty.png)


# Step1. UI Node

以GUI視覺化方式，設定描述圖靶內容的Json資料結構，而**不需要手動編輯**Json檔案內容。

其GUI元件功能說明如下：  
1. Shape欄位：每一圈圖靶的外觀  
2. Radius欄位：每一圈圖靶的半徑  
3. Color欄位：每一圈圖靶的顏色  
4. Position欄位：每一圈圖靶的中心點座標  
5. Cross Line：開啟/關閉 十字標線  
6. Open按鈕：將GUI設定的內容，轉為Json資料結構  


![](https://i.imgur.com/qqDHv2a.png)


由UI編輯後的Json的資料內容如下圖：

![](https://i.imgur.com/5eAWwQw.png)



## ROS資料傳遞: Step1.UI節點 >>> Step2.Make節點

由Step1. UI節點 所產生的Json資料內容，將直接轉為String資料型態 傳送至Step2. Make節點
![](https://i.imgur.com/jA0RqnL.png)


# Step2. Make節點
1. 當接收到Step1. UI節點傳送過來的圖靶描述內容時(String)，將其轉換回Json格式
2. 在Python中，使用json.load()方法將圖靶描述(String)內容存為 Dictionary
3. 使用OpenCV依據讀取的Dictionary，產生並儲存圖靶的PNG圖檔，檔名<font color=#FF0000>**暫定**</font>為 **circle.png**
4. circle.png將儲存在 Make節點的Docker內，檔案路徑：根目錄(/circle.png)，如下圖**黃框處**
![](https://i.imgur.com/Y3kFUzc.png)


## ROS資料傳遞: Step2.Make節點 >>> Step3.Show節點
Step2.Make節點  將circle.png圖檔轉換為Base64編碼  
再將圖檔的Base64編碼以String資料型態 傳送至 Step3. Show節點
![](https://i.imgur.com/9fJS0ZW.png)



# Step3. Show節點
1. 當接收到Step2. Make節點傳送過來的 Base64編碼後，將其轉回圖像格式並存為PNG檔。<br>
儲存的檔名<font color=#FF0000>**暫定**</font>為 **imageToSave.png**<br>
圖檔將儲存在Show節點的Docker內，檔案路徑為： /dev_ws/src/imageToSave.png
![](https://i.imgur.com/E4svGHc.png)


2. 最終，使用Python Tkinter 讀取PNG，顯示在螢幕上。


![](https://i.imgur.com/fu9kZ7q.png)
