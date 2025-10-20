import sys
import subprocess
from pathlib import Path

def create_temporal_fragments_list(absolute_fragments_dir, start: int, end: int):
    ts_files = sorted(absolute_fragments_dir.glob("*.ts"),
                      key=lambda f: int(f.stem))
    list_file = absolute_fragments_dir/ ".ts_list.txt"

    with open(list_file, "w") as f:

        for ts in ts_files[start:end]:
            f.write(f"file '{ts.resolve()}'\n")
    return list_file

def ejecutar_concat_ffmpeg(list_file_path: str, output_file_path: str):
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file_path),
        "-c", "copy",
        str(output_file_path)
    ]
    subprocess.run(cmd, check=True)

def concatenar_fragmentos(fragments_dir: str, start: int, end: int):
    base_dir = Path(__file__).resolve().parent
    
    absolute_fragments_dir = base_dir / fragments_dir
    
    list_file = create_temporal_fragments_list(absolute_fragments_dir, start, end)
        
    output_file_path = (base_dir / fragments_dir).parent / "streaming.mp4"
    ejecutar_concat_ffmpeg(list_file, output_file_path)

if __name__ == "__main__":
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

