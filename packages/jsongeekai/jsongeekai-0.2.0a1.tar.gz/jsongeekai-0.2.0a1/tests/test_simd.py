"""Test SIMD optimizations."""
import json
import pytest
import numpy as np
from jsonschema import validate
from jsongeekai.simd import SIMDParser, has_avx2, has_avx512
from jsongeekai.exceptions import SIMDNotSupportedError
import random
import string
import uuid
from datetime import datetime

def generate_complex_json(size_mb=1):
    """生成指定大小的复杂JSON数据"""
    data = {
        "metadata": {
            "version": "1.0",
            "generator": "test_generator",
            "timestamp": str(datetime.now().isoformat()),
            "size": f"{size_mb}MB"
        },
        "settings": {
            "encoding": "utf-8",
            "compression": "none",
            "validation": True,
            "cache_enabled": True,
            "max_depth": 10
        },
        "data": []
    }
    
    # 计算每个数据项的大致大小
    sample_item = {
        "id": str(uuid.uuid4()),
        "type": "test_data",
        "attributes": {
            "name": "Test_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            "description": "Description_" + ''.join(random.choices(string.ascii_letters + string.digits, k=20)),
            "tags": ["parsing", "speed", "performance", "memory", "validation"]
        },
        "statistics": {
            "views": random.randint(0, 1000000),
            "likes": random.randint(0, 50000),
            "shares": random.randint(0, 10000)
        },
        "status": {
            "is_active": random.choice([True, False]),
            "last_updated": str(datetime.now().isoformat()),
            "version": f"1.{random.randint(0, 100)}"
        }
    }
    
    # 计算需要生成的数据项数量
    sample_json = json.dumps(sample_item)
    items_needed = (size_mb * 1024 * 1024) // len(sample_json)
    
    # 生成数据
    for _ in range(items_needed):
        item = {
            "id": str(uuid.uuid4()),
            "type": "test_data",
            "attributes": {
                "name": "Test_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
                "description": "Description_" + ''.join(random.choices(string.ascii_letters + string.digits, k=20)),
                "tags": ["parsing", "speed", "performance", "memory", "validation"]
            },
            "statistics": {
                "views": random.randint(0, 1000000),
                "likes": random.randint(0, 50000),
                "shares": random.randint(0, 10000)
            },
            "status": {
                "is_active": random.choice([True, False]),
                "last_updated": str(datetime.now().isoformat()),
                "version": f"1.{random.randint(0, 100)}"
            }
        }
        data["data"].append(item)
    
    return data

# 定义期望的JSON Schema
EXPECTED_SCHEMA = {
    "type": "object",
    "required": ["metadata", "settings", "data"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["version", "generator", "timestamp", "size"],
            "properties": {
                "version": {"type": "string"},
                "generator": {"type": "string"},
                "timestamp": {"type": "string"},
                "size": {"type": "string"}
            }
        },
        "settings": {
            "type": "object",
            "required": ["encoding", "compression", "validation", "cache_enabled", "max_depth"],
            "properties": {
                "encoding": {"type": "string"},
                "compression": {"type": "string"},
                "validation": {"type": "boolean"},
                "cache_enabled": {"type": "boolean"},
                "max_depth": {"type": "integer"}
            }
        },
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "type", "attributes", "statistics", "status"],
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "attributes": {
                        "type": "object",
                        "required": ["name", "description", "tags"],
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 5,
                                "maxItems": 5
                            }
                        }
                    },
                    "statistics": {
                        "type": "object",
                        "required": ["views", "likes", "shares"],
                        "properties": {
                            "views": {"type": "integer"},
                            "likes": {"type": "integer"},
                            "shares": {"type": "integer"}
                        }
                    },
                    "status": {
                        "type": "object",
                        "required": ["is_active", "last_updated", "version"],
                        "properties": {
                            "is_active": {"type": "boolean"},
                            "last_updated": {"type": "string"},
                            "version": {"type": "string"}
                        }
                    }
                }
            }
        }
    }
}

def test_simd_capability_detection():
    """测试SIMD能力检测"""
    # 检测AVX2和AVX512支持
    avx2_support = has_avx2()
    avx512_support = has_avx512()
    
    print(f"AVX2 support: {avx2_support}")
    print(f"AVX512 support: {avx512_support}")
    
    # 验证返回类型
    assert isinstance(avx2_support, bool)
    assert isinstance(avx512_support, bool)
    
    # 如果支持AVX512，应该也支持AVX2
    if avx512_support:
        assert avx2_support

def test_simd_parser_basic():
    """测试SIMD解析器基本功能"""
    parser = SIMDParser()
    
    # 测试简单的JSON字符串
    test_str = '{"key": "value"}'
    result = parser.parse(test_str)
    
    print(f"Basic test result: {result}")
    
    # 验证解析结果
    assert isinstance(result, dict)
    assert "key" in result
    assert result["key"] == "value"

def test_string_parsing_with_escapes():
    """测试带转义字符的字符串解析"""
    parser = SIMDParser()
    
    # 测试带转义字符的JSON字符串
    test_str = '{"key": "value with \\"quotes\\" and \\n newline"}'
    result = parser.parse(test_str)
    
    print(f"Escape test result: {result}")
    
    # 验证解析结果
    assert isinstance(result, dict)
    assert "key" in result
    assert result["key"] == 'value with "quotes" and \n newline'

def test_error_handling():
    """测试错误处理"""
    parser = SIMDParser()
    
    # 测试无效的JSON字符串
    with pytest.raises(SIMDNotSupportedError):
        parser.parse("{invalid json}")

def test_large_json():
    """测试大型JSON处理"""
    parser = SIMDParser()
    
    # 生成复杂的测试数据
    test_data = generate_complex_json(size_mb=1)
    test_str = json.dumps(test_data)
    
    print(f"\nLarge JSON test:")
    print(f"Test data size: {len(test_str)} bytes")
    print(f"Sample data structure:")
    print(json.dumps(test_data["data"][0], indent=2)[:500] + "...")
    
    # 解析数据
    try:
        result = parser.parse(test_str)
        
        # 验证结果
        validate(instance=result, schema=EXPECTED_SCHEMA)
        print("\nJSON Schema validation passed!")
        
        # 验证数据完整性
        assert len(result["data"]) > 0, "No data items found"
        assert all(isinstance(item["id"], str) for item in result["data"]), "Invalid ID format"
        assert all(len(item["attributes"]["tags"]) == 5 for item in result["data"]), "Invalid tags count"
        assert all(isinstance(item["statistics"]["views"], int) for item in result["data"]), "Invalid views format"
        
        # 打印性能指标
        metrics = parser.get_performance_metrics()
        print("\nPerformance metrics:")
        print(f"Total parse time: {metrics['total_parse_time']:.3f}s")
        print(f"Bytes processed: {metrics['total_bytes_processed']:,} bytes")
        print(f"Processing speed: {metrics['bytes_per_second']:,.0f} bytes/s")
        print(f"Average tokens per parse: {metrics['avg_tokens_per_parse']:.1f}")
        print(f"Cache hit ratio: {metrics['cache_hit_ratio']:.2%}")
        
    except Exception as e:
        print(f"\nError during parsing: {e}")
        print("Sample of parsed data:")
        if 'result' in locals():
            print(json.dumps(result, indent=2)[:500] + "...")
        raise
