import os
from hydra import initialize, compose
from omegaconf import OmegaConf, DictConfig
kcn_params = "config.yaml"
config_path="configs/"
overrides = []

if os.environ.get('KCN_PARAMS') and os.environ.get('KCN_PARAMS') != '':
    full_path = os.getenv('KCN_PARAMS')
    full_path = "../" + full_path
    config_path = os.path.dirname(full_path)
    kcn_params = os.path.basename(full_path)  # Extract the filename
    
if os.environ.get('KCN_OVERRIDES') and os.environ.get('KCN_OVERRIDES') != '':
    overrides_env = os.getenv("KCN_OVERRIDES")
    overrides = overrides_env.split('|') if overrides_env else []

with initialize(version_base=None, config_path=config_path):
    args = compose(config_name=kcn_params)