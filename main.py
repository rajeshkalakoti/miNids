import random
from pathlib import Path

import hydra
import pandas as pd
from omegaconf import DictConfig

from log_config import base_logger, configure_logging

logger = base_logger("data reading")


@hydra.main(version_base="1.3", config_path="config", config_name="config")
def main(cfg: DictConfig) -> None:
    configure_logging()
    ds = cfg.dataset
    rng = random.Random(ds.seed)
    df = pd.read_csv(Path(cfg.project_path) / ds.paths[ds.name],
                     skiprows=lambda i: i > 0 and rng.random() > ds.read_fraction)
    df = df.groupby(ds.target_name).sample(ds.n_per_class, random_state=ds.seed)
    X = df.drop(columns=list(ds.label_columns))
    y = (df[ds.target_name] == "Attack").astype(int)
    logger.info("X: %s, y: %s", X.shape, y.value_counts().to_dict())


if __name__ == "__main__":
    main()
