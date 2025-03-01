import os
import sys
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
from blackjack_api.cli import CLI

cli = CLI()
cli.loop()