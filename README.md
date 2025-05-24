# Giới thiệu đề tài

## Đề tài: **Xây dựng hệ thống tìm kiếm ảnh dựa trên nội dung theo chuẩn MPEG-7**

Hệ thống được thiết kế để tìm kiếm ảnh dựa trên nội dung hình ảnh (Content-Based Image Retrieval - CBIR), tuân theo tiêu chuẩn MPEG-7. Trong đó:

- **VGG16** được sử dụng để trích xuất **đặc trưng hình dạng (shape features)** từ ảnh.
- **DCT (Discrete Cosine Transform)** được sử dụng để trích xuất **đặc trưng màu sắc (color features)**.
- Bộ dữ liệu sử dụng là **`corel_images`** được lấy từ Kaggle.

Mục tiêu của hệ thống là cải thiện độ chính xác trong việc truy vấn ảnh dựa trên nội dung thực tế, phục vụ cho các ứng dụng như lưu trữ, truy xuất và phân loại ảnh.

# Thông tin tác giả

- **Họ và tên:** Nguyễn Minh Hoàng  
- **MSSV:** N21DCCN034  
- **Lớp:** D21CQCNHT01-N

# Mô Tả Chi Tiết Những Gì Đã Làm Trong Dự Án
Dự án cuối kỳ môn Cơ sở dữ liệu đa phương tiện tập trung vào việc xây dựng một ứng dụng hoàn chỉnh để xử lý, trích xuất đặc trưng và tìm kiếm ảnh dựa trên nội dung. Dưới đây là các thành phần chính và chi tiết công việc đã thực hiện:

## 1. Đóng Gói Ứng Dụng
Ứng dụng được thiết kế với kiến trúc ba tầng (frontend, backend, database) và được đóng gói bằng Docker để đảm bảo tính nhất quán và dễ dàng triển khai.

### Frontend:  

Được phát triển bằng HTML, CSS, và JavaScript, tạo giao diện người dùng thân thiện để upload ảnh và hiển thị kết quả tìm kiếm.  
Sử dụng Nginx làm web server để phục vụ các tài nguyên tĩnh (ảnh, file HTML) và xử lý các yêu cầu HTTP từ người dùng.  
Giao diện được tối ưu để hỗ trợ việc upload nhiều ảnh hoặc file zip, đồng thời hiển thị kết quả tìm kiếm một cách trực quan.


### Backend:  

Xây dựng bằng Flask, một framework Python nhẹ và linh hoạt, để xử lý logic nghiệp vụ chính như trích xuất đặc trưng ảnh, lưu trữ dữ liệu, và cung cấp API.  
Các API được thiết kế để giao tiếp với frontend, bao gồm API upload ảnh và API tìm kiếm ảnh tương đồng.


### Database:  

Sử dụng PostgreSQL, một hệ quản trị cơ sở dữ liệu quan hệ mạnh mẽ, kết hợp với extension pgvector để hỗ trợ lưu trữ và truy vấn dữ liệu vector.  
Dữ liệu vector (đặc trưng ảnh) được lưu trữ dưới dạng các cột đặc biệt trong bảng images, tối ưu cho các phép toán tìm kiếm độ tương đồng.


### Triển Khai:  

Toàn bộ ứng dụng được đóng gói bằng Docker Compose, bao gồm ba dịch vụ: frontend, backend, và database.  
File docker-compose.yml định nghĩa các dịch vụ, ánh xạ cổng, volume lưu trữ, và các biến môi trường cần thiết để kết nối giữa các thành phần.



## 2. Trích Xuất Đặc Trưng Ảnh
Để tìm kiếm ảnh dựa trên nội dung, hai phương pháp trích xuất đặc trưng đã được triển khai: VGG16 và DCT.

### VGG16:  

Sử dụng mô hình VGG16 (đã được huấn luyện trước trên tập dữ liệu ImageNet) để trích xuất đặc trưng cấp cao từ ảnh.  
Ảnh đầu vào được chuẩn hóa về kích thước 224x224, sau đó đưa qua mô hình VGG16 với lớp GlobalAveragePooling2D để tạo vector đặc trưng 512 chiều.  
Vector này đại diện cho các đặc điểm ngữ nghĩa của ảnh, phù hợp để so sánh nội dung tổng quát.


### DCT (Discrete Cosine Transform):  

Áp dụng DCT để trích xuất đặc trưng bố cục màu (Color Layout) theo chuẩn MPEG-7.  
Quy trình:  
Ảnh được chuyển sang không gian màu YCrCb và chia thành lưới 8x8 khối.  
Tính giá trị trung bình của các kênh Y, Cr, Cb cho từng khối.  
Áp dụng DCT lên các giá trị trung bình này và lấy 6 hệ số đầu tiên làm đặc trưng.


Đặc trưng DCT tập trung vào phân bố màu sắc và bố cục không gian của ảnh.



## 3. Tính Độ Tương Đồng
Để so sánh và tìm kiếm các ảnh tương tự, hai phương pháp tính độ tương đồng đã được sử dụng:

### Cosine Similarity:  

Đo độ tương đồng giữa các vector đặc trưng VGG16 (512 chiều).  
Công thức:  Cosine Similarity = (A · B) / (||A|| * ||B||)


Phương pháp này hiệu quả trong việc xác định sự tương đồng về hướng giữa các vector trong không gian đa chiều, phù hợp với đặc trưng ngữ nghĩa.


### Chi-Square Distance:  

Được áp dụng để so sánh các đặc trưng DCT (6 chiều).  
Công thức:  Chi-Square Distance = Σ [(xi - yi)² / (xi + yi)]


Phương pháp này đo lường sự khác biệt giữa các phân phối đặc trưng, phù hợp với đặc trưng bố cục màu.


### Tìm Kiếm Kết Hợp:  

Một phương pháp tìm kiếm hybrid đã được triển khai, kết hợp cả Cosine Similarity (cho VGG16) và Chi-Square Distance (cho DCT) để tăng độ chính xác của kết quả tìm kiếm.



## 4. Lưu Trữ Đặc Trưng Trong Cơ Sở Dữ Liệu

### Công cụ: Sử dụng PostgreSQL với extension pgvector để lưu trữ và quản lý các vector đặc trưng.  
Cấu trúc bảng images:  
path: Đường dẫn đến file ảnh trên hệ thống.  
color_layout: Vector đặc trưng DCT (6 chiều).  
vgg_features: Vector đặc trưng VGG16 (512 chiều).


### Tối ưu hóa:  
pgvector hỗ trợ các phép toán vector như tính khoảng cách cosine hoặc L2 trực tiếp trong cơ sở dữ liệu, giúp tăng tốc độ truy vấn.  
Dữ liệu được lưu trữ dưới dạng binary để giảm dung lượng và tăng hiệu suất.



## 5. Xây Dựng API
Các API được thiết kế để hỗ trợ tương tác giữa frontend và backend:

### API Upload Ảnh:  

Chức năng:  
Nhận một ảnh, nhiều ảnh (tối đa 5) hoặc một file zip chứa nhiều ảnh từ người dùng.  
Lưu ảnh vào thư mục tĩnh, trích xuất đặc trưng (VGG16 và DCT), và lưu thông tin vào cơ sở dữ liệu.


Xử lý:  
Với file zip: Giải nén, xử lý từng ảnh, và xóa file tạm sau khi hoàn tất.  
Với nhiều ảnh: Xử lý đồng thời và trả về danh sách các file đã upload thành công.

### API Tìm Kiếm:  

Chức năng:  
Nhận một ảnh từ người dùng, trích xuất đặc trưng, và tìm kiếm các ảnh tương tự trong cơ sở dữ liệu.  
Trả về danh sách các ảnh có độ tương đồng cao nhất dựa trên cả VGG16 và DCT.


Quy trình:  
Upload ảnh tạm thời.  
Trích xuất đặc trưng.  
So sánh với dữ liệu trong cơ sở dữ liệu.  
Xóa ảnh tạm sau khi hoàn tất.


## 6. Quản Lý File và Dọn Dẹp

Quản lý file:  
Các file ảnh được lưu trong thư mục tĩnh của backend (static/images).  
File tạm (upload để tìm kiếm hoặc từ file zip) được xóa ngay sau khi xử lý để tránh chiếm dụng bộ nhớ.


Dọn dẹp:  
Hàm remove_file được gọi trong khối finally của các API để đảm bảo không để lại file rác, ngay cả khi xảy ra lỗi.



## 7. Tích Hợp và Kiểm Thử

Tích hợp:  
Các thành phần frontend, backend, và database được tích hợp thông qua Docker Compose, sử dụng các biến môi trường để kết nối linh hoạt.


Kiểm thử:  
Kiểm tra khả năng upload và tìm kiếm với các tập dữ liệu ảnh đa dạng (ảnh đơn, nhiều ảnh, file zip).  
Đánh giá hiệu suất của việc trích xuất đặc trưng và tìm kiếm trên cơ sở dữ liệu với hàng nghìn bản ghi.


# Hướng Dẫn Chạy Project

## Yêu Cầu Môi Trường

Để chạy được project này, cần đảm bảo:
- Terminal có thể chạy được file .sh (Windows đã cài Git Bash/ WSL hoặc Linux)
- Đã cài đặt **Docker** và **Docker Compose** trên máy tính.
- Docker đang ở trạng thái **đang chạy (running)**.
- Đảm bảo rằng đang ở đúng thư mục chứa các file `*.sh` trước khi thực hiện các lệnh trên.


## 1. Cấp quyền thực thi cho các file shell

Trước tiên, cần cấp quyền thực thi cho 2 file sau:

```bash
chmod +x init-data.sh
chmod +x run-project.sh
```

## 2. Khởi tạo dữ liệu

Sau khi đã cấp quyền, chạy file `init-data.sh` để khởi tạo dữ liệu cần thiết cho project:

```bash
sudo ./init-data.sh
```

## 3. Khởi động project

Sau khi dữ liệu đã được khởi tạo thành công, chạy file `run-project.sh` để khởi động project:

```bash
./run-project.sh
```
---

# Hướng Dẫn Sử Dụng Ứng Dụng

Hệ thống hỗ trợ hai chức năng chính:

## 1. Search (Tìm kiếm ảnh tương tự)

- Người dùng chọn một ảnh từ thiết bị để gửi lên server.
- Server sẽ xử lý ảnh đầu vào, trích xuất đặc trưng và so sánh với dữ liệu trong hệ thống.
- Kết quả trả về là **danh sách các ảnh có độ tương đồng cao nhất** với ảnh được gửi lên.
- Giải nén file test-set.zip trong thư mục backup, sau đó chọn một ảnh trong các folder trong test set để test khả năng tìm kiếm của hệ thống.

- Request:

```bash
curl -X POST http://localhost:5000/search \
  -F "image=@201.jpg" \
  -H "Content-Type: multipart/form-data"
```


- Response:
[
    {
        "id": 178,
        "img": "static/images/51b27b41-7430-4165-89d9-ca9df7ca0b71.jpg"
    },
    {
        "id": 186,
        "img": "static/images/3c3d9928-d7d7-4acc-9800-d80ea84de200.jpg"
    },
    {
        "id": 144,
        "img": "static/images/fd789634-b478-4efe-8da3-12155b966b1c.jpg"
    },
    {
        "id": 177,
        "img": "static/images/243c917b-e3d7-44de-9d81-10c0b7d094fe.jpg"
    },
    {
        "id": 155,
        "img": "static/images/a594460c-af32-4b74-a762-0dd89fb5430f.jpg"
    },
    {
        "id": 183,
        "img": "static/images/3c3a7cc3-7075-47d5-8ec6-f2a7c34359c6.jpg"
    },
    {
        "id": 151,
        "img": "static/images/edf3b8c8-ba80-4d84-9f5a-48a31ec8af53.jpg"
    },
    {
        "id": 200,
        "img": "static/images/83fc5dc5-d38b-4f7e-9f5e-fca6b7506e43.jpg"
    },
    {
        "id": 170,
        "img": "static/images/5735c7b1-9902-426c-b667-4a9d048e3da1.jpg"
    },
    {
        "id": 138,
        "img": "static/images/34f024c5-95a9-4746-90db-5ea8c5fec627.jpg"
    }
]


## 2. Upload (Bổ sung ảnh vào hệ thống)

Hệ thống cho phép người dùng bổ sung thêm dữ liệu ảnh mới để cải thiện độ bao phủ dữ liệu tìm kiếm.
Người dùng có thể up load thêm bộ ảnh của mình để cung cấp thêm dữ liệu cho hệ thống, sau đó có thể dùng một ảnh tương tự để tìm kiếm ngay.

Có hai chế độ upload:

- **Upload files:**  
  Cho phép chọn **tối đa 5 ảnh** từ thiết bị để thêm vào hệ thống.

- **Upload ZIP:**  
  Dành cho trường hợp người dùng muốn **cập nhật nhiều ảnh cùng lúc**. Tập tin `.zip` cần chứa ảnh ở định dạng hợp lệ (jpg).

Sau khi upload, hệ thống sẽ:
- Tự động **trích xuất đặc trưng hình dạng và màu sắc** cho từng ảnh.
- **Lưu trữ vào cơ sở dữ liệu**, sẵn sàng phục vụ cho truy vấn tìm kiếm trong tương lai.





