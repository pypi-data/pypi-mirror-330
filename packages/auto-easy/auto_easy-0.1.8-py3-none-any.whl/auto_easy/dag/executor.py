import os
import ast
import importlib.util


def check_import_errors(directory):
    """
    递归遍历指定目录中的所有 Python 文件，检查是否存在 import 错误。
    :param directory: 要检查的目录路径
    :return: 包含导入错误信息的字典，键为文件路径，值为错误信息列表
    """
    error_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                errors = []
                try:
                    # 静态分析 import 语句
                    with open(file_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ImportFrom):
                                module_name = node.module
                                for name in node.names:
                                    try:
                                        if module_name:
                                            full_module_name = f"{module_name}.{name.name}"
                                        else:
                                            full_module_name = name.name
                                        spec = importlib.util.find_spec(full_module_name)
                                        if spec is None:
                                            error_msg = f"Import error: '{name.name}' from '{module_name}' not found in {file_path}"
                                            errors.append(error_msg)
                                    except (ImportError, AttributeError):
                                        error_msg = f"Import error: '{name.name}' from '{module_name}' in {file_path}"
                                        errors.append(error_msg)
                    # 如果有错误，记录到结果中
                    if errors:
                        error_files[file_path] = errors
                except SyntaxError as e:
                    error_msg = f"Syntax error in {file_path}: {str(e)}"
                    error_files[file_path] = [error_msg]
    return error_files


if __name__ == "__main__":
    target_directory = 'auto_easy'
    errors = check_import_errors(target_directory)
    if errors:
        print("发现以下导入错误：")
        for file_path, error_list in errors.items():
            print(f"文件: {file_path}")
            for error in error_list:
                print(f"  - {error}")
    else:
        print("未发现导入错误。")