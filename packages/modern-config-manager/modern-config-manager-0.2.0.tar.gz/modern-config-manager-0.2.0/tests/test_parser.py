import unittest
from pathlib import Path
import json
import yaml
from dataclasses import dataclass, field
from config_manager import ConfigRegistry, ConfigParser

@ConfigRegistry.register("model", "test_model")
@dataclass
class TestModelConfig:
    input_dim: int
    output_dim: int
    hidden_dims: list = field(default_factory=lambda: [256, 128])

@ConfigRegistry.register("training", "test_training")
@dataclass
class TestTrainingConfig:
    learning_rate: float
    batch_size: int
    epochs: int = 10
    output_dir: str = "./output"

class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.parser = ConfigParser()
        self.test_config_path = Path("test_config.yaml")
    
    def tearDown(self):
        if self.test_config_path.exists():
            self.test_config_path.unlink()
    
    def test_list_command(self):
        """测试list命令，验证是否能正确列出所有可用配置"""
        args = self.parser.parse_args(["list"])
        self.assertIsNotNone(args)
        configs = args
        self.assertIsInstance(configs, dict)
        self.assertIn("model", configs)
        self.assertIn("training", configs)
        self.assertIn("test_model", configs["model"])
        self.assertIn("test_training", configs["training"])
        
        # 打印配置列表，方便观察
        print("\n=== Available Configurations ===")
        for config_type, names in configs.items():
            print(f"{config_type}:")
            for name in names:
                print(f"  - {name}")
        print("============================\n")
    
    def test_params_command(self):
        """测试params命令，验证是否能正确显示配置参数说明"""
        print("\n=== Parameters for test_model ===")
        args = self.parser.parse_args(["params", "--type", "model", "--name", "test_model"])
        self.assertIsNone(args)  # params命令直接打印信息，返回None
        print("==============================\n")
        
        print("\n=== Testing Invalid Config Type ===")
        # 测试无效的配置类型
        args = self.parser.parse_args(["params", "--type", "invalid", "--name", "test_model"])
        self.assertIsNone(args)
        print("================================\n")
    
    def test_train_command_with_config_file(self):
        """测试使用配置文件的train命令"""
        # 创建测试配置文件
        config_data = {
            "model_name": "test_model",
            "model": {
                "input_dim": 10,
                "output_dim": 2
            },
            "training_name": "test_training",
            "training": {
                "learning_rate": 0.001,
                "batch_size": 32
            }
        }
        with open(self.test_config_path, "w") as f:
            yaml.dump(config_data, f)
        
        args = self.parser.parse_args(["train", "--config", str(self.test_config_path)])
        self.assertIsNotNone(args)
        self.assertTrue(hasattr(args, "model"))
        self.assertTrue(hasattr(args, "training"))
        
        # 验证配置内容
        self.assertEqual(args.model.input_dim, 10)
        self.assertEqual(args.model.output_dim, 2)
        self.assertEqual(args.training.learning_rate, 0.001)
        self.assertEqual(args.training.batch_size, 32)
    
    def test_train_command_with_cli_params(self):
        """测试使用命令行参数的train命令"""
        args = self.parser.parse_args([
            "train",
            "--model_name", "test_model",
            "--training_name", "test_training",
            "--params",
            "input_dim=10",
            "output_dim=2",
            "learning_rate=0.001",
            "batch_size=32"
        ])
        
        self.assertIsNotNone(args)
        self.assertTrue(hasattr(args, "model"))
        self.assertTrue(hasattr(args, "training"))
        
        # 验证配置内容
        self.assertEqual(args.model.input_dim, 10)
        self.assertEqual(args.model.output_dim, 2)
        self.assertEqual(args.training.learning_rate, 0.001)
        self.assertEqual(args.training.batch_size, 32)
    
    def test_train_command_with_output_dir(self):
        """测试train命令的输出目录参数"""
        args = self.parser.parse_args([
            "train",
            "--model_name", "test_model",
            "--training_name", "test_training",
            "--output_dir", "./custom_output",
            "--params",
            "input_dim=10",
            "output_dim=2",
            "learning_rate=0.001",
            "batch_size=32"
        ])
        
        self.assertIsNotNone(args)
        self.assertEqual(args.training.output_dir, "./custom_output")
    
    def test_invalid_config_file(self):
        """测试无效的配置文件"""
        # 创建无效的配置文件
        with open(self.test_config_path, "w") as f:
            f.write("invalid: yaml: content:")
        
        with self.assertRaises(yaml.YAMLError):
            self.parser.parse_args(["train", "--config", str(self.test_config_path)])
    
    def test_invalid_params_format(self):
        """测试无效的参数格式"""
        args = self.parser.parse_args([
            "train",
            "--model_name", "test_model",
            "--training_name", "test_training",
            "--params",
            "invalid_param"  # 缺少=号
        ])
        
        self.assertIsNone(args)

if __name__ == "__main__":
    unittest.main()