# YOLOv8-Traffic-Monitoring-System
**Đây là một hệ thống giám sát giao thông sử dụng thuật toán YOLO và ngôn ngữ lập trình Python.**
## Hệ thống này được thiết kế để nhận diện các phương tiện giao thông trên đường gồm 5 loại ( xe máy , xe đạp , xe ô tô , xe tải , xe bus)
## Một số tính năng chính 
- 1 . Đếm số lượng xe vi phạm
- 2 . Thống kế lượng xe vi phạm trong ngày , trong năm 
- 3 . In Biên Bản phạt tiền đối Xe Vi Phạm đi sai làn đường 
- 4 . Phát hiện xe máy vi phạm ko đội mũ bảo hiểm
- 5 . Tracking đối với phương tiện 
## Triển khai lên web sử dụng [Flask](https://flask.palletsprojects.com/en/2.3.x/) và Database [MYSQL](https://www.mysql.com/)
![Hình ảnh](https://flask.palletsprojects.com/en/2.3.x/_images/flask-horizontal.png)
# Python version
This project was generated with [Python](https://www.python.org/downloads/release/python-3913/) version 3.9.13.
# YOLO version
This project was generated with [YOLO](https://github.com/autogyro/yolo-V8) version YOLOV8..
<p float="left">
  <img src="https://ultralytics.com/static/backgrounds/vision.svg" width="400" />
  <img src="https://ultralytics.com/static/yolov8/community.svg" width="400" /> 
</p><br><br>

# HƯỚNG DẪN SỬ DỤNG CODE

## 2.	Cài đặt các phần mềm liên quan 
### 2.1.	Hướng dẫn cài đặt và sử dụng cơ sở dữ liệu MySQL Server và MySQL Workbench 8.0.2.0
## B1: Download phần mềm tại đường dẫn.
- https://dev.mysql.com/downloads/installer/ 
	### Link hướng dẫn cài đặt Mysql: 
- https://www.youtube.com/watch?v=BYwb50Xbf8s 
####           Lưu ý : Sau khi cài đặt thành công, lúc tạo tài khoản và mật khẩu để đăng nhập cần phải ghi nhớ để đăng nhập vào database và giúp cho python kết nối được với database rất cần thiết cho việc chạy project.
#### Sau khi tải xong, chúng ta vào bấm 2 lần vào khu vực như hình bên dưới và đăng nhập với tài khoản và mật khẩu lúc cài đặt MySQL. 
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh1.png)
<br><br>
Vào được như hình dưới  là chúng ta đã cài đặt thành công 
<br><br>
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh2.png)
 
## 2.2.	Hướng dẫn cài đặt phần mềm Pycharm và Python
### 2.2.1.	 Tải và cài đặt phần mềm Pycharm
## B1: Download PyCharm:
- https://www.jetbrains.com/pycharm/download/?section=windows
### Link youtube hướng dẫn: 
- https://www.youtube.com/watch?v=0Jt6npqCmU4
### 2.2.2.	Tải và cài đặt Python 
#### Lưu ý : Chúng ta nên cài đặt Python version 3.9.13 đối với windown 10 hoặc có thể cài đặt Python version: 3.10 phiên bản mới nhất đối với windown 11 thì mới có thể chạy được project với YOLOv8.
### Link download python 3.9.13:
- https://www.python.org/downloads/release/python-3913/
### Link youtube hướng dẫn:
- https://www.youtube.com/watch?v=tgG2BjygiAM
## 3.	Hướng dẫn thực hiện tạo bảng cở sở dữ liệu trong MySQL
### B1: Sau khi tải và đăng nhập vào MySQL (giao diện như mục 2.1 hình thứ 2).
### B2: Mở file “codeDatabase.txt” => Copy nội code => đưa vào MYSQL và chạy code bên MySQL. Trình tự thực hiện như hình bên dưới.
<br><br>
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh3.png)
<br><br>
#### Nếu hiển thị như bước thứ 5 trong hình ảnh trên là quá trình khởi tạo databse thành công.
## 4.	Hướng dẫn train model với YOLOv8 trên GOOGLE COLAB
## B1: Tạo thư mục trên Driver sau đó Upload thư mục DATA lên google Driver, trình tự thực hiện như hình bên dưới.
<br><br>
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh4.png)
<br><br>
### B2: Sau khi tạo file trên Google Colab , tiến hành liên kết với driver và cài đặt YOLOv8 trên google Colab
<br><br>
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh5.png)
<br><br>
### B3: Chạy lệnh huấn luyện với thư mục DATA vừa upload lên google Driver ở B1
<br><br>
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh6.png)
<br><br>
## 5.	Hướng dẫn chạy Project với Pycharm
### B1: Download python_project về máy tính. 
### B2: Vào thư mục python_project.
### B3: Tiến hành mở “python_project” với Pycharm như hình bên dưới.
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh7.png)
 
### B4: Sau khi mở dự án với Pycharm tiến hành cài đặt các thư viện như hình bên dưới.
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh8.png)
 
- Nếu một số File bị lỗi thư viện thì tiến hành cài đặt thư viện đó bằng 2 cách như bên dưới:
#### Cách 1: Sử dụng terminal: 
- Cách thực hiện: Mở lệnh terminal và gõ lệnh : 
`Pip install [tên thư viên bị lỗi]` 
#### Cách 2: Cài đặt thư viện thông qua phần mềm Pycharm như hình dưới.
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh9.png)

### B5:  Sau khi cài đặt tất cả các thư viện thành công, vào file app_server và chạy chương trình
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh10.png)
 
-	Kết quả cuối cùng:
![Hình ảnh](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh11.png)
<br><br>
**Xem video demo tại đây:**
   [![Video Demo](https://raw.githubusercontent.com/LHHT-DISCOVERY/YOLOv8-Traffic-Monitoring-Systems/main/IMG_IMPL/%E1%BA%A2nh11.png)](https://www.youtube.com/watch?v=Z-aQCrljl3A)

# Liên hệ

## Nếu bạn có bất kỳ câu hỏi, đề xuất hoặc báo cáo vấn đề, xin vui lòng liên hệ với chúng tôi:
<br><br>

|     **Tên**       |       **Email**      |      **Facebook**                               |          **GitHub**               |
|-------------------|----------------------|-------------------------------------------------|-----------------------------------|
| LÝ HUỲNH HỮU TRÍ  |  lytri102@gmail.com  | https://www.facebook.com/lyshuynhshuustris.tris | https://github.com/LHHT-DISCOVERY |
 
