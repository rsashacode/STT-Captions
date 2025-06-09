import yaml
import os
import shutil

from pydantic import BaseModel


CONFIG_PATH = "config.yaml"
SAMPLE_PATH = "config.sample.yaml"


class AppConfig(BaseModel):
    # Core
    debug: bool = True
    app_name: str ="Captions Generator"
    version: str = "0.0.1"

    # Audio Input
    input_n_devices: int = 2
    input_samplerate: list = [48000, 48000]
    input_n_channels: list = [2, 2]
    input_sd_device_ids: list = [1, 1]
    input_device_names: list = ["Room1", "Room2"]

    # Processing
    chunk_size_seconds: float = 5
    dtype: str = 'int16'


    def model_post_init(self, __context) -> None:
        if not all([
            len(self.input_samplerate) == self.input_n_devices,
            len(self.input_n_channels) == self.input_n_devices,
            len(self.input_sd_device_ids) == self.input_n_devices,
            len(self.input_device_names) == self.input_n_devices,
        ]):
            raise ValueError(
                f"Mismatch between input_n_devices ({self.input_n_devices}) and list lengths: "
                f"samplerate ({len(self.input_samplerate)}), channels ({len(self.input_n_channels)}), "
                f"device_ids ({len(self.input_sd_device_ids)})."
            )


    @classmethod
    def from_yaml(cls, path: str = CONFIG_PATH) -> "AppConfig":
        if not os.path.exists(path):
            if os.path.exists(SAMPLE_PATH):
                shutil.copyfile(SAMPLE_PATH, path)
                print(f"[INFO] Created '{path}' from sample. Please edit it with your settings.")
            else:
                raise FileNotFoundError("No config.yaml or config.sample.yaml found.")

        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)


settings = AppConfig.from_yaml()
