"""
PyCliMonitor: A python command line tool that monitoring current system's CPU, GPU, RAM, SSD and Networks.
Version: 1.0
"""


# 在文件顶部导入区域添加
import sys

# 在现有导入语句下方添加语言字典
# 语言配置字典
TEXTS = {
    "en": {
        "system_monitor": "System Resource Monitor",
        "system": "System",
        "cpu_usage": "CPU Usage",
        "model": "Model",
        "gpu_usage": "GPU Usage",
        "usage": "Usage",
        "memory": "Memory",
        "vram": "VRAM",
        "temp": "Temp",
        "memory_usage": "Memory Usage",
        "memory_label": "RAM",
        "swap": "Swap",
        "disk_usage": "Disk Usage",
        "network_interfaces": "Network Interfaces",
        "online": "Online",
        "offline": "Offline",
        "press_exit": "Press Ctrl+C to exit",
        "exiting": "Exiting monitor...",
        "error": "Error occurred",
        "installing": "Installing",
        "install_success": "installed successfully",
        "gpu_unavailable": "GPU information unavailable",
        "unknown_cpu": "Unknown CPU model"
    },
    "cn": {
        "system_monitor": "系统资源监控",
        "system": "系统",
        "cpu_usage": "CPU 使用情况",
        "model": "型号",
        "gpu_usage": "GPU使用情况",
        "usage": "使用率",
        "memory": "显存",
        "vram": "显存",
        "temp": "温度",
        "memory_usage": "内存使用情况",
        "memory_label": "内存",
        "swap": "交换",
        "disk_usage": "磁盘使用情况",
        "network_interfaces": "网络接口",
        "online": "在线",
        "offline": "离线",
        "press_exit": "按 Ctrl+C 退出监控",
        "exiting": "退出监控...",
        "error": "发生错误",
        "installing": "正在安装",
        "install_success": "安装成功",
        "gpu_unavailable": "GPU信息不可用",
        "unknown_cpu": "未知CPU型号"
    }
}

import psutil
import time
import os
import threading
import GPUtil
import subprocess
from tabulate import tabulate
import platform
from datetime import datetime
import shutil

# 检查并安装依赖包
def install_required_packages(lang="en"):
    required_packages = ["psutil", "GPUtil", "tabulate"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{TEXTS[lang]['installing']} {package}...")
            subprocess.check_call(["pip", "install", package])
            print(f"{package} {TEXTS[lang]['install_success']}")

# 记录上一次网络数据，用于计算速率
last_net_io = psutil.net_io_counters()
last_time = time.time()

# 获取终端大小
def get_terminal_size():
    return shutil.get_terminal_size()

# ANSI转义序列
CLEAR_SCREEN = "\033[2J"
CURSOR_HOME = "\033[H"
ERASE_LINE = "\033[K"
CURSOR_UP = "\033[1A"
CURSOR_DOWN = "\033[1B"
RESET_ALL = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RED = "\033[31m"

# 使用ANSI转义序列更新屏幕，避免闪烁
def update_screen():
    # 将光标移动到左上角
    print(CURSOR_HOME, end='')

# 初始化屏幕
def init_screen():
    # 第一次运行时清屏，之后只移动光标
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    # 设置Windows终端支持ANSI转义序列
    if platform.system() == 'Windows':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass

# 获取CPU信息及其主频
def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=0.1, percpu=True)
    cpu_info = []
    
    # 每行显示4个CPU核心
    cores_per_row = 4
    for i in range(0, len(cpu_percent), cores_per_row):
        row = []
        for j in range(cores_per_row):
            if i + j < len(cpu_percent):
                percent = cpu_percent[i+j]
                # 根据CPU负载选择颜色
                color = RESET_ALL
                if percent > 80: color = RED
                elif percent > 60: color = YELLOW
                elif percent > 30: color = GREEN
                
                row.append(f"CPU{i+j:2d}: {color}{percent:5.1f}%{RESET_ALL}")
        cpu_info.append(row)
    
    return cpu_info

# 获取CPU的当前主频
def get_cpu_freq():
    try:
        # 尝试获取全局CPU频率
        cpu_freq = psutil.cpu_freq()
        if cpu_freq and cpu_freq.current:
            return f"{cpu_freq.current:.0f}MHz"
        
        # 尝试获取每核心频率并取平均值
        per_cpu_freq = psutil.cpu_freq(percpu=True)
        if per_cpu_freq and len(per_cpu_freq) > 0:
            valid_freqs = [f.current for f in per_cpu_freq if f and f.current]
            if valid_freqs:
                avg_freq = sum(valid_freqs) / len(valid_freqs)
                return f"{avg_freq:.0f}MHz"
    except:
        pass
    
    return "N/A"

