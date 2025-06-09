import time
import asyncio

import sounddevice as sd

from config import settings


class AudioProcessor:
    def __init__(self):
        self.loop: asyncio.AbstractEventLoop | None = None
        self.queue: asyncio.Queue[bytes] = asyncio.Queue(maxsize=100)

    def _callback(self, indata, frames, time, status):
        if status:
            print(f"[!] Status: {status}")
        data = indata.copy().tobytes()
        self.loop.call_soon_threadsafe(self.queue.put_nowait, data)

    async def consume(self):
        while True:
            chunk = await self.queue.get()
            print(f"Got audio chunk: {len(chunk)} bytes")

            # Placeholder for processing
            await asyncio.sleep(0)

    async def run(self):
        print("Starting audio recording. Press Ctrl+C to stop.")
        self.loop = asyncio.get_running_loop()
        with sd.InputStream(
                samplerate=settings.input_samplerate[0],
                blocksize=int(settings.input_samplerate[0] * settings.chunk_size_seconds),
                channels=settings.input_n_channels[0],
                device=settings.input_sd_device_ids[0],
                dtype=settings.dtype,
                callback=self._callback
        ):
            await self.consume()


if __name__ == "__main__":
    try:
        asyncio.run(AudioProcessor().run())
    except KeyboardInterrupt:
        print("\nStopped.")