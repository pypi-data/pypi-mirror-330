import os
from hydra import initialize, compose
from omegaconf import DictConfig

class ConfigLoader:
    def __init__(self):
        self.kcn_params = "config.yaml"
        self.config_path = "configs/"
        self.overrides = []

    def _load_env_variables(self):
        """Load environment variables for config parameters and overrides."""
        if os.environ.get("KCN_PARAMS"):
            full_path = os.getenv("KCN_PARAMS")
            self.kcn_params = os.path.basename(full_path)  # Extract the filename

        if os.environ.get("KCN_OVERRIDES"):
            overrides_env = os.getenv("KCN_OVERRIDES")
            self.overrides = overrides_env.split("|") if overrides_env else []

    def get_args(self) -> DictConfig:
        """Load and return the Hydra configuration."""
        self._load_env_variables()
        with initialize(version_base=None, config_path=self.config_path):
            args = compose(config_name=self.kcn_params, overrides=self.overrides)
        return args