# 获取CPU型号
def get_cpu_model(lang="en"):
    try:
        if platform.system() == 'Windows':
            try:
                import wmi
                w = wmi.WMI()
                processor_info = w.Win32_Processor()[0]
                return processor_info.Name.strip()
            except ImportError:
                # 如果没有wmi模块，使用命令行
                try:
                    output = subprocess.check_output("wmic cpu get name", shell=True)
                    lines = output.decode('utf-8').strip().split('\n')
                    if len(lines) >= 2:
                        return lines[1].strip()
                except:
                    pass
        elif platform.system() == 'Linux':
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if line.startswith('model name'):
                            return line.split(':', 1)[1].strip()
            except:
                pass
        elif platform.system() == 'Darwin':  # macOS
            try:
                output = subprocess.check_output("sysctl -n machdep.cpu.brand_string", shell=True)
                return output.decode('utf-8').strip()
            except:
                pass
                
        # 如果上面的方法都失败，使用platform模块
        return platform.processor()
    except Exception as e:
        return TEXTS[lang]["unknown_cpu"]

# 获取内存信息
def get_memory_info(lang="en"):
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    txt = TEXTS[lang]
    
    # 根据使用率选择颜色
    mem_color = RESET_ALL
    if memory.percent > 85: mem_color = RED
    elif memory.percent > 70: mem_color = YELLOW
    elif memory.percent > 50: mem_color = GREEN
    
    swap_color = RESET_ALL
    if swap.percent > 50: swap_color = RED
    elif swap.percent > 25: swap_color = YELLOW
    
    return [
        [txt["memory_label"], f"{mem_color}{memory.percent:5.1f}%{RESET_ALL}", f"{memory.used/1024**3:.1f}/{memory.total/1024**3:.1f}GB"],
        [txt["swap"], f"{swap_color}{swap.percent:5.1f}%{RESET_ALL}", f"{swap.used/1024**3:.1f}/{swap.total/1024**3:.1f}GB"]
    ]

# 获取磁盘信息
def get_disk_info(lang="en"):
    disk_info = []
    disk_io = psutil.disk_io_counters(perdisk=True) if hasattr(psutil, 'disk_io_counters') else {}
    
    for partition in psutil.disk_partitions():
        if os.name == 'nt' and ('cdrom' in partition.opts or partition.fstype == ''):
            continue
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_name = partition.device.strip("\\").strip(":")
            io_info = disk_io.get(disk_name, None)
            io_text = f"R: {io_info.read_bytes/(1024**2):.1f}MB, W: {io_info.write_bytes/(1024**2):.1f}MB" if io_info else "N/A"
            
            # 根据使用率选择颜色
            disk_color = RESET_ALL
            if usage.percent > 90: disk_color = RED
            elif usage.percent > 75: disk_color = YELLOW
            elif usage.percent > 50: disk_color = GREEN
            
            disk_info.append([
                f"{partition.device} ({partition.mountpoint})",
                f"{disk_color}{usage.percent:5.1f}%{RESET_ALL}",
                f"{usage.used/1024**3:.1f}/{usage.total/1024**3:.1f}GB",
                io_text
            ])
        except (PermissionError, FileNotFoundError):
            pass
            
    return disk_info

# 获取网络信息
def get_network_info(lang="en"):
    global last_net_io, last_time
    
    txt = TEXTS[lang]
    
    current_net_io = psutil.net_io_counters()
    current_time = time.time()
    time_delta = current_time - last_time
    
    # 计算速率 (bytes/sec)
    rx_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv) / time_delta
    tx_speed = (current_net_io.bytes_sent - last_net_io.bytes_sent) / time_delta
    
    # 更新上一次的值
    last_net_io = current_net_io
    last_time = current_time
    
    # 设置网络速度颜色
    rx_color = GREEN if rx_speed > 1024*10 else RESET_ALL  # 10KB/s以上显示绿色
    tx_color = BLUE if tx_speed > 1024*5 else RESET_ALL    # 5KB/s以上显示蓝色
    
    network_info = []
    for name, stats in psutil.net_if_stats().items():
        if stats.isup:  # 只显示活动的网络接口
            network_info.append([
                name[:15] + (name[15:] and '...'),
                CYAN + txt["online"] + RESET_ALL if stats.isup else txt["offline"],
                f"↓ {rx_color}{rx_speed/1024:7.1f} KB/s{RESET_ALL} | ↑ {tx_color}{tx_speed/1024:7.1f} KB/s{RESET_ALL}"
            ])
            
    return network_info

