import onnxruntime as ort
import traceback

print("ORT version:", ort.__version__)
print("Providers:", ort.get_available_providers())

try:
    # Create a session with an invalid model on purpose.
    # We only care whether the CUDA provider loads.
    ort.InferenceSession(b"", providers=["CUDAExecutionProvider"])
except Exception:
    traceback.print_exc()
