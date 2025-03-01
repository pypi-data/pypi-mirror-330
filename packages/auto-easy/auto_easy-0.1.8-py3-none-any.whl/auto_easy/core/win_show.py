import os
import importlib.util
import sys

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 将项目根目录添加到 sys.path
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

def check_import_errors(directory):
    """
    递归遍历指定目录中的所有 Python 文件，检查是否存在 import 错误。

    :param directory: 要检查的目录路径
    :return: 包含导入错误信息的字典，键为文件路径，值为错误信息
    """
    error_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    spec = importlib.util.spec_from_file_location(
                        file.replace('.py', ''), file_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[spec.name] = module
                    spec.loader.exec_module(module)
                except ImportError as e:
                    error_files[file_path] = str(e)
    return error_files

if __name__ == "__main__":
    target_directory = 'auto_easy'
    errors = check_import_errors(target_directory)
    if errors:
        print("发现以下导入错误：")
        for file_path, error in errors.items():
            print(f"文件: {file_path}, 错误: {error}")
    else:
        print("未发现导入错误。")
