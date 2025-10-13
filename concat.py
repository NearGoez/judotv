import sys
from utils import concatenar_fragmentos

if len(sys.argv) < 1:
    print('Por favor proporcione una ruta')

fragments_dir = sys.argv[1]
print(fragments_dir)
concatenar_fragmentos(fragments_dir)

