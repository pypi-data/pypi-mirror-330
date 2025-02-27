import cv2

import livesync as ls
from livesync import layers

if __name__ == "__main__":
    # Example: Webcam Recording with Watermark Pipeline
    #
    # ●  (f2): Records processed frames to MP4 file
    # │
    # ●  (f1): Adds a watermark to the frame
    # │
    # ◇  (x): Captures frames from webcam (device 0)
    #

    x = ls.WebcamInput(device_id=0, fps=30, buffer_type="rgb24")

    watermark_img = cv2.imread("./examples/assets/sample-watermark.png", cv2.IMREAD_UNCHANGED)
    logo_image = cv2.imencode(".png", watermark_img)[1].tobytes()

    f1 = layers.WatermarkLayer(watermark_bytes=logo_image, position="top-left", watermark_scale=0.15, opacity=0.6)
    f2 = layers.VideoQualityControlLayer(quality="240p")
    f3 = layers.VideoRecorderLayer(filename="./examples/output.mp4")

    y = f3(f2(f1(x)))

    sync = ls.Sync(inputs=[x], outputs=[y])
    with sync.compile() as runner:
        runner.run(callback=ls.LoggingCallback())
