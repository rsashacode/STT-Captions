import asyncio
import sounddevice as sd


class AudioProcessor:
    def __init__(
            self,
            device_id: int,
            device_name: str,
            samplerate: int,
            n_channels: int,
            blocksize: int,
            dtype: str,
    ):
        self.device_id = device_id
        self.device_name = device_name
        self.samplerate = samplerate
        self.n_channels = n_channels
        self.blocksize = blocksize
        self.dtype = dtype

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
            print(f"Mic {self.device_name} id={self.device_id} Got audio chunk: {len(chunk)} bytes")

            # Placeholder for processing
            await asyncio.sleep(0)

    async def run(self):
        print(f"Mic {self.device_name} id={self.device_id} Starting")
        self.loop = asyncio.get_running_loop()
        with sd.InputStream(
                device=self.device_id,
                samplerate=self.samplerate,
                blocksize=self.blocksize,
                channels=self.n_channels,
                dtype=self.dtype,
                callback=self._callback
        ):
            await self.consume()
