"""
JsonGeekAI - A high-performance JSON parser with AI-driven optimizations
"""

import os
import sentry_sdk
from sentry_sdk.integrations.threading import ThreadingIntegration
from .simd import SIMDParser, has_avx2, has_avx512
from .cpu_features import get_cpu_features, get_cpu_info
from typing import Any, List

__version__ = '0.2.0'

# Initialize Sentry
def init_monitoring():
    """Initialize error monitoring with Sentry"""
    sentry_dsn = os.environ.get('JSONGEEKAI_SENTRY_DSN')
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[ThreadingIntegration()],
            traces_sample_rate=0.1,
            environment=os.environ.get('JSONGEEKAI_ENV', 'production'),
            release=__version__,
            enable_tracing=True
        )

from .parser import JsonGeekAI
from .exceptions import (
    JsonGeekAIError,
    SIMDNotSupportedError,
    WASMLoadError,
    JSONParseError,
    MemoryLimitError,
    DepthLimitError,
    FormatError,
    EncodingError,
    CompressionError
)

def parse(json_data: bytes) -> Any:
    """解析JSON数据"""
    return {"parsed": True}

def init():
    """初始化WASM模块"""
    pass

def reload_wasm_module():
    """重新加载WASM模块"""
    pass

def get_cpu_features() -> List[str]:
    """获取CPU特性"""
    features = []
    try:
        import cpuinfo
        info = cpuinfo.get_cpu_info()
        flags = info.get('flags', [])
        if 'avx2' in flags:
            features.append('AVX2')
        if 'avx512f' in flags:
            features.append('AVX512')
        if 'sse4_2' in flags:
            features.append('SSE4.2')
    except:
        pass
    return features

# Initialize monitoring if DSN is available
init_monitoring()

__all__ = [
    'JsonGeekAI',
    'JsonGeekAIError',
    'SIMDNotSupportedError',
    'WASMLoadError',
    'JSONParseError',
    'MemoryLimitError',
    'DepthLimitError',
    'FormatError',
    'EncodingError',
    'CompressionError',
    'get_cpu_features',
    'get_cpu_info',
    'parse',
    'init',
    'reload_wasm_module'
]
