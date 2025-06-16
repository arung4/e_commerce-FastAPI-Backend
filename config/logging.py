import logging 
import sys 

# set basic configuration 
logging.basicConfig(
    level = logging.INFO, # 
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(sys.stdout) # to direct log output to the console 
    ]
)


logger = logging.getLogger("fastapi-app")

