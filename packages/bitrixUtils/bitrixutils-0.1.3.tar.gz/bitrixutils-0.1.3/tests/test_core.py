import sys
import os
import json

# Adiciona o diretório do bitrix.py ao sys.path (caso precise criar um novo arquivo para testes)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../bitrixUtils')))
import core

