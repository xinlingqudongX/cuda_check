import os
import wmi
import requests
import re
from typing import List, Tuple

def getComputer(gpu_brand:str = 'NVIDIA'):
    # 创建一个wmi对象
    computer = wmi.WMI()

    # 获取Win32_VideoController类的实例列表
    gpu_info = computer.Win32_VideoController()

    # 遍历每个实例，打印相关信息
    for gpu in gpu_info:
        print("Name:", gpu.Name) # 显卡名称
        print("DriverVersion:", gpu.DriverVersion) # 驱动版本
        print("VideoProcessor:", gpu.VideoProcessor) # 显卡处理器
        print("AdapterRAM:", gpu.AdapterRAM) # 显存大小
        print("CurrentRefreshRate:", gpu.CurrentRefreshRate) # 当前刷新率
        print("CurrentHorizontalResolution:", gpu.CurrentHorizontalResolution) # 当前水平分辨率
        print("CurrentVerticalResolution:", gpu.CurrentVerticalResolution) # 当前垂直分辨率
        if gpu_brand.lower() in gpu.Name.lower():
            return gpu
        print('')
    return 

def getNVIDIA():
    NVIDIA_GPU = {}
    cuda_gpus = 'https://developer.nvidia.com/cuda-gpus'
    res = requests.get(cuda_gpus)
    pattern = r'<tr>.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?<td>(.*?)</td></tr>'
    datas:List[Tuple[str,str,str]] = re.findall(pattern,res.text,re.S)
    for [link,name,version] in datas:
        # print(f'{name} {version} {link}')
        NVIDIA_GPU.setdefault(name,{
            'name':name,
            'link':link,
            'version':version
        })

    cuda_legacy_gpus = 'https://developer.nvidia.com/cuda-legacy-gpus'
    res = requests.get(cuda_legacy_gpus)
    datas:List[Tuple[str,str,str]] = re.findall(pattern,res.text,re.S)
    for [link,name,version] in datas:
        # print(f'{name} {version} {link}')
        NVIDIA_GPU.setdefault(name,{
            'name':name,
            'link':link,
            'version':version
        })
    
    return NVIDIA_GPU

def main():
    gpu = getComputer()
    if not gpu:
        print('未找到相关GPU')
        return
    gpuObj = getNVIDIA()
    [gpu_series,gpu_type, gpu_version ] = gpu.VideoProcessor.split(' ')
    
    for gpu_name in gpuObj.keys():
        if f'{gpu_series} {gpu_type} {gpu_version}' in gpu_name:
            print('CUDA支持,请点击链接:',gpuObj.get(gpu_name).get('link'),gpuObj.get(gpu_name).get('version'))
            return
    print('该GPU不支持CUDA')


if __name__ == '__main__':
    main()