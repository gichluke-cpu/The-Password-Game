import logging
import pdb

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_game():
    logging.info("Game started")

def end_game():
    logging.info("Game ended")

def attack(attacker, defender, damage):
    # Trừ máu
    defender["health"] -= damage
    if defender["health"] <= 0:
        defender["health"] = 0
        logging.info(f"{attacker['name']} attacked {defender['name']} for {damage} damage.")
        logging.info(f"{defender['name']} has been defeated!")
    else:
        logging.info(f"{attacker['name']} attacked {defender['name']} for {damage} damage.")
        logging.info(f"{defender['name']} has {defender['health']} health left.")

# Khởi tạo nhân vật
player1 = {"name": "Arthur", "health": 100}
player2 = {"name": "Zata", "health": 100}

# Debug
pdb.set_trace()

# Chạy mô phỏng trận đấu
start_game()
attack(player1, player2, 30)   # Arthur đánh Zata
attack(player2, player1, 50)   # Zata đánh Arthur
end_game()
