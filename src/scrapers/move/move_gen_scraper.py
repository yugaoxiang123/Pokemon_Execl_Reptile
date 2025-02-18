import re
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, List

class MoveGenScraper:
    def __init__(self):
        self.url = "https://wiki.52poke.com/wiki/招式列表"
        self.output_dir = Path('json')
        self.output_dir.mkdir(exist_ok=True)
        
    def _get_page_content(self) -> str:
        """获取页面内容"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        response.encoding = 'utf-8'
        return response.text
        
    def _parse_gen_section(self, gen_section) -> List[str]:
        """解析每个世代部分的招式"""
        moves = []
        # 找到该世代的表格
        table = gen_section.find_next('table', class_='hvlist')
        if not table:
            return moves
            
        # 遍历表格中的所有行
        for row in table.find_all('tr')[1:]:  # 跳过表头
            cells = row.find_all('td')
            if len(cells) >= 4:  # 确保有足够的单元格
                # 获取英文名（第4个td）
                eng_name = cells[3].get_text(strip=True)
                if eng_name:
                    moves.append(eng_name)
                    
        return moves
        
    def scrape(self) -> Dict[int, List[str]]:
        """爬取所有世代的招式"""
        print("开始爬取招式数据...")
        content = self._get_page_content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # 存储所有世代的招式
        moves_by_gen = {}
        
        # 查找所有世代的标题
        gen_pattern = re.compile(r'第([一二三四五六七八九])世代')
        gen_headers = soup.find_all('span', {'class': 'mw-headline'})
        
        for header in gen_headers:
            if gen_pattern.match(header.get_text()):
                gen_num = self._convert_chinese_num(header.get_text()[1])
                print(f"处理第{gen_num}世代...")
                
                # 获取该世代的所有招式
                moves = self._parse_gen_section(header.parent)
                if moves:
                    moves_by_gen[gen_num] = moves
                    print(f"第{gen_num}世代找到 {len(moves)} 个招式")
        
        # 保存数据
        output_file = self.output_dir / 'moves_by_gen.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(moves_by_gen, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {output_file}")
        
        return moves_by_gen
    
    def _convert_chinese_num(self, chinese_num: str) -> int:
        """将中文数字转换为阿拉伯数字"""
        num_map = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9
        }
        return num_map.get(chinese_num, 0)

def main():
    scraper = MoveGenScraper()
    moves_by_gen = scraper.scrape()
    
    # 打印示例数据
    print("\n示例数据:")
    for gen, moves in moves_by_gen.items():
        print(f"\n第{gen}世代的前5个招式:")
        print(moves[:5])

if __name__ == "__main__":
    main() 