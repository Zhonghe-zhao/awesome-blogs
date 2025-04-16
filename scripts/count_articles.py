import os
import glob
import re
from datetime import datetime

def count_md_files(directory):
    """统计指定目录下的.md文件数量（排除README.md）"""
    print(f"Checking directory: {directory}")
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and file != 'README.md':
                md_files.append(os.path.join(root, file))
    print(f"Found files: {md_files}")
    return len(md_files)

def update_readme():
    # 分类配置
    categories = {
        'programming': ('编程语言', '深入理解各种语言特性'),
        'architecture': ('系统架构', '分布式/高可用设计模式'),
        'tools': ('开发者工具', '提升效率的神器'),
        'thinking': ('认知思维', '技术人的思维模型')
    }
    
    # 获取各分类文章数量
    counts = {cat: count_md_files(os.path.join('blogs', cat)) for cat in categories}
    print(f"Article counts: {counts}")
    
    # 读取README内容
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    print("Original content snippet:\n", content[:200])
    
    # 更新文章数量（更宽松的正则表达式）
    for cat, (name, desc) in categories.items():
        # 匹配各种可能的空格和格式变化
        pattern = rf'(\|\s*\[{name}\]\(/blogs/{cat}\)\s*\|\s*{desc}\s*\|\s*)\d+(\s*\|\s*)'
        replacement = f'\\g<1>{counts[cat]}\\g<2>'
        content, n = re.subn(pattern, replacement, content)
        print(f"Updated {cat} count: {n} replacements made (pattern used: {pattern})")
    
    # 更新推荐日期
    today = datetime.now().strftime("%Y.%m.%d")
    content, n = re.subn(
        r'(## 🏻 )\d{4}\.\d{2}\.\d{2}(日推荐)',
        f'\\g<1>{today}\\g<2>',
        content
    )
    print(f"Updated date: {n} replacements made")
    
    # 写回README
    with open('README.md', 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print("README.md has been updated successfully.")
    print("Updated content snippet:\n", content[:200])

if __name__ == '__main__':
    update_readme()