import math
import os
from abc import ABC, abstractmethod
from typing import Generic, Literal, TypeVar

import datasets
import optuna
from omegaconf import DictConfig
from transformers import (
    EarlyStoppingCallback,
    Trainer,
    TrainerCallback,
    TrainingArguments,
    set_seed,
)
from transformers.trainer_utils import BestRun


class BaseDataset(ABC, datasets.Dataset):
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg

    @abstractmethod
    def __len__(self):
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, idx):
        raise NotImplementedError


BoundBaseDatasetType = TypeVar("BoundBaseDatasetType", bound=datasets.Dataset)


class BaseTrainer(ABC, Generic[BoundBaseDatasetType]):
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        set_seed(cfg.seed)

    @abstractmethod
    def _model_init_factory(self):
        raise NotImplementedError

    @abstractmethod
    def _dataset_factory(
        self, dataset_cfg: DictConfig, dataset_key: Literal["train", "eval"]
    ) -> BoundBaseDatasetType:
        raise NotImplementedError

    @staticmethod
    def get_trial_suggestion(trial: optuna.Trial, param_name: str, param: DictConfig):
        suggestion_map = {
            "int": lambda: trial.suggest_int(
                param_name,
                param.low,
                param.high,
                step=param.get("step", 1),
                log=param.get("log", False),
            ),
            "float": lambda: trial.suggest_float(
                param_name,
                param.low,
                param.high,
                step=param.get("step", None),
                log=param.get("log", False),
            ),
            "categorical": lambda: trial.suggest_categorical(param_name, param.choices),
        }
        return suggestion_map[param.type]()

    def _optuna_hp_space_factory(self):
        def optuna_hp_space_factory(trial: optuna.Trial):
            params = {}

            for param in self.cfg.hyperopt.hp_space.model:
                param_name = (
                    f"model__{param.name}"  # prefixed and handle in _model_init_factory
                )
                params[param_name] = self.get_trial_suggestion(trial, param_name, param)

            for param in self.cfg.hyperopt.hp_space.training:
                param_name = f"{param.name}"  # no prefix: following default_hp_space_optuna example
                params[param_name] = self.get_trial_suggestion(trial, param_name, param)

            return params

        return optuna_hp_space_factory

    def _init_trainer(self):
        train_ds = self._dataset_factory(self.cfg.dataset, "train")
        eval_ds = self._dataset_factory(self.cfg.dataset, "eval")

        run_name = (
            self.cfg.trainer.run_name if hasattr(self.cfg.trainer, "run_name") else ""
        )

        training_args = dict(self.cfg.trainer)
        # override
        output_dir = training_args.pop("output_dir", "trainer_output")
        training_args.pop("load_best_model_at_end", None)
        training_args.pop("remove_unused_columns", None)

        weight_decay = training_args.pop("weight_decay", 0.0)  # override
        use_scaled_weight_decay = training_args.pop(
            "use_scaled_weight_decay", False
        )  # custom
        if use_scaled_weight_decay:
            weight_decay = 0.05 * math.sqrt(
                self.cfg.trainer.per_device_train_batch_size
                / (len(train_ds) * self.cfg.trainer.num_train_epochs)
            )
        early_stopping_patience = self.cfg.get("early_stopping_patience", 1)  # custom

        training_args = TrainingArguments(
            **training_args,
            output_dir=os.path.join(output_dir, run_name),
            weight_decay=weight_decay,
            load_best_model_at_end=not self.cfg.do_hyperoptim,
            remove_unused_columns=False,
        )

        callbacks: list[TrainerCallback] = [
            EarlyStoppingCallback(early_stopping_patience=early_stopping_patience)
        ]
        if self.cfg.do_hyperoptim:
            return Trainer(
                args=training_args,
                train_dataset=train_ds,
                eval_dataset=eval_ds,
                callbacks=callbacks,
                model_init=self._model_init_factory(),
            )
        return Trainer(
            model=self._model_init_factory()(),
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=eval_ds,
            callbacks=callbacks,
        )

    def train(self):
        cfg = self.cfg
        trainer = self._init_trainer()

        if not cfg.do_hyperoptim:
            trainer.train(
                resume_from_checkpoint=cfg.checkpoint_path
                if cfg.resume_from_checkpoint
                else None
            )
            final_file = os.path.join(
                cfg.trainer.output_dir, cfg.trainer.run_name, "final"
            )
            trainer.save_model(final_file)
            return

        storage = None
        if cfg.hyperopt.persistence:
            storage = optuna.storages.RDBStorage(
                url=cfg.hyperopt.storage_url,
                heartbeat_interval=cfg.hyperopt.storage_heartbeat_interval,
                engine_kwargs=cfg.hyperopt.storage_engine_kwargs,
            )

        best_trial = trainer.hyperparameter_search(
            n_trials=cfg.hyperopt.n_trials,
            gc_after_trial=True,
            direction="minimize",  # minimize loss
            backend="optuna",
            hp_space=self._optuna_hp_space_factory(),
            study_name=cfg.trainer.run_name,
            storage=storage,
            load_if_exists=cfg.hyperopt.load_if_exists,
            pruner=optuna.pruners.PatientPruner(
                optuna.pruners.MedianPruner(), patience=cfg.hyperopt.patience
            ),
        )
        self._save_best_trial_config(best_trial)

    def _save_best_trial_config(self, best_trial: BestRun | list[BestRun]):
        best_trial_file = os.path.join(
            self.cfg.trainer.output_dir, self.cfg.trainer.run_name, "best_trial.json"
        )
        with open(best_trial_file, "w") as f:
            import json

            if isinstance(best_trial, list):
                best_trial = best_trial[0]

            json.dump(best_trial._asdict(), f)
