import subprocess
import torch

try:
    result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True, check=True)
    nvcc_version = result.stdout.strip()
except subprocess.CalledProcessError as e:
    nvcc_version = f"Error: {e}"

print(nvcc_version)
print("PyTorch version:", torch.__version__)
print("Is PyTorch CUDA accessible:", torch.cuda.is_available())