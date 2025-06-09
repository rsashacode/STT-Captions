import time

import queue
import sounddevice as sd

from config import settings


audio_queue = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(f"[!] Status: {status}")
    audio_queue.put(indata.copy())


def main():
    print("Starting audio stream. Press Ctrl+C to stop.")

    for device_idx in range(settings.input_n_devices):
        with sd.InputStream(
            samplerate=settings.input_samplerate[device_idx],
            blocksize=int(settings.input_samplerate[device_idx] * settings.chunk_size_seconds),
            channels=settings.input_n_channels[device_idx],
            device=settings.input_sd_device_ids[device_idx],
            dtype=settings.dtype,
            callback=callback
        ):
            try:
                while True:
                    chunk = audio_queue.get()
                    print(f"Received audio chunk with shape: {chunk.shape}, dtype: {chunk.dtype}, time: {time.time()}")

            except KeyboardInterrupt:
                print("\nStopped by user.")


if __name__ == "__main__":
    main()