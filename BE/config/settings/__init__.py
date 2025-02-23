from dotenv import load_dotenv
import os


load_dotenv()

if os.getenv("env","local")=="local":
    from .local import *
else:
    from .prod import *