# Web social media - Helix

## Triển khai

1. Clone project
2. Cài đặt các thư viện cần thiết: pip install -r requirements.txt
3. Mở file config.py và cấu hình kết nối của bạn
4. Tạo CSDL:
    - Cách 1: Mở file db.sql trong app và tạo bảng trong database
    - Cách 2: Chạy migrations để khởi tạo cơ sở dữ liệu
5. Chạy ứng dụng: flask run

*Chú ý: request - gửi thông tin dưới dạng multipart/form-data nếu có file ảnh.