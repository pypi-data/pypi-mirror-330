from typing import Literal

import cv2
import numpy as np
from numpy.typing import NDArray

from ..._utils.logs import logger
from ...frames.video_frame import VideoFrame
from ..core.callable_layer import CallableLayer


class WatermarkLayer(CallableLayer[VideoFrame, VideoFrame | None]):
    """
    A layer that overlays a watermark onto a video frame.

    The watermark image is decoded from bytes and then resized relative to the
    frame's width. The watermark can be positioned in one of several locations.
    A global opacity can be applied to control the transparency.

    Parameters
    ----------
    watermark_bytes : bytes
        The encoded watermark image bytes.
    position : {'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'}, optional
        The position of the watermark on the frame, by default "bottom-right".
    watermark_scale : float, optional
        The scale factor relative to the frame's width, by default 0.1.
    opacity : float, optional
        The global opacity for the watermark (0.0 transparent, 1.0 opaque), by default 1.0.
    name : str or None, optional
        An optional name for the layer.
    """

    def __init__(
        self,
        watermark_bytes: bytes,
        position: Literal["top-left", "top-right", "bottom-left", "bottom-right", "center"] = "bottom-right",
        watermark_scale: float = 0.1,
        opacity: float = 1.0,
        margin_ratio: float = 0.02,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        self.position = position
        self.watermark_scale = watermark_scale
        self.opacity = opacity
        self.margin_ratio = margin_ratio

        # Decode the watermark from bytes. The watermark may contain an alpha channel.
        nparr = np.frombuffer(watermark_bytes, np.uint8)
        try:
            self.watermark_image: NDArray[np.uint8] = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)  # type: ignore
        except Exception as e:
            logger.error(f"Failed to decode watermark image from the provided bytes: {e}")
            raise ValueError("Failed to decode watermark image from the provided bytes.") from e

    async def call(self, x: VideoFrame) -> VideoFrame | None:
        """
        Apply the watermark on the provided video frame.

        Parameters
        ----------
        x : VideoFrame
            The input video frame.

        Returns
        -------
        VideoFrame or None
            The watermarked frame, or None if an error occurs.
        """
        try:
            frame_buffer = x.data
            frame_h, frame_w = frame_buffer.shape[:2]

            # Determine the new size of the watermark relative to the frame's width.
            wm_h, wm_w = self.watermark_image.shape[:2]
            new_w = int(frame_w * self.watermark_scale)
            scale_factor = new_w / wm_w
            new_h = int(wm_h * scale_factor)
            resized_watermark = cv2.resize(self.watermark_image, (new_w, new_h), interpolation=cv2.INTER_AREA)

            # Compute margin in a ratio-based manner (e.g., 2% of frame width/height).
            # This way, if frame resolution changes, the watermark stays proportionally placed.
            margin_x = int(frame_w * self.margin_ratio)
            margin_y = int(frame_h * self.margin_ratio)

            # Calculate the position based on the desired placement.
            if self.position == "top-left":
                x_pos = margin_x
                y_pos = margin_y
            elif self.position == "top-right":
                x_pos = frame_w - new_w - margin_x
                y_pos = margin_y
            elif self.position == "bottom-left":
                x_pos = margin_x
                y_pos = frame_h - new_h - margin_y
            elif self.position == "center":
                x_pos = (frame_w - new_w) // 2
                y_pos = (frame_h - new_h) // 2
            else:  # Default to bottom-right.
                x_pos = frame_w - new_w - margin_x
                y_pos = frame_h - new_h - margin_y

            # Overlay the watermark onto the frame.
            watermarked_frame: NDArray[np.uint8] = self._overlay_image(
                frame_buffer,  # type: ignore
                resized_watermark,  # type: ignore
                x_pos,
                y_pos,
                self.opacity,
            )

            # Return the modified video frame.
            video_frame = VideoFrame(
                data=watermarked_frame,
                time_base=x.time_base,
                pts=x.pts,
                timestamp_ms=x.timestamp_ms,
                width=x.width,
                height=x.height,
                buffer_type=x.buffer_type,
            )
            return video_frame
        except Exception as e:
            logger.error(f"Error during watermark insertion: {e}")
            return None

    @staticmethod
    def _overlay_image(
        background: NDArray[np.uint8], overlay: NDArray[np.uint8], x: int, y: int, opacity: float
    ) -> NDArray[np.uint8]:
        """
        Overlay the watermark onto the background image.

        Parameters
        ----------
        background : NDArray[np.uint8]
            The background image.
        overlay : NDArray[np.uint8]
            The watermark image.
        x : int
            The x-coordinate for placing the watermark.
        y : int
            The y-coordinate for placing the watermark.
        opacity : float
            Global opacity for blending the watermark.

        Returns
        -------
        NDArray[np.uint8]
            The blended image.
        """
        bg_h, bg_w = background.shape[:2]
        ol_h, ol_w = overlay.shape[:2]

        if x + ol_w > bg_w or y + ol_h > bg_h:
            ol_w = min(ol_w, bg_w - x)
            ol_h = min(ol_h, bg_h - y)
            overlay = overlay[0:ol_h, 0:ol_w]

        roi = background[y : y + ol_h, x : x + ol_w]

        # If the overlay has an alpha channel (RGBA)
        if overlay.shape[2] == 4:
            overlay_rgb = overlay[..., :3]
            alpha_mask = (overlay[..., 3:] / 255.0) * opacity

            if roi.shape[2] == overlay_rgb.shape[2]:
                blended = (alpha_mask * overlay_rgb + (1 - alpha_mask) * roi).astype(background.dtype)
                background[y : y + ol_h, x : x + ol_w] = blended
            elif roi.shape[2] == overlay_rgb.shape[2] + 1:
                roi_rgb = roi[..., :3]
                blended = (alpha_mask * overlay_rgb + (1 - alpha_mask) * roi_rgb).astype(background.dtype)
                background[y : y + ol_h, x : x + ol_w, :3] = blended
        else:
            # Handle overlay without its own alpha channel (RGB)
            if roi.shape[2] == overlay.shape[2]:
                blended = (opacity * overlay + (1 - opacity) * roi).astype(background.dtype)
                background[y : y + ol_h, x : x + ol_w] = blended
            elif roi.shape[2] == overlay.shape[2] + 1:
                roi_rgb = roi[..., :3]
                blended = (opacity * overlay + (1 - opacity) * roi_rgb).astype(background.dtype)
                background[y : y + ol_h, x : x + ol_w, :3] = blended

        return background
