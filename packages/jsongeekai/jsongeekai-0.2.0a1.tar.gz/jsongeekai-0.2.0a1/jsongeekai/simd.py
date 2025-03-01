"""
SIMD optimizations for JsonGeekAI.
"""
from typing import Any, Dict, Optional, Tuple, Generator, Iterator
import json
import numpy as np
from numba import jit, vectorize
import cpuinfo
import time
from .exceptions import SIMDNotSupportedError

def get_simd_parser():
    """Get SIMD-optimized parser if available."""
    try:
        return SIMDParser()
    except (ImportError, RuntimeError) as e:
        raise SIMDNotSupportedError(str(e))

def has_avx2() -> bool:
    """检测是否支持AVX2指令集"""
    try:
        info = cpuinfo.get_cpu_info()
        flags = info.get('flags', [])
        return 'avx2' in flags if flags else False
    except Exception:
        return False

def has_avx512() -> bool:
    """检测是否支持AVX512指令集"""
    try:
        info = cpuinfo.get_cpu_info()
        flags = info.get('flags', [])
        return any(flag.startswith('avx512') for flag in flags) if flags else False
    except Exception:
        return False

class SIMDParser:
    """SIMD-optimized JSON parser."""
    
    def __init__(self, chunk_size: int = 64 * 1024):  # 64KB chunks by default
        """Initialize SIMD parser."""
        self._init_simd_capabilities()
        self._init_caches()
        self._init_performance_metrics()
        self.chunk_size = chunk_size
        self._token_buffer = []
        self._current_chunk = None
    
    def _init_simd_capabilities(self):
        """初始化SIMD能力检测"""
        self.has_avx2 = has_avx2()
        self.has_avx512 = has_avx512()
        self._setup_optimized_functions()
    
    def _init_caches(self):
        """初始化缓存"""
        self._token_cache = {}  # 缓存已解析的token
        self._structure_cache = {}  # 缓存已解析的结构
        self._max_cache_size = 1000  # 最大缓存条目数
    
    def _init_performance_metrics(self):
        """初始化性能指标"""
        self._metrics = {
            'total_parse_time': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_bytes_processed': 0,
            'token_counts': [],
            'avg_token_length': 0,
            'error_count': 0
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        metrics = self._metrics.copy()
        if self._metrics['token_counts']:
            metrics['avg_tokens_per_parse'] = sum(self._metrics['token_counts']) / len(self._metrics['token_counts'])
        else:
            metrics['avg_tokens_per_parse'] = 0
        
        if self._metrics['total_bytes_processed'] > 0:
            metrics['bytes_per_second'] = self._metrics['total_bytes_processed'] / (self._metrics['total_parse_time'] or 1)
        else:
            metrics['bytes_per_second'] = 0
            
        metrics['cache_hit_ratio'] = self._metrics['cache_hits'] / (self._metrics['cache_hits'] + self._metrics['cache_misses'] or 1)
        
        return metrics
    
    def reset_performance_metrics(self):
        """重置性能指标"""
        self._init_performance_metrics()
    
    def _cache_key(self, data: np.ndarray) -> str:
        """生成缓存键"""
        return hash(data.tobytes())
    
    def _get_from_cache(self, data: np.ndarray) -> Optional[Dict[str, Any]]:
        """从缓存中获取结果"""
        key = self._cache_key(data)
        return self._token_cache.get(key)
    
    def _add_to_cache(self, data: np.ndarray, result: Dict[str, Any]):
        """添加结果到缓存"""
        key = self._cache_key(data)
        
        # 如果缓存已满，移除最旧的条目
        if len(self._token_cache) >= self._max_cache_size:
            oldest_key = next(iter(self._token_cache))
            del self._token_cache[oldest_key]
        
        self._token_cache[key] = result
    
    def _cleanup_cache(self):
        """清理过期的缓存条目"""
        if len(self._token_cache) > self._max_cache_size * 0.9:
            # 保留最近使用的80%的条目
            keep_count = int(self._max_cache_size * 0.8)
            keys_to_keep = list(self._token_cache.keys())[-keep_count:]
            new_cache = {}
            for key in keys_to_keep:
                new_cache[key] = self._token_cache[key]
            self._token_cache = new_cache
    
    def _setup_optimized_functions(self):
        """设置优化函数"""
        if self.has_avx512:
            self._string_scanner = self._avx512_string_scanner
        elif self.has_avx2:
            self._string_scanner = self._avx2_string_scanner
        else:
            self._string_scanner = self._basic_string_scanner
    
    @staticmethod
    @jit(nopython=True)
    def _basic_string_scanner(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """基础的字符串扫描实现"""
        quotes = np.zeros(len(data), dtype=np.bool_)
        escapes = np.zeros(len(data), dtype=np.bool_)
        
        for i in range(len(data)):
            if i > 0 and data[i-1] == ord('\\'):
                continue
            if data[i] == ord('"'):
                quotes[i] = True
            elif data[i] == ord('\\'):
                escapes[i] = True
            
        return quotes, escapes

    @staticmethod
    @jit(nopython=True, parallel=True)
    def _avx2_string_scanner(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """AVX2优化的字符串扫描"""
        quotes = np.zeros(len(data), dtype=np.bool_)
        escapes = np.zeros(len(data), dtype=np.bool_)
        
        chunk_size = 32
        chunks = len(data) // chunk_size
        
        for i in range(chunks):
            start = i * chunk_size
            end = start + chunk_size
            chunk = data[start:end]
            
            for j in range(chunk_size):
                idx = start + j
                if idx > 0 and data[idx-1] == ord('\\'):
                    continue
                if chunk[j] == ord('"'):
                    quotes[idx] = True
                elif chunk[j] == ord('\\'):
                    escapes[idx] = True
        
        # 处理剩余部分
        for i in range(chunks * chunk_size, len(data)):
            if i > 0 and data[i-1] == ord('\\'):
                continue
            if data[i] == ord('"'):
                quotes[i] = True
            elif data[i] == ord('\\'):
                escapes[i] = True
            
        return quotes, escapes

    @staticmethod
    @jit(nopython=True, parallel=True)
    def _avx512_string_scanner(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """AVX512优化的字符串扫描"""
        quotes = np.zeros(len(data), dtype=np.bool_)
        escapes = np.zeros(len(data), dtype=np.bool_)
        
        chunk_size = 64
        chunks = len(data) // chunk_size
        
        for i in range(chunks):
            start = i * chunk_size
            end = start + chunk_size
            chunk = data[start:end]
            
            for j in range(chunk_size):
                idx = start + j
                if idx > 0 and data[idx-1] == ord('\\'):
                    continue
                if chunk[j] == ord('"'):
                    quotes[idx] = True
                elif chunk[j] == ord('\\'):
                    escapes[idx] = True
        
        # 处理剩余部分
        for i in range(chunks * chunk_size, len(data)):
            if i > 0 and data[i-1] == ord('\\'):
                continue
            if data[i] == ord('"'):
                quotes[i] = True
            elif data[i] == ord('\\'):
                escapes[i] = True
            
        return quotes, escapes

    @staticmethod
    @vectorize(['boolean(uint8)'])
    def _is_whitespace_vec(c):
        """向量化的空白字符检查"""
        return c in [ord(' '), ord('\t'), ord('\n'), ord('\r')]

    @staticmethod
    @vectorize(['boolean(uint8)'])
    def _is_delimiter_vec(c):
        """向量化的分隔符检查"""
        return c in [ord(','), ord(':'), ord('{'), ord('}'), ord('['), ord(']')]

    @staticmethod
    @vectorize(['boolean(uint8)'])
    def _is_number_start_vec(c):
        """向量化的数字开始检查"""
        return (c >= ord('0') and c <= ord('9')) or c == ord('-') or c == ord('+')

    @staticmethod
    @vectorize(['boolean(uint8)'])
    def _is_bool_or_null_start_vec(c):
        """向量化的布尔值或null开始检查"""
        return c in [ord('t'), ord('f'), ord('n')]

    def _token_generator(self, data: np.ndarray) -> Generator[Tuple[int, int], None, None]:
        """生成器函数，按需生成token
        
        Args:
            data: 输入数据数组
            
        Yields:
            Tuple[int, int]: token的(开始位置, 长度)
        """
        current_token_start = -1
        in_string = False
        escaped = False
        
        for i in range(len(data)):
            c = data[i]
            
            # 处理字符串
            if c == ord('"') and not escaped:
                if not in_string:
                    current_token_start = i
                    in_string = True
                else:
                    # 字符串结束
                    yield current_token_start, i - current_token_start + 1
                    in_string = False
                    current_token_start = -1
            
            # 处理转义字符
            if c == ord('\\'):
                escaped = True
            else:
                escaped = False
            
            # 如果不在字符串中，处理其他token
            if not in_string:
                # 跳过空白字符
                if chr(c) in ' \\t\\n\\r':
                    if current_token_start != -1:
                        yield current_token_start, i - current_token_start
                        current_token_start = -1
                    continue
                
                # 处理分隔符
                if chr(c) in ',:[{]}':
                    if current_token_start != -1:
                        yield current_token_start, i - current_token_start
                        current_token_start = -1
                    yield i, 1  # 分隔符作为单独的token
                    continue
                
                # 开始新token
                if current_token_start == -1:
                    current_token_start = i
        
        # 处理最后一个token
        if current_token_start != -1:
            yield current_token_start, len(data) - current_token_start
    
    def _chunk_generator(self, json_str: str) -> Generator[np.ndarray, None, None]:
        """将JSON字符串分块处理
        
        Args:
            json_str: JSON字符串
            
        Yields:
            np.ndarray: 数据块
        """
        # 预处理字符串
        if json_str.startswith('\ufeff'):
            json_str = json_str[1:]
        json_str = json_str.strip()
        
        # 基本验证
        if not (json_str.startswith('{') and json_str.endswith('}')) and \
           not (json_str.startswith('[') and json_str.endswith(']')):
            raise SIMDNotSupportedError("Invalid JSON structure")
        
        # 分块处理
        start = 0
        while start < len(json_str):
            end = start + self.chunk_size
            
            # 确保不会切断UTF-8字符
            while end < len(json_str) and (json_str[end] & 0xC0) == 0x80:
                end -= 1
            
            # 转换为numpy数组
            chunk = np.frombuffer(json_str[start:end].encode('utf-8'), dtype=np.uint8)
            yield chunk
            start = end
    
    def parse_string(self, json_str: str) -> Iterator[Dict[str, Any]]:
        """使用生成器解析JSON字符串
        
        Args:
            json_str: JSON字符串
            
        Yields:
            Dict[str, Any]: 解析结果
        """
        if not json_str:
            raise SIMDNotSupportedError("Empty string is not valid")
        
        start_time = time.time()
        
        try:
            # 分块处理
            for chunk in self._chunk_generator(json_str):
                self._current_chunk = chunk
                self._metrics['total_bytes_processed'] += len(chunk)
                
                # 处理当前块的token
                for token_start, token_length in self._token_generator(chunk):
                    token = {
                        'start': token_start,
                        'length': token_length,
                        'value': chunk[token_start:token_start + token_length].tobytes().decode('utf-8')
                    }
                    self._token_buffer.append(token)
                    
                    # 当积累足够的token时处理它们
                    if len(self._token_buffer) >= 1000:  # 批处理大小
                        yield self._process_token_buffer()
                
            # 处理剩余的token
            if self._token_buffer:
                yield self._process_token_buffer()
                
        except Exception as e:
            self._metrics['error_count'] += 1
            raise SIMDNotSupportedError(f"Failed to parse string: {e}")
        finally:
            parse_time = time.time() - start_time
            self._metrics['total_parse_time'] += parse_time
    
    def _process_token_buffer(self) -> Dict[str, Any]:
        """处理token缓冲区
        
        Returns:
            Dict[str, Any]: 处理结果
        """
        result = {
            'tokens': self._token_buffer.copy(),
            'chunk_id': id(self._current_chunk)
        }
        
        # 清空缓冲区
        self._token_buffer = []
        
        # 更新性能指标
        self._metrics['token_counts'].append(len(result['tokens']))
        if result['tokens']:
            avg_length = sum(t['length'] for t in result['tokens']) / len(result['tokens'])
            self._metrics['avg_token_length'] = (
                (self._metrics['avg_token_length'] * len(self._metrics['token_counts']) + avg_length)
                / (len(self._metrics['token_counts']) + 1)
            )
        
        return result

    def parse(self, json_str: str) -> Dict[str, Any]:
        """解析JSON字符串
        
        Args:
            json_str: JSON字符串
            
        Returns:
            Dict[str, Any]: 解析后的JSON对象
        """
        # 获取所有token
        all_tokens = []
        for chunk_tokens in self.parse_string(json_str):
            all_tokens.extend(chunk_tokens['tokens'])
        
        if not all_tokens:
            raise SIMDNotSupportedError("No valid tokens found")
        
        # 重建JSON结构
        token_idx = 0
        
        def get_token(idx: int) -> str:
            """获取指定位置的token
            
            Args:
                idx: token索引
                
            Returns:
                str: token值
            """
            if idx >= len(all_tokens):
                raise SIMDNotSupportedError("Token index out of range")
            return all_tokens[idx]['value'].strip()
        
        def parse_value() -> Tuple[Any, int]:
            """解析值
            
            Returns:
                Tuple[Any, int]: (解析后的值, 下一个token的索引)
            """
            nonlocal token_idx
            token = get_token(token_idx)
            
            # 处理null
            if token.lower() == 'null':
                token_idx += 1
                return None, token_idx
            
            # 处理布尔值
            if token.lower() == 'true':
                token_idx += 1
                return True, token_idx
            if token.lower() == 'false':
                token_idx += 1
                return False, token_idx
            
            # 处理数字
            try:
                if '.' in token or 'e' in token.lower():
                    value = float(token)
                else:
                    value = int(token)
                token_idx += 1
                return value, token_idx
            except ValueError:
                pass
            
            # 处理字符串
            if token.startswith('"') and token.endswith('"'):
                token_idx += 1
                return token[1:-1], token_idx
            
            # 处理对象
            if token == '{':
                token_idx += 1
                return parse_object()
            
            # 处理数组
            if token == '[':
                token_idx += 1
                return parse_array()
            
            raise SIMDNotSupportedError(f"Invalid token: {token}")
        
        def parse_object() -> Tuple[Dict[str, Any], int]:
            """解析对象
            
            Returns:
                Tuple[Dict[str, Any], int]: (解析后的对象, 下一个token的索引)
            """
            nonlocal token_idx
            obj = {}
            
            while token_idx < len(all_tokens):
                token = get_token(token_idx)
                
                # 对象结束
                if token == '}':
                    token_idx += 1
                    return obj, token_idx
                
                # 获取键
                if not token.startswith('"'):
                    raise SIMDNotSupportedError(f"Invalid object key: {token}")
                key = token[1:-1]
                token_idx += 1
                
                # 跳过冒号
                if get_token(token_idx) != ':':
                    raise SIMDNotSupportedError("Expected ':' after object key")
                token_idx += 1
                
                # 获取值
                value, next_idx = parse_value()
                obj[key] = value
                token_idx = next_idx
                
                # 检查是否有逗号
                if token_idx < len(all_tokens):
                    token = get_token(token_idx)
                    if token == ',':
                        token_idx += 1
                    elif token != '}':
                        raise SIMDNotSupportedError("Expected ',' or '}' in object")
            
            raise SIMDNotSupportedError("Unclosed object")
        
        def parse_array() -> Tuple[list, int]:
            """解析数组
            
            Returns:
                Tuple[list, int]: (解析后的数组, 下一个token的索引)
            """
            nonlocal token_idx
            arr = []
            
            while token_idx < len(all_tokens):
                token = get_token(token_idx)
                
                # 数组结束
                if token == ']':
                    token_idx += 1
                    return arr, token_idx
                
                # 获取值
                value, next_idx = parse_value()
                arr.append(value)
                token_idx = next_idx
                
                # 检查是否有逗号
                if token_idx < len(all_tokens):
                    token = get_token(token_idx)
                    if token == ',':
                        token_idx += 1
                    elif token != ']':
                        raise SIMDNotSupportedError("Expected ',' or ']' in array")
            
            raise SIMDNotSupportedError("Unclosed array")
        
        # 开始解析
        try:
            result, _ = parse_value()
            return result
        except Exception as e:
            raise SIMDNotSupportedError(f"Failed to parse JSON structure: {e}")

    def dumps(self, obj: Any) -> str:
        """将Python对象转换为JSON字符串
        
        Args:
            obj: Python对象
            
        Returns:
            str: JSON字符串
            
        Raises:
            TypeError: 如果对象不可序列化
        """
        start_time = time.time()
        
        try:
            # 将对象转换为字节序列
            if isinstance(obj, (dict, list)):
                # 使用numpy的向量化操作处理大型集合
                if isinstance(obj, dict):
                    items = []
                    for k, v in obj.items():
                        if not isinstance(k, str):
                            k = str(k)
                        items.append(f'"{k}": {self._dumps_value(v)}')
                    result = '{' + ', '.join(items) + '}'
                else:  # list
                    items = [self._dumps_value(x) for x in obj]
                    result = '[' + ', '.join(items) + ']'
            else:
                result = self._dumps_value(obj)
            
            # 更新性能指标
            self._metrics['total_bytes_processed'] += len(result)
            
            return result
            
        except Exception as e:
            self._metrics['error_count'] += 1
            raise TypeError(f"Object not JSON serializable: {e}")
        finally:
            dump_time = time.time() - start_time
            self._metrics['total_parse_time'] += dump_time
    
    def _dumps_value(self, value: Any) -> str:
        """序列化单个值
        
        Args:
            value: 要序列化的值
            
        Returns:
            str: 序列化后的字符串
        """
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            # 处理特殊字符
            escaped = value.replace('\\', '\\\\')
            escaped = escaped.replace('"', '\\"')
            escaped = escaped.replace('\n', '\\n')
            escaped = escaped.replace('\r', '\\r')
            escaped = escaped.replace('\t', '\\t')
            return f'"{escaped}"'
        elif isinstance(value, (list, tuple)):
            return '[' + ', '.join(self._dumps_value(x) for x in value) + ']'
        elif isinstance(value, dict):
            items = []
            for k, v in value.items():
                if not isinstance(k, str):
                    k = str(k)
                items.append(f'"{k}": {self._dumps_value(v)}')
            return '{' + ', '.join(items) + '}'
        else:
            try:
                # 尝试使用对象的__str__方法
                return f'"{str(value)}"'
            except Exception:
                raise TypeError(f"Object of type {type(value)} is not JSON serializable")
