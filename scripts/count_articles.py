import os
import re
from datetime import datetime

def count_md_files(directory):
    """统计指定目录下的.md文件数量（排除README.md），不递归子目录"""
    print(f"扫描目录: {os.path.abspath(directory)}")  # 打印绝对路径
    
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"警告：目录不存在 {directory}")
        return 0
    
    try:
        # 获取目录下所有条目（不递归）
        entries = os.listdir(directory)
    except PermissionError:
        print(f"错误：无权限访问 {directory}")
        return 0
    
    md_files = []
    for entry in entries:
        full_path = os.path.join(directory, entry)
        # 检查是否为文件（排除目录）
        if os.path.isfile(full_path):
            # 处理大小写问题 + 排除README.md
            if entry.lower().endswith('.md') and entry != 'README.md':
                md_files.append(entry)
    
    print(f"找到匹配文件: {md_files}")
    return len(md_files)

def update_readme():
    # 分类配置（路径需与实际目录名完全一致）
    categories = {
        'books': ('书籍', '读书笔记/好书推荐'),
        'tools': ('开发者工具', '提升效率的神器'),
        'thinking': ('习惯思考', '鱼总是最后一个看见水的')
    }
    
    # 获取各分类文章数量（添加调试）
    counts = {}
    for cat in categories:
        dir_path = os.path.join('blogs', cat)
        counts[cat] = count_md_files(dir_path)
    print(f"文章数量统计: {counts}")
    
    # 读取README内容
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("错误：README.md 文件不存在")
        return
    
    # 更新文章数量（优化正则表达式）
    for cat, (name, desc) in categories.items():
        # 匹配更灵活的空格和特殊字符
        pattern = rf'(\|.*?$${re.escape(name)}$$$/blogs/{re.escape(cat)}$.*?\|.*?)\d+(.*?\|)'
        replacement = f'\\g<1>{counts[cat]}\\g<2>'
        content, n = re.subn(pattern, replacement, content)
        print(f"更新 {cat} 数量: 完成 {n} 处替换")
    
    # 更新推荐日期（处理特殊符号）
    today = datetime.now().strftime("%Y.%m.%d")
    content, n = re.subn(
        r'(## 🏻\s*)\d{4}\.\d{2}\.\d{2}(日推荐)',
        f'\\g<1>{today}\\g<2>',
        content
    )
    print(f"更新日期: 完成 {n} 处替换")
    
    # 写回README（保持UNIX换行符）
    try:
        with open('README.md', 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print("README.md 更新成功")
    except Exception as e:
        print(f"写入失败: {str(e)}")

if __name__ == '__main__':
    # 添加工作目录检查
    print(f"当前工作目录: {os.getcwd()}")
    update_readme()