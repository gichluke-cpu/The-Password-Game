import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('app.log'),
                              logging.StreamHandler()])

logging.debug('Đây là thông điệp DEBUG')
logging.info('Đây là thông điệp INFO')
logging.warning('Đây là thông điệp WARNING')
logging.error('Đây là thông điệp ERROR')
logging.critical('Đây là thông điệp CRITICAL')

def divide(a, b):
    try:
        result = a / b
        logging.info(f"Chia {a} cho {b} thành công, kết quả: {result}")
        return result
    except ZeroDivisionError:
        logging.error("Không thể chia cho 0")
        return None

divide(10, 2)
divide(10, 0)
