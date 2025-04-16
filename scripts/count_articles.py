import os
import glob
import re

def count_articles():
    categories = {

        'thinking': '认知思维'
    }
    
    counts = {}
    for category in categories.keys():
        path = f"blogs/{category}/*.md"
        counts[category] = len([f for f in glob.glob(path) if not f.endswith('README.md')])
    
    return counts

def update_readme(counts):
    with open('README.md', 'r+', encoding='utf-8') as f:
        content = f.read()
        
        # 使用正则表达式替换表格中的数字
        for category, count in counts.items():
            pattern = rf'\| \[.*\]\(/blogs/{category}\) \| .* \| \d+ \|'
            replacement = f'| [{categories[category]}](/blogs/{category}) | {categories[category]} | {count} |'
            content = re.sub(pattern, replacement, content)
        
        f.seek(0)
        f.write(content)
        f.truncate()

if __name__ == '__main__':
    counts = count_articles()
    update_readme(counts)