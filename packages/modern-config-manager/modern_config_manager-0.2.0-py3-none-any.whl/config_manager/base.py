from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import json
import yaml
from pathlib import Path


@dataclass
class BaseConfig:
    """配置类的基类，提供配置的基本功能。

    该类作为所有配置类的基类，提供了配置的序列化、反序列化、类型转换等基本功能。
    支持 JSON 和 YAML 格式的配置文件读写，并能自动进行参数类型转换。

    属性:
        name (str): 配置的名称
        version (str): 配置的版本号
    """
    name: str
    version: str
    
    def to_dict(self) -> Dict[str, Any]:
        """将配置对象转换为字典格式。

        Returns:
            Dict[str, Any]: 包含所有配置参数的字典
        """
        return {k: v for k, v in self.__dict__.items()}
    
    def save(self, path: str) -> None:
        """将配置保存到文件。

        支持保存为 JSON 或 YAML 格式，根据文件扩展名自动选择格式。

        Args:
            path (str): 保存配置的文件路径，支持 .json、.yaml 或 .yml 扩展名

        Raises:
            ValueError: 当文件格式不支持时抛出
        """
        path = Path(path)
        if path.suffix == '.json':
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        elif path.suffix in {'.yaml', '.yml'}:
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(self.to_dict(), f, allow_unicode=True)
        else:
            raise ValueError(f"不支持的文件格式：{path.suffix}")
    
    @classmethod
    def load(cls, path: str) -> 'BaseConfig':
        """从文件加载配置。

        支持从 JSON 或 YAML 文件加载配置，根据文件扩展名自动选择格式。

        Args:
            path (str): 配置文件的路径，支持 .json、.yaml 或 .yml 扩展名

        Returns:
            BaseConfig: 加载的配置对象

        Raises:
            ValueError: 当文件格式不支持时抛出
        """
        path = Path(path)
        if path.suffix == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif path.suffix in {'.yaml', '.yml'}:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        else:
            raise ValueError(f"不支持的文件格式：{path.suffix}")
        return cls(**data)
    
    def __post_init__(self):
        """数据类初始化后的处理函数。

        执行参数的自动类型转换，支持以下转换：
        1. 基本类型（int、float、bool、str）的转换
        2. 字符串到布尔值的转换（'true', 'yes', '1' 转换为 True）
        3. 逗号分隔的字符串到列表的转换
        4. JSON 字符串到字典的转换

        Raises:
            ValueError: 当参数值无法转换为目标类型时抛出
        """
        for field_name, field in self.__class__.__dataclass_fields__.items():
            value = getattr(self, field_name)
            if value is not None:
                try:
                    # 处理基本类型
                    if field.type in {int, float, bool, str}:
                        if field.type == bool and isinstance(value, str):
                            value = value.lower() in {"true", "yes", "1"}
                        else:
                            value = field.type(value)
                    # 处理列表类型
                    elif hasattr(field.type, "__origin__") and field.type.__origin__ is list:
                        if isinstance(value, str):
                            # 假设值是逗号分隔的字符串
                            items = value.split(",")
                            item_type = field.type.__args__[0]  # 获取列表元素类型
                            value = [item_type(item.strip()) for item in items]
                    # 处理字典类型
                    elif hasattr(field.type, "__origin__") and field.type.__origin__ is dict:
                        if isinstance(value, str):
                            # 假设值是JSON格式的字符串
                            value = json.loads(value)
                    
                    setattr(self, field_name, value)
                except (ValueError, TypeError, json.JSONDecodeError) as e:
                    raise ValueError(f"参数 {field_name} 的值 {value} 无法转换为类型 {field.type}: {str(e)}")