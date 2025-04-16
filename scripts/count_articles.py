import os
import glob
import re
from datetime import datetime

def count_md_files(directory):
    """统计指定目录下的.md文件数量（排除README.md）"""
    return len([f for f in glob.glob(f"{directory}/*.md") 
              if not f.endswith('README.md')])

def update_readme():
    # 分类配置
    categories = {
        'programming': {
            'name': '编程语言',
            'desc': '深入理解各种语言特性'
        },
        'architecture': {
            'name': '系统架构',
            'desc': '分布式/高可用设计模式'
        },
        'tools': {
            'name': '开发者工具',
            'desc': '提升效率的神器'
        },
        'thinking': {
            'name': '认知思维',
            'desc': '技术人的思维模型'
        }
    }
    
    # 获取各分类文章数量
    counts = {category: count_md_files(f'blogs/{category}') 
             for category in categories}
    
    # 读取README内容
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新文章数量
    for category, data in categories.items():
        content = re.sub(
            rf'\| \[.*\]\(/blogs/{category}\).*\| \d+ \|',
            f'| [{data["name"]}](/blogs/{category}) | {data["desc"]} | {counts[category]} |',
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