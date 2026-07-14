from rembg import new_session
import traceback

print("Creating session...")

try:
    session = new_session()
    print("SUCCESS")
except Exception:
    traceback.print_exc()
