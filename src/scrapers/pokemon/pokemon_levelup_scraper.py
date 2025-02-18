import time
import pandas as pd
from pathlib import Path
from typing import Dict, List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

class PokemonLevelUpScraper:
    def __init__(self):
        self.base_url = "https://dex.pokemonshowdown.com/pokemon/{name_en}"
        
        # 设置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # 初始化WebDriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # 设置等待时间
        self.wait = WebDriverWait(self.driver, 10)

    def get_levelup_moves(self, name_en: str) -> Dict[str, List[str]]:
        """获取宝可梦的升级技能"""
        try:
            url = self.base_url.format(name_en=name_en.lower())
            self.driver.get(url)
            
            # 等待页面加载完成
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            moves_dict = {}  # 改用字典存储等级对应的技能列表
            
            # 找到Level-up标题
            levelup_header = soup.find('h3', string='Level-up')
            if not levelup_header:
                print(f"未找到{name_en}的升级技能信息")
                return moves_dict
                
            # 获取父级ul标签
            moves_ul = levelup_header.find_parent('ul')
            if not moves_ul:
                return moves_dict
                
            # 遍历技能列表
            current = levelup_header.find_parent('li').find_next_sibling('li')
            while current and not current.find('h3'):
                if 'result' in current.get('class', []):
                    # 获取等级和技能名称
                    tag_span = current.select_one('.tagcol')
                    move_span = current.select_one('.shortmovenamecol')
                    
                    if tag_span and move_span:
                        level = tag_span.text.strip()
                        move_name = move_span.text.strip()
                        
                        # 初始化列表（如果不存在）
                        if level not in moves_dict:
                            moves_dict[level] = []
                        
                        # 添加技能到对应等级的列表
                        moves_dict[level].append(move_name)
                
                current = current.find_next_sibling('li')
            
            return moves_dict
            
        except Exception as e:
            print(f"获取{name_en}的升级技能失败: {e}")
            return {}

    def update_excel_with_levelup_moves(self, excel_file: str):
        """更新Excel文件，添加升级技能信息"""
        try:
            print(f"读取Excel文件: {excel_file}")
            # 读取现有的Excel文件
            with pd.ExcelFile(excel_file) as xls:
                df = pd.read_excel(xls, sheet_name=0)  # 读取第一个sheet
                
                # 获取所有英文名称
                pokemon_names = df['英文名称'].dropna().unique().tolist()
                print(f"找到 {len(pokemon_names)} 个宝可梦")
                
                # 创建新的DataFrame来存储升级技能信息
                levelup_data = []
                
                # 获取每个宝可梦的升级技能
                for pokemon in tqdm(pokemon_names, desc="获取升级技能"):
                    moves = self.get_levelup_moves(pokemon)
                    if moves:
                        # 将技能信息格式化为字符串
                        moves_str = []
                        for level, move_list in moves.items():
                            if not level or level == '–':
                                # 初始技能用|分隔，整体用()包裹
                                moves_str.append(f"({','.join(move_list)})")
                            else:
                                # 每个等级的技能列表
                                for move in move_list:
                                    moves_str.append(f"[{level}:{move}]")
                        
                        levelup_data.append({
                            '宝可梦': pokemon,
                            '升级技能': ' '.join(moves_str)
                        })
                    time.sleep(0.5)
                
                # 创建新的DataFrame
                df_levelup = pd.DataFrame(levelup_data)
                
                # 保存到新的sheet
                with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
                    # 如果sheet2已存在，先删除它
                    if 'LevelUpMoves' in writer.book.sheetnames:
                        idx = writer.book.sheetnames.index('LevelUpMoves')
                        writer.book.remove(writer.book.worksheets[idx])
                    
                    # 写入新的sheet
                    df_levelup.to_excel(writer, sheet_name='LevelUpMoves', index=False)
                    
                    # 调整列宽
                    worksheet = writer.sheets['LevelUpMoves']
                    worksheet.column_dimensions['A'].width = 30  # 宝可梦名称列
                    worksheet.column_dimensions['B'].width = 100  # 升级技能列
                
                print("\n升级技能信息已保存到新的sheet页: LevelUpMoves")
                
        except Exception as e:
            print(f"更新Excel文件失败: {e}")

    def __del__(self):
        """清理资源"""
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    scraper = PokemonLevelUpScraper()
    excel_file = 'output/pokemon_data.xlsx'
    print("开始获取升级技能信息...")
    scraper.update_excel_with_levelup_moves(excel_file)
    scraper.__del__()

        # 测试几个典型的宝可梦

    # test_pokemon = [

    #     'Bulbasaur',      # 初始宝可梦

    #     'Charizard',      # 进化宝可梦

    #     'Mewtwo',         # 传说宝可梦

    #     'Pikachu',        # 特殊宝可梦

    #     'Eevee',          # 多进化宝可梦

    #     'Ditto'           # 特殊宝可梦（可能没有升级技能）

    # ]

    

    # print("开始测试...")

    # for pokemon in test_pokemon:

    #     print(f"\n处理 {pokemon}...")

    #     moves = scraper.get_levelup_moves(pokemon)

    #     if moves:

    #         # 格式化输出

    #         moves_str = []

    #         for level, move_list in moves.items():

    #             if level == '-':

    #                 moves_str.append(f"初始技能: ({','.join(move_list)})")

    #             else:

    #                 for move in move_list:

    #                     moves_str.append(f"[{level}:{move}]")

    #         print(' '.join(moves_str))

if __name__ == "__main__":
    main() 