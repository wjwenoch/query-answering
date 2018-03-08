
import logging


logging_format = '[%(asctime)s] %(module)s(%(levelname)s)- %(message)s'
logging.basicConfig(format=logging_format, datefmt='%Y-%m-%d, %H:%M:%S', level=logging.INFO)


import os
temp_dir = os.path.dirname(os.path.abspath(__file__))
temp_files_dir = os.path.join(temp_dir[0: temp_dir.rindex('src')], 'files')
model_save_dir = os.path.join(temp_files_dir, 'models')
if not os.path.exists(model_save_dir):
    os.makedirs(model_save_dir)



params = {
    'learning_rate': 3e-3,
    'epoch' : 100,
    'batch_size': 64,
}