import logging
import os
import shutil
from pathlib import Path
from digiprospector_utils.dp_logging import get_logger
import pytest

#Improved test to check multiple calls to get_logger with the same name
def test_get_logger_multiple_calls():
    logger1 = get_logger("test_multiple")
    logger2 = get_logger("test_multiple")
    assert logger1 is logger2 # Check that both calls return the same logger instance
    assert len(logger1.handlers) == 2


def test_get_logger_default():
    logger = get_logger("test_default")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_default"
    assert len(logger.handlers) == 2
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    assert isinstance(logger.handlers[1], logging.handlers.RotatingFileHandler)

    # Clean up the log file - improved to handle potential exceptions
    log_file_path = Path(logger.handlers[1].baseFilename)
    try:
        log_file_path.unlink()
    except FileNotFoundError:
        pass


def test_get_logger_custom_log_dir(tmp_path):
    log_dir = tmp_path / "logs"
    logger = get_logger("test_custom_dir", log_dir=log_dir)
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_custom_dir"
    assert len(logger.handlers) == 2
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    assert isinstance(logger.handlers[1], logging.handlers.RotatingFileHandler)
    assert Path(logger.handlers[1].baseFilename).parent == log_dir

    # Clean up the log file - improved to handle potential exceptions
    log_file_path = Path(logger.handlers[1].baseFilename)
    try:
        log_file_path.unlink()
    except FileNotFoundError:
        pass


def test_get_logger_custom_levels(tmp_path):
    log_dir = tmp_path / "logs"
    logger = get_logger("test_custom_levels", s_lvl=logging.WARNING, f_lvl=logging.ERROR, log_dir=log_dir)
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_custom_levels"
    assert len(logger.handlers) == 2
    assert logger.handlers[0].level == logging.WARNING
    assert logger.handlers[1].level == logging.ERROR

    # Clean up the log file - improved to handle potential exceptions
    log_file_path = Path(logger.handlers[1].baseFilename)
    try:
        log_file_path.unlink()
    except FileNotFoundError:
        pass


def test_get_logger_invalid_log_dir(tmp_path):
    #Test with invalid log directory
    with pytest.raises(TypeError):
        get_logger("test_invalid_log_dir", log_dir=123)


def test_get_logger_nonexistent_log_dir(tmp_path):
    #Test with a non-existent log directory
    log_dir = tmp_path / "logs" / "subdir"
    logger = get_logger("test_nonexistent_log_dir", log_dir=log_dir)
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_nonexistent_log_dir"
    assert len(logger.handlers) == 2
    assert logger.handlers[0].level == logging.INFO
    assert logger.handlers[1].level == logging.DEBUG
    assert Path(logger.handlers[1].baseFilename).parent == log_dir
    
    # Clean up the log file - improved to handle potential exceptions
    log_file_path = Path(logger.handlers[1].baseFilename)
    try:
        log_file_path.unlink()
    except FileNotFoundError:
        pass

