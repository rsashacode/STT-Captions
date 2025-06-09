import queue
import sounddevice as sd
import time


SAMPLERATE = 48000
DEVICE = 1
CHANNELS = 2
DTYPE = 'int16'
CHUNK_SECONDS = 5


audio_queue = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(f"[!] Status: {status}")
    audio_queue.put(indata.copy())


def main():
    print("Starting audio stream. Press Ctrl+C to stop.")

    with sd.InputStream(
        samplerate=SAMPLERATE,
        blocksize=SAMPLERATE * CHUNK_SECONDS,
        channels=CHANNELS,
        device=DEVICE,
        dtype=DTYPE,
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