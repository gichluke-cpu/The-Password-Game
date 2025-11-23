import sys

try:
    username = input("Nhập tên người dùng (username): ").strip()
    password = input("Nhập mật khẩu (password): ").strip()

    if not username or not password:
        raise ValueError("Tên người dùng và mật khẩu không được để trống!")

    if len(password) < 6:
        raise Exception("Mật khẩu quá ngắn! Mật khẩu phải có ít nhất 6 ký tự.")

    print("\n✅ Đăng nhập thành công!")
    print(f"Chào mừng, {username}!")

except ValueError as e:
    print("\n❌ LỖI ĐẦU VÀO (ValueError):")
    print(f"Chi tiết: {e}")
    
except Exception as e:
    print("\n❌ LỖI BẢO MẬT (Exception):")
    print(f"Chi tiết: {e}")

finally:
    print("\n--- Kết thúc quá trình đăng nhập ---")
