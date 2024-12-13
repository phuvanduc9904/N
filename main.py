import os
import subprocess

def create_user_and_set_password():
    try:
        # Kiểm tra xem người dùng 'duc' đã tồn tại chưa
        user_exists = subprocess.getoutput("id -u duc 2>/dev/null")
        
        if not user_exists:
            print("Đang tạo người dùng 'duc'...")
            os.system("sudo useradd -m -s /bin/bash duc")  # Tạo người dùng 'duc'
            print("Đã tạo người dùng 'duc'.")
        
        # Đặt mật khẩu cho người dùng 'duc'
        os.system("echo 'duc:duc' | sudo chpasswd")  # Đặt mật khẩu là 'duc'
        print("Đã đặt mật khẩu 'duc' cho người dùng 'duc'.")
        
    except Exception as e:
        print(f"Lỗi khi tạo người dùng hoặc đặt mật khẩu: {str(e)}")

def setup_ssh():
    try:
        print("Đang kiểm tra và cài đặt SSH server...")
        # Cài đặt SSH server nếu chưa có
        os.system("sudo apt update && sudo apt install -y openssh-server")
        
        # Khởi động SSH server
        os.system("sudo service ssh start")
        print("SSH server đã được cài đặt và khởi động.")
        
        # Lấy địa chỉ IP công khai của Gitpod
        public_ip = subprocess.getoutput("curl -s ifconfig.me")
        print(f"Địa chỉ IP công khai: {public_ip}")
        
        # Thêm thông báo "Kết nối thành công" vào tệp trong thư mục người dùng
        user_motd_file = os.path.expanduser("~/ssh_motd.txt")
        motd_message = f"Chào mừng! Bạn đã kết nối SSH thành công tới Gitpod.\nKết Nối Thành Công!"
        with open(user_motd_file, "w") as motd_file:
            motd_file.write(motd_message)
        print(f"Thông báo đã được lưu vào: {user_motd_file}")

        # In cấu hình SSH để truy cập
        print("\nCấu hình SSH để truy cập:")
        print(f"Sử dụng lệnh dưới đây để kết nối qua SSH:")
        print(f"ssh duc@{public_ip}")

    except Exception as e:
        print(f"Lỗi trong quá trình thiết lập SSH: {str(e)}")


def setup_ssh_key():
    try:
        # Tạo SSH key (nếu chưa có)
        ssh_dir = os.path.expanduser("~/.ssh")
        if not os.path.exists(ssh_dir):
            os.makedirs(ssh_dir)
        
        private_key_path = os.path.join(ssh_dir, "id_rsa")
        public_key_path = f"{private_key_path}.pub"
        
        if not os.path.exists(private_key_path):
            os.system(f"ssh-keygen -t rsa -b 2048 -f {private_key_path} -N ''")
            print("Đã tạo SSH key mới.")
        
        # Đọc public key từ file và lưu vào biến pub_key
        with open(public_key_path, "r") as pub_key_file:
            pub_key = pub_key_file.read()
        
        # Thêm public key vào authorized_keys
        authorized_keys_path = os.path.join(ssh_dir, "authorized_keys")
        if os.path.exists(authorized_keys_path):
            with open(authorized_keys_path, "r") as auth_file:
                existing_keys = auth_file.read()
        else:
            existing_keys = ""

        with open(authorized_keys_path, "a") as auth_file:
            if pub_key not in existing_keys:
                auth_file.write(pub_key + "\n")
                print("Đã thêm public key vào authorized_keys.")
        
        # Cấp quyền chính xác cho file SSH
        os.system(f"chmod 600 {authorized_keys_path}")
        os.system(f"chmod 700 {ssh_dir}")
        print("Đã cấu hình SSH key hoàn tất.")

    except Exception as e:
        print(f"Lỗi trong quá trình tạo SSH key: {str(e)}")


if __name__ == "__main__":
    create_user_and_set_password()  # Tạo người dùng 'duc' và đặt mật khẩu
    setup_ssh_key()  # Tạo SSH key
    setup_ssh()  # Cài đặt SSH server và thông báo thành công
    print("Thiết lập SSH thành công.")