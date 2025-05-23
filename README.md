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


