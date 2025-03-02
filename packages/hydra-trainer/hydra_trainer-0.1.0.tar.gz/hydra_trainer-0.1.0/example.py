from typing import Literal

import hydra
import optuna
from omegaconf import DictConfig

from hydra_trainer import BaseDataset, BaseTrainer


class ExampleDataset(BaseDataset):
    def __init__(self, cfg: DictConfig, dataset_key: Literal["train", "eval"]):
        super().__init__(cfg)
        self.dataset_key = dataset_key
        # TODO: implement dataset loading and preprocessing
        raise NotImplementedError

    def __len__(self):
        # TODO: implement this method
        raise NotImplementedError

    def __getitem__(self, idx):
        # TODO: implement this method
        raise NotImplementedError


class ExampleTrainer(BaseTrainer[ExampleDataset]):
    def _model_init_factory(self):
        model_cfg = self.cfg.model

        def model_init_closure(trial: optuna.Trial | None = None):
            if trial is not None and hasattr(self.cfg.hyperopt.hp_space, "model"):
                # Override config with trial parameters for model
                for param in self.cfg.hyperopt.hp_space.model:
                    param_name = param.name
                    trial_name = f"model__{param_name}"
                    model_cfg[param_name] = trial.params[trial_name]

            # TODO: implement model initialization
            raise NotImplementedError

        return model_init_closure

    def _dataset_factory(
        self, dataset_cfg: DictConfig, dataset_key: Literal["train", "eval"]
    ) -> ExampleDataset:
        # TODO: implement this method
        raise NotImplementedError


@hydra.main(config_path="../conf", config_name="base", version_base=None)
def main(cfg: DictConfig):
    trainer = ExampleTrainer(cfg)
    trainer.train()


if __name__ == "__main__":
    main()