# 获取GPU信息
def get_gpu_info(lang="en"):
    txt = TEXTS[lang]
    
    try:
        gpus = GPUtil.getGPUs()
        gpu_info = []
        
        for i, gpu in enumerate(gpus):
            # 根据GPU使用率选择颜色
            load_color = RESET_ALL
            if gpu.load > 0.8: load_color = RED
            elif gpu.load > 0.5: load_color = YELLOW
            elif gpu.load > 0.3: load_color = GREEN
            
            # 根据显存使用率选择颜色
            mem_color = RESET_ALL
            if gpu.memoryUtil > 0.8: mem_color = RED
            elif gpu.memoryUtil > 0.5: mem_color = YELLOW
            elif gpu.memoryUtil > 0.3: mem_color = GREEN
            
            # 根据温度选择颜色
            temp_color = RESET_ALL
            if gpu.temperature > 80: temp_color = RED
            elif gpu.temperature > 70: temp_color = YELLOW
            elif gpu.temperature > 60: temp_color = GREEN
            
            gpu_info.append([
                f"GPU {i}: {gpu.name}",  # 不截断GPU名称
                f"{load_color}{gpu.load*100:5.1f}%{RESET_ALL}",
                f"{mem_color}{gpu.memoryUsed:5.1f}MB / {gpu.memoryTotal:5.1f}MB ({gpu.memoryUtil*100:5.1f}%){RESET_ALL}",
                f"{temp_color}{gpu.temperature}°C{RESET_ALL}"
            ])
            
        return gpu_info
    except Exception as e:
        return [[txt["gpu_unavailable"], str(e)[:30], "", ""]]

# 主监控循环
def monitor(lang="en"):
    # 初始化屏幕
    init_screen()
    
    # 获取语言文本
    txt = TEXTS[lang]
    
    # 缓存计算行数以便在终端大小变化时重绘
    last_line_count = 0
        
    # 获取CPU型号 (只需获取一次)
    cpu_model = get_cpu_model(lang)

    try:
        first_run = True
        while True:
            if first_run:
                # 第一次运行完全清屏
                init_screen()
                first_run = False
            else:
                # 后续运行只将光标移至左上角
                update_screen()
            
            terminal = get_terminal_size()
            term_width = terminal.columns
            
            # 显示标题
            print(f"{BOLD}{CYAN}{txt['system_monitor']:^{term_width}}{RESET_ALL}")
            print(f"{YELLOW}{'=' * term_width}{RESET_ALL}")
            print(f"{MAGENTA}{txt['system']}: {platform.system()} {platform.release()} ({platform.machine()}) | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET_ALL}")
            
            # CPU信息 - 在每次循环中获取最新CPU频率
            current_cpu_freq = get_cpu_freq()
            print(f"\n{BOLD}{txt['cpu_usage']} ({txt['model']}: {CYAN}{cpu_model}{RESET_ALL}):{RESET_ALL}")
            cpu_info = get_cpu_info()
            for row in cpu_info:
                print(f"{' | '.join(row)}", end=ERASE_LINE+"\n")
                
            # GPU信息
            print(f"\n{BOLD}{txt['gpu_usage']}:{RESET_ALL}")
            gpu_info = get_gpu_info(lang)
            for row in gpu_info:
                print(f"{row[0]}: {txt['usage']}:{row[1]}", end="\n")
            for row in gpu_info:
                print(f"{txt['memory']}:{row[2]} {txt['temp']}:{row[3]}", end=ERASE_LINE+"\n")
            
            # 内存和磁盘
            print(f"\n{BOLD}{txt['memory_usage']}:{RESET_ALL}")
            memory_info = get_memory_info(lang)
            for row in memory_info:
                print(f"{row[0]} {row[1]} {row[2]}", end=ERASE_LINE+"\n")
            
            print(f"\n{BOLD}{txt['disk_usage']}:{RESET_ALL}")
            disk_info = get_disk_info(lang)
            for row in disk_info:
                print(f"{row[0][:25]}: {row[1]} {row[2]} {row[3]}", end=ERASE_LINE+"\n")
            
            # 网络接口
            print(f"\n{BOLD}{txt['network_interfaces']}:{RESET_ALL}")
            network_info = get_network_info(lang)
            for row in network_info:
                print(f"{row[0]}: {row[1]} {row[2]}", end=ERASE_LINE+"\n")           
          
            # 底部信息
            print(f"\n{YELLOW}{'=' * term_width}{RESET_ALL}")
            print(f"{BOLD}{txt['press_exit']}{RESET_ALL}", end=ERASE_LINE+"\n")
            
            # 刷新间隔
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{GREEN}{txt['exiting']}{RESET_ALL}")

# 主函数，处理命令行参数
def main():
    try:
        # 获取命令行参数
        lang = "cn" if len(sys.argv) > 1 and sys.argv[1].lower() == "cn" else "en"
        # 安装依赖
        install_required_packages(lang)
        # 启动监控
        monitor(lang)
    except Exception as e:
        txt = TEXTS["cn" if len(sys.argv) > 1 and sys.argv[1].lower() == "cn" else "en"]
        print(f"{BOLD}{RED}{txt['error']}: {e}{RESET_ALL}")

if __name__ == "__main__":
    main()