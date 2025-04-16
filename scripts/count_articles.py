import os
import glob
import re
from datetime import datetime

def count_md_files(directory):
    """统计指定目录下的.md文件数量（排除README.md）"""
    return len([f for f in glob.glob(f"{directory}/*.md") 
              if not f.endswith('README.md')])

def update_readme():
    # 获取各分类文章数量
    counts = {
        'programming': count_md_files('blogs/programming'),
        'architecture': count_md_files('blogs/architecture'),
        'tools': count_md_files('blogs/tools'),
        'thinking': count_md_files('blogs/thinking')
    }
    
    # 读取README内容
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新文章数量
    for category, count in counts.items():
        content = re.sub(
            rf'\| \[.*\]\(/blogs/{category}\).*\| \d+ \|',
            f'| [{"编程语言" if category=="programming" else "系统架构" if category=="architecture" else "开发者工具" if category=="tools" else "认知思维"}](/blogs/{category}) | {"深入理解各种语言特性" if category=="programming" else "分布式/高可用设计模式" if category=="architecture" else "提升效率的神器" if category=="tools" else "技术人的思维模型"} | {count} |',
            content
        )
    
    # 更新推荐日期
    today = datetime.now().strftime("%Y.%m.%d")
    content = re.sub(
        r'## 🏻 \d{4}\.\d{1,2}\.\d{1,2}日推荐',
        f'## 🏻 {today}日推荐',
        content
    )
    
    # 写回README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    update_readme()