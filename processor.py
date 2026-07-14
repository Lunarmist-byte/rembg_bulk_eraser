import os
import threading
from PIL import Image
from rembg import remove, new_session


class BackgroundRemover:
    def __init__(self, input_folder, output_folder,
                 progress_callback,
                 completion_callback,
                 error_callback):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
        self.error_callback = error_callback
        self.is_cancelled = False

        # Load the ONNX model only once
        self.session = new_session()

    def start(self):
        self.thread = threading.Thread(target=self.process_images)
        self.thread.daemon = True
        self.thread.start()

    def cancel(self):
        self.is_cancelled = True

    def process_images(self):
        try:
            valid_exts = (".png", ".jpg", ".jpeg", ".webp")
            images = [f for f in os.listdir(self.input_folder) if f.lower().endswith(valid_exts)]
            
            if not images:
                self.completion_callback(0)
                return

            os.makedirs(self.output_folder, exist_ok=True)

            for i, filename in enumerate(images):
                if self.is_cancelled:
                    break

                in_path = os.path.join(self.input_folder, filename)
                out_path = os.path.join(self.output_folder, f"{os.path.splitext(filename)[0]}_nobg.png")

                with Image.open(in_path) as img:
                    out = remove(
                        img, 
                        session=self.session,
                        post_process_mask=True,
                        alpha_matting=True,
                        alpha_matting_foreground_threshold=240,
                        alpha_matting_background_threshold=10,
                        alpha_matting_erode_size=10
                    )
                    out.save(out_path)

                self.progress_callback(i + 1, len(images), (i + 1) / len(images))

            if not self.is_cancelled:
                self.completion_callback(len(images))

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.error_callback(str(e))
