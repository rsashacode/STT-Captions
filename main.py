import asyncio
from config import settings
from audio_processor import AudioProcessor


async def main():
    # Build one AudioProcessor per configured device
    processors = []
    for device_idx in range(settings.input_n_devices):
        proc = AudioProcessor(
            device_id=settings.input_sd_device_ids[device_idx],
            device_name=settings.input_device_names[device_idx],
            samplerate=settings.input_samplerate[device_idx],
            n_channels=settings.input_n_channels[device_idx],
            blocksize=int(settings.input_samplerate[device_idx] * settings.chunk_size_seconds),
            dtype=settings.dtype
        )
        processors.append(proc)

    # Fire them all off
    tasks = [asyncio.create_task(p.run()) for p in processors]

    # Wait until cancelled (Ctrl+C)
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAll recordings stopped.")
