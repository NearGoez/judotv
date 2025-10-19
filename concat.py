import sys
from utils import concatenar_fragmentos

start_ts_index = 0
end_ts_index = -1

if len(sys.argv) < 2:
    print('Por favor proporcione una ruta')
    sys.exit(1)
elif len(sys.argv) >= 4 :
    start_ts_index = int(sys.argv[2])
    end_ts_index = int(sys.argv[3])
elif len(sys.argv) >= 3 :
    start_ts_index = int(sys.argv[2])

fragments_dir = sys.argv[1]
print(fragments_dir)
concatenar_fragmentos(fragments_dir, start_ts_index, end_ts_index)

