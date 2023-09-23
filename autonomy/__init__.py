from .block import Block
from .tool.tool import Tool
from .cli import CLI

for attr in dir(Block):
    if attr.startswith('__'):
        continue
    globals()[attr] = getattr(Block, attr)