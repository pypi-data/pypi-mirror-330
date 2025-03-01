import pytest
from jsongeekai.perf.deepseek_optimizer import DeepSeekOptimizer, OptimizationSuggestion

@pytest.fixture
def sample_profile_data():
    return {
        # 解析器性能数据
        "avg_string_length": 64,
        "parsing_frequency": 2000,
        "avg_document_size": 2 * 1024 * 1024,  # 2MB
        
        # 内存使用数据
        "object_creation_rate": 1000,
        "avg_object_lifetime_ms": 500,
        "peak_objects": 150,
        "avg_objects": 80,
        "value_type_conversions": 1500
    }

def test_simd_optimization_suggestion(sample_profile_data):
    optimizer = DeepSeekOptimizer()
    suggestions = optimizer.analyze_parser_performance(sample_profile_data)
    
    simd_suggestions = [s for s in suggestions if s.type == 'simd']
    assert len(simd_suggestions) == 1
    
    suggestion = simd_suggestions[0]
    assert suggestion.target == 'JsonParser.parse_string'
    assert suggestion.confidence >= 0.8
    assert 'simd' in suggestion.hardware_requirements

def test_parallel_optimization_suggestion(sample_profile_data):
    optimizer = DeepSeekOptimizer()
    suggestions = optimizer.analyze_parser_performance(sample_profile_data)
    
    parallel_suggestions = [s for s in suggestions if s.type == 'parallel']
    assert len(parallel_suggestions) == 1
    
    suggestion = parallel_suggestions[0]
    assert suggestion.target == 'JsonParser.parse_large_document'
    assert suggestion.confidence >= 0.8
    assert 'cpu_cores' in suggestion.hardware_requirements

def test_memory_optimization_suggestions(sample_profile_data):
    optimizer = DeepSeekOptimizer()
    suggestions = optimizer.analyze_memory_patterns(sample_profile_data)
    
    assert len(suggestions) == 2  # 应该有对象池化和值类型优化两个建议
    
    pooling_suggestions = [s for s in suggestions if s.target == 'JsonObject']
    assert len(pooling_suggestions) == 1
    assert pooling_suggestions[0].type == 'memory'
    
    value_suggestions = [s for s in suggestions if s.target == 'JsonValue']
    assert len(value_suggestions) == 1
    assert value_suggestions[0].type == 'memory'

def test_full_optimization_pipeline(sample_profile_data):
    optimizer = DeepSeekOptimizer()
    all_suggestions = optimizer.suggest_optimizations(sample_profile_data)
    
    # 验证总建议数量
    assert len(all_suggestions) == 4  # SIMD + 并行 + 对象池化 + 值类型优化
    
    # 验证建议排序（按预期收益降序）
    improvements = [s.estimated_improvement for s in all_suggestions]
    assert improvements == sorted(improvements, reverse=True)
    
    # 验证建议完整性
    for suggestion in all_suggestions:
        assert isinstance(suggestion, OptimizationSuggestion)
        assert suggestion.code_snippet
        assert 0 <= suggestion.confidence <= 1
        assert suggestion.estimated_improvement > 0

def test_hardware_capability_detection():
    optimizer = DeepSeekOptimizer()
    
    # 验证硬件特性检测
    assert hasattr(optimizer, 'has_avx2')
    assert hasattr(optimizer, 'has_avx512')
    assert hasattr(optimizer, 'optimal_threads')
    
    # 验证线程数合理性
    assert optimizer.optimal_threads > 0
    assert optimizer.optimal_threads <= 32  # 假设最大支持32线程
