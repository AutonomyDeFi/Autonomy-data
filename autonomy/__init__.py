from .block import Block
from .tool.tool import Tool
from .cli import CLI
import os
from dotenv import load_dotenv
load_dotenv()


OPENAI_API_KEY= os.getenv("OPENAI_API_KEY", "")
INCH_API_KEY=os.getenv("ONEINCH_API_KEY", "")

PINECONE_API_KEY= os.getenv("PINECONE_API_KEY", "")
PINECONE_ENVIRONMENT= os.getenv("PINECONE_ENVIRONMENT", "")

for attr in dir(Block):
    if attr.startswith('__'):
        continue
    globals()[attr] = getattr(Block, attr)

