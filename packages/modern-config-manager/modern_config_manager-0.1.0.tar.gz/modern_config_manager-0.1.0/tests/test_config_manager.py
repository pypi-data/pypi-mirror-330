import os
import json
import yaml
import pytest
from dataclasses import dataclass, field
from typing import List, Dict
from config_manager import ConfigRegistry, BaseConfig, CompositeConfig

# 测试用的配置类
@ConfigRegistry.register("test", "basic")
@dataclass
class TestConfig(BaseConfig):
    name: str
    value: int
    flag: bool = True
    items: List[int] = field(default_factory=lambda: [1, 2, 3])
    params: Dict[str, str] = field(default_factory=lambda: {"key": "value"})

@ConfigRegistry.register("test", "derived")
@dataclass
class DerivedTestConfig(TestConfig):
    extra_field: str = "test"

# 基本功能测试
def test_config_registration():
    # 测试配置注册
    config_cls = ConfigRegistry.get_config("test", "basic")
    assert config_cls == TestConfig

    # 测试配置实例化
    config = config_cls(name="test_instance", value=42)
    assert config.name == "test_instance"
    assert config.value == 42
    assert config.flag == True

def test_config_type_conversion():
    # 测试字符串到布尔值的转换
    config = TestConfig(name="test", value=1, flag="true")
    assert isinstance(config.flag, bool)
    assert config.flag == True

    # 测试字符串到列表的转换
    config = TestConfig(name="test", value=1, items="1,2,3")
    assert isinstance(config.items, list)
    assert config.items == [1, 2, 3]

    # 测试字符串到字典的转换
    config = TestConfig(name="test", value=1, params='{"key": "value"}')
    assert isinstance(config.params, dict)
    assert config.params == {"key": "value"}

def test_config_inheritance():
    # 测试配置继承
    derived_config = DerivedTestConfig(name="derived", value=100)
    assert derived_config.name == "derived"
    assert derived_config.value == 100
    assert derived_config.extra_field == "test"

def test_config_save_load(tmp_path):
    # 测试配置保存和加载
    config = TestConfig(name="save_test", value=42)
    
    # 测试YAML格式
    yaml_path = tmp_path / "config.yaml"
    config.save(str(yaml_path))
    loaded_config = TestConfig.load(str(yaml_path))
    assert loaded_config.name == config.name
    assert loaded_config.value == config.value

    # 测试JSON格式
    json_path = tmp_path / "config.json"
    config.save(str(json_path))
    loaded_config = TestConfig.load(str(json_path))
    assert loaded_config.name == config.name
    assert loaded_config.value == config.value

def test_composite_config():
    # 测试组合配置
    config1 = TestConfig(name="component1", value=1)
    config2 = DerivedTestConfig(name="component2", value=2)
    
    composite = CompositeConfig(
        test1=config1,
        test2=config2
    )
    
    assert composite.test1.value == 1
    assert composite.test2.value == 2
    assert composite.test2.extra_field == "test"

    # 测试组合配置的序列化
    config_dict = composite.to_dict()
    assert config_dict["test1"]["value"] == 1
    assert config_dict["test2"]["value"] == 2

def test_config_validation():
    # 测试必填字段验证
    with pytest.raises(TypeError):
        TestConfig(name="missing_value")

    # 测试类型验证
    with pytest.raises(ValueError):
        TestConfig(name="invalid_value", value="not_an_int")

def test_config_registry_operations():
    # 测试配置注册中心的操作
    configs = ConfigRegistry.list_available_configs()
    assert "test" in configs
    assert "basic" in configs["test"]
    assert "derived" in configs["test"]

    # 测试获取配置参数信息
    params = ConfigRegistry.get_config_params("test", "basic")
    assert "name" in params
    assert "value" in params
    assert "flag" in params

def test_config_conflict_detection():
    # 测试参数冲突检测
    with pytest.raises(ValueError):
        @ConfigRegistry.register("test2", "conflict")
        @dataclass
        class ConflictConfig(BaseConfig):
            # 使用已存在的参数名
            name: str
            value: int
            flag: bool = True