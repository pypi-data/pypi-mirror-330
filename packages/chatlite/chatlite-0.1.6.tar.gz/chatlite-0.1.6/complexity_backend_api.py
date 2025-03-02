import os
import subprocess


def run():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    ocr_app_path = os.path.join(cur_dir, "complexity_runner.py")
    cmd = ["python", ocr_app_path]
    subprocess.run(cmd, env={**os.environ})



if __name__ == "__main__":
    run()