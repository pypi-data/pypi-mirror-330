import platform
import ctypes
import struct
from typing import List, Dict

def _check_cpuid() -> bool:
    """检查是否支持CPUID指令"""
    if platform.system() != 'Windows':
        return True  # 在非Windows系统上假设支持
    
    try:
        # Windows上尝试执行CPUID
        def cpuid(func, func2=0):
            # EAX, EBX, ECX, EDX
            a = ctypes.c_uint32(func)
            b = ctypes.c_uint32(0)
            c = ctypes.c_uint32(func2)
            d = ctypes.c_uint32(0)
            
            try:
                if platform.machine().endswith('64'):
                    # 64位系统
                    masm = bytearray([
                        0x53,                    # push rbx
                        0x89, 0xd0,              # mov eax,edx
                        0x49, 0x89, 0xc8,        # mov r8,rcx
                        0x0f, 0xa2,              # cpuid
                        0x41, 0x89, 0x00,        # mov [r8],eax
                        0x41, 0x89, 0x58, 0x04,  # mov [r8+4],ebx
                        0x41, 0x89, 0x48, 0x08,  # mov [r8+8],ecx
                        0x41, 0x89, 0x50, 0x0c,  # mov [r8+12],edx
                        0x5b,                    # pop rbx
                        0xc3                     # ret
                    ])
                else:
                    # 32位系统
                    masm = bytearray([
                        0x53,             # push ebx
                        0x57,             # push edi
                        0x8b, 0x7c, 0x24, 0x0c,  # mov edi,[esp+12]
                        0x0f, 0xa2,       # cpuid
                        0x89, 0x07,       # mov [edi],eax
                        0x89, 0x5f, 0x04,  # mov [edi+4],ebx
                        0x89, 0x4f, 0x08,  # mov [edi+8],ecx
                        0x89, 0x57, 0x0c,  # mov [edi+12],edx
                        0x5f,             # pop edi
                        0x5b,             # pop ebx
                        0xc3              # ret
                    ])
                
                # 分配可执行内存
                size = len(masm)
                addr = ctypes.windll.kernel32.VirtualAlloc(
                    None, size, 0x1000, 0x40
                )
                if not addr:
                    return False
                
                # 复制代码到可执行内存
                ctypes.memmove(addr, bytes(masm), size)
                func = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_uint32))(addr)
                
                # 执行CPUID
                regs = (ctypes.c_uint32 * 4)()
                func(regs)
                return True
                
            except:
                return False
                
        return cpuid(0) and cpuid(1)
    except:
        return False

def _get_x86_features() -> List[str]:
    """获取x86 CPU特性"""
    features = []
    
    if not _check_cpuid():
        return features
        
    try:
        # 检查SSE4.2
        def has_sse42():
            try:
                import platform
                if platform.machine().lower() in ('amd64', 'x86_64', 'i386', 'i686'):
                    return True
            except:
                pass
            return False
            
        # 检查AVX2
        def has_avx2():
            try:
                import numpy as np
                return bool(np.show_config().get('AVX2'))
            except:
                pass
            return False
            
        # 检查AVX-512
        def has_avx512():
            try:
                import numpy as np
                return bool(np.show_config().get('AVX512F'))
            except:
                pass
            return False
            
        if has_sse42():
            features.append('sse4.2')
        if has_avx2():
            features.append('avx2')
        if has_avx512():
            features.append('avx512')
            
    except:
        pass
        
    return features

def _get_arm_features() -> List[str]:
    """获取ARM CPU特性"""
    features = []
    
    try:
        if platform.system() == 'Linux':
            # 在Linux上读取/proc/cpuinfo
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'Features' in line:
                        if 'neon' in line.lower():
                            features.append('neon')
                        if 'sve' in line.lower():
                            features.append('sve')
                        break
        elif platform.system() == 'Darwin':
            # 在macOS上，如果是ARM架构就假定支持NEON
            if platform.machine().startswith('arm'):
                features.append('neon')
                
    except:
        pass
        
    return features

def get_cpu_features() -> List[str]:
    """获取当前CPU支持的SIMD特性"""
    arch = platform.machine().lower()
    
    if arch in ('amd64', 'x86_64', 'i386', 'i686'):
        return _get_x86_features()
    elif arch.startswith('arm') or arch.startswith('aarch'):
        return _get_arm_features()
    else:
        return []

def get_cpu_info() -> Dict[str, str]:
    """获取CPU详细信息"""
    info = {
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'simd_features': get_cpu_features()
    }
    
    try:
        if platform.system() == 'Windows':
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
            )
            info['model_name'] = winreg.QueryValueEx(
                key, "ProcessorNameString"
            )[0]
        elif platform.system() == 'Linux':
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line:
                        info['model_name'] = line.split(':')[1].strip()
                        break
        elif platform.system() == 'Darwin':
            import subprocess
            output = subprocess.check_output(
                ['sysctl', '-n', 'machdep.cpu.brand_string']
            ).decode()
            info['model_name'] = output.strip()
    except:
        info['model_name'] = 'Unknown'
        
    return info
