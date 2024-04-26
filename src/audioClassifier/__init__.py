import os
import logging

out_dir = 'logs'
outpath = os.path.join(out_dir,'logs.txt')
os.makedirs(out_dir, exist_ok=True)

frmt = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'

logging.basicConfig(
    level = logging.INFO,
    format = frmt,
    handlers = [logging.StreamHandler(),
               logging.FileHandler(outpath)]
)

logger = logging.getLogger()