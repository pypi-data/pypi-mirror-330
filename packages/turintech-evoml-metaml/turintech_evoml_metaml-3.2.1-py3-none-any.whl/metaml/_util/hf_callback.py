"""Defines Huggingface CallabackTrainer to produce logs during the training of
models.
"""
import logging
from typing import Dict
from transformers.trainer_callback import (
    TrainerCallback,
    TrainerControl,
    TrainingArguments,
    TrainerState,
)


logger = logging.getLogger("metaml.huggingface")


class LoggingCallback(TrainerCallback):
    """Provides logs on epoch end."""

    def on_log(
        self,
        _args: TrainingArguments,
        _state: TrainerState,
        _control: TrainerControl,
        logs: Dict[str, float],
        **kwargs,
    ):
        """Event called on log."""
        log_messages = []
        for key, value in logs.items():
            log_messages.append(f"{key}: {value}")

        log_message_str = " | ".join(log_messages)
        logger.info(log_message_str)
