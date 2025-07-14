# moku_utils.py

from moku import Moku
from moku.exceptions import MokuException
import os
os.environ["MOKU_DATA_PATH"] = r"C:\Users\venv\Lib\site-packages\moku\data"
def safe_connect(ip):
    """
    Establish a clean connection to Moku:Go using required arguments.
    Handles busy state and timeouts gracefully.
    """
    try:
        moku = Moku(
            ip,
            force_connect=True,
            ignore_busy=True,
            persist_state=False,
            connect_timeout=10,
            read_timeout=10
        )
        return moku
    except MokuException as e:
        print(f"[Warning] Moku connection error: {e}")
        return None