import os
import shutil
from pydub import AudioSegment
from PIL import Image
from initial import initialize_data_directories

def check_resources():
    if not os.path.exists(r"data\builtin\sound.wav"):
        initialize_data_directories()

def backup_default_resources(seewo_pic_path: str):
    if not os.path.exists(r"data\backup\original_seewo_image.png"):
        os.makedirs(r"data\backup", exist_ok=True)
        print(seewo_pic_path)
        shutil.copy(seewo_pic_path, r"data\backup\original_seewo_image.png")
        
def get_bultin_assets():
    check_resources()
    with open(r"data\builtin\default_seewo_image.png", "rb") as f:
        pil_img = Image.open(f)
    with open(r"data\backup\original_seewo_image.png", "rb") as f:
        fix_pil_img = Image.open(f)
    icon_path = r"data\builtin\icon.ico"
    sound = r"data\builtin\default_seewo_sound.mp3"
    return pil_img, fix_pil_img, icon_path, sound
