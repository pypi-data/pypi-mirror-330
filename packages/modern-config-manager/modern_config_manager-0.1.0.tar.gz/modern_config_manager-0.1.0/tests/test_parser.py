import os
import pytest
from config_manager import ConfigRegistry, BaseConfig
from config_manager.parser import ConfigParser
from dataclasses import dataclass

# 测试用的配置类
@ConfigRegistry.register("model", "parser_test_model")
@dataclass
class TestModelConfig(BaseConfig):
    input_size: int
    output_size: int
    hidden_size: int = 128
    dropout: float = 0.1

@ConfigRegistry.register("training", "parser_test_training")
@dataclass
class TestTrainingConfig(BaseConfig):
    batch_size: int = 32
    learning_rate: float = 0.001
    epochs: int = 100

# 命令行参数解析测试
def test_parser_basic():
    parser = ConfigParser()
    args = parser.parse_args(["train", 
                            "--model_name", "parser_test_model",
                            "--training_name", "parser_test_training", "--params", "input_size=784", "output_size=10"])
    
    assert args.model_name == "parser_test_model"
    assert args.training_name == "parser_test_training"
    assert args.model.input_size == 784
    assert args.model.output_size == 10

def test_parser_train_config_parsing(tmp_path):
    # 创建测试配置文件
    config_path = tmp_path / "test_config.yaml"
    with open(config_path, "w") as f:
        f.write("""model_name: parser_test_model
training_name: parser_test_training
model:
  input_size: 784
  output_size: 10
  hidden_size: 256
training:
  batch_size: 128
  learning_rate: 0.005
  epochs: 50""")
    
    parser = ConfigParser()
    args = parser.parse_args(["train",
                            "--model_name", "parser_test_model",
                            "--training_name", "parser_test_training",
                            "--config", str(config_path)])
    
    assert args is not None
    assert args.model_name == "parser_test_model"
    assert args.training_name == "parser_test_training"
    assert hasattr(args, "model")
    assert hasattr(args, "training")
    assert args.model.input_size == 784
    assert args.model.output_size == 10
    assert args.model.hidden_size == 256
    assert args.training.batch_size == 128
    assert args.training.learning_rate == 0.005
    assert args.training.epochs == 50

def test_parser_list_command(capsys):
    parser = ConfigParser()
    args = parser.parse_args(["list"])
    # 检查终端输出是否包含预期的内容
    captured = capsys.readouterr()
    assert "可用的配置类:" in captured.out

def test_parser_invalid_command():
    parser = ConfigParser()
    with pytest.raises(SystemExit):
        parser.parse_args(["invalid_command"])

def test_parser_missing_required_args():
    parser = ConfigParser()
    with pytest.raises(SystemExit):
        parser.parse_args(["train"])

# 新增测试用例：测试ConfigParser实例的可调用性和配置解析
def test_parser_callable():
    parser = ConfigParser()
    configs = parser.parse_args(["train", 
    "--model_name", "parser_test_model",
    "--training_name", "parser_test_training", "--params", "input_size=784", "output_size=10"])
    assert configs is not None
