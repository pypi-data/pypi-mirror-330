import base64
import sys
import zlib
import random
from itertools import cycle

def ofuscar(archivo_entrada, archivo_salida, veces):
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        codigo = f.read()

    codigo_comprimido = zlib.compress(codigo.encode('utf-8'))
    codigo_b64 = base64.b64encode(codigo_comprimido).decode('utf-8')
    
    key = bytes([random.randint(1, 255) for _ in range(8)])
    codigo_xor = bytes([b ^ k for b, k in zip(codigo_b64.encode(), cycle(key))])
    
    codigo_hex = codigo_xor.hex()
    
    skidder_lines = "\n".join([f"# _skidder__" * veces for _ in range(3)])
    
    plantilla = f"""
{skidder_lines}

from itertools import cycle
import base64
import zlib

_DATA = "{codigo_hex}"
_KEY = bytes([{','.join(map(str, key))}])

def _decode():
    _xor = bytes([b ^ k for b, k in zip(bytes.fromhex(_DATA), cycle(_KEY))])
    _b64 = _xor.decode('utf-8')
    _compressed = base64.b64decode(_b64)
    return zlib.decompress(_compressed).decode('utf-8')

exec(_decode())
"""

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(plantilla)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python PyCrypterFUD.py <input_file> <output_file> <times>")
        sys.exit(1)
    ofuscar(sys.argv[1], sys.argv[2], int(sys.argv[3]))