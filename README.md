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
---

# Hướng Dẫn Sử Dụng Ứng Dụng

Hệ thống hỗ trợ hai chức năng chính:

## 1. Search (Tìm kiếm ảnh tương tự)

- Người dùng chọn một ảnh từ thiết bị để gửi lên server.
- Server sẽ xử lý ảnh đầu vào, trích xuất đặc trưng và so sánh với dữ liệu trong hệ thống.
- Kết quả trả về là **danh sách các ảnh có độ tương đồng cao nhất** với ảnh được gửi lên.

## 2. Upload (Bổ sung ảnh vào hệ thống)

Hệ thống cho phép người dùng bổ sung thêm dữ liệu ảnh mới để cải thiện độ bao phủ dữ liệu tìm kiếm.

Có hai chế độ upload:

- **Upload files:**  
  Cho phép chọn **tối đa 5 ảnh** từ thiết bị để thêm vào hệ thống.

- **Upload ZIP:**  
  Dành cho trường hợp người dùng muốn **cập nhật nhiều ảnh cùng lúc**. Tập tin `.zip` cần chứa ảnh ở định dạng hợp lệ (jpg).

Sau khi upload, hệ thống sẽ:
- Tự động **trích xuất đặc trưng hình dạng và màu sắc** cho từng ảnh.
- **Lưu trữ vào cơ sở dữ liệu**, sẵn sàng phục vụ cho truy vấn tìm kiếm trong tương lai.



