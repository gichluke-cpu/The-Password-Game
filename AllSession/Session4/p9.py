import re


bad_words = ["ngu", "dmm", "vl", "cc", "lol"]


bad_word_pattern = re.compile(r"\b(" + "|".join(bad_words) + r")\b", re.IGNORECASE)


uppercase_pattern = re.compile(r"^[A-Z0-9\s!]+$")



chat_messages = [
    "/help", 
    "/teleport to base", 
    "Liên hệ 123-456-7890 để mua vàng!", 
    "Bạn có thể gửi email đến hackgame@gmail.com để nhận code", 
    "Haha, mày ngu vl", 
    "CHƠI NGAY NHẬN QUÀ KHỦNG!!!", 
    "cái thằng cc này", 
    "tin nhắn thường",
    "/command không hợp lệ!" 
]

print("--- Hệ thống Lọc và Kiểm soát Nội dung Chat ---")


for message in chat_messages:
    print(f"\n[Gốc]: \"{message}\"")

    
    command_pattern = r"^/[a-zA-Z0-9\s]+$"
    if re.match(command_pattern, message):
        print(f"   -> [Phân loại]: LỆNH GAME HỢP LỆ. Thực thi lệnh: {message[1:].strip()}")
        continue 

    
    phone_email_pattern = r"\b\d{3}-\d{3}-\d{4}\b|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    spam_contacts = re.findall(phone_email_pattern, message)
    if spam_contacts:
        print(f"   -> [Cảnh báo Spam]: Phát hiện số điện thoại/email: {', '.join(spam_contacts)}")
        
    cleaned_message = bad_word_pattern.sub("***", message)
    if cleaned_message != message:
        print(f"   -> [Kiểm duyệt]: Thay thế từ cấm. Kết quả: \"{cleaned_message}\"")
        message = cleaned_message 
    if uppercase_pattern.fullmatch(message):
        print("   -> [Cảnh báo Spam]: Tin nhắn CÓ THỂ là spam (viết HOA toàn bộ).")
        
    print(f"   -> [Kết quả cuối]: \"{message}\"")