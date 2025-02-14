import time
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Tuple
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import re

class PokemonEvolutionScraper:
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

    def get_evolution_info(self, name_en: str) -> Optional[Tuple[str, str]]:
        """获取宝可梦的进化信息"""
        try:
            url = self.base_url.format(name_en=name_en.lower())
            self.driver.get(url)
            
            # 等待页面加载完成
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # 找到进化信息的dd标签
            table = soup.find('table', class_='evos')
            if not table:
                return None
            
            dd_tag = table.find_next_sibling('div')
            if not dd_tag:
                return None
                
            # 找到small标签中的进化信息
            small_tag = dd_tag.find('small')
            if small_tag and 'Evolves from' in small_tag.text:
                # 提取进化等级和原始宝可梦名称
                evolution_text = small_tag.text
                level_match = re.search(r'\((.*?)\)', evolution_text)
                # pokemon_match = re.search(r'Evolves from ([^(]+)', evolution_text)
                pokemon_match = re.search(r'Evolves from (\w+)', evolution_text)       
                if level_match and pokemon_match:
                    level = level_match.group(1)
                    base_pokemon = pokemon_match.group(1).strip()
                    return base_pokemon, f"{level}:{name_en}"
            
            return None
            
        except Exception as e:
            print(f"获取{name_en}的进化信息失败: {e}")
            return None

    def update_excel_with_evolution_info(self, excel_file: str):
        """更新Excel文件，添加进化信息"""
        try:
            print(f"读取Excel文件: {excel_file}")
            # 读取现有的Excel文件
            with pd.ExcelFile(excel_file) as xls:
                df = pd.read_excel(xls, sheet_name='LevelUpMoves')  # 读取LevelUpMoves表
            
            # 获取所有英文名称
            pokemon_names = df['宝可梦'].dropna().unique().tolist()
            print(f"找到 {len(pokemon_names)} 个宝可梦")
            
            # 1. 创建新列并指定位置
            column = '进化条件'
            if column not in df.columns:
                # 在第二列位置插入新列
                df.insert(loc=1, column=column, value=None)
                print(f"在目标表格中创建新列: {column}")
            
            # 获取每个宝可梦的进化信息
            for pokemon in tqdm(pokemon_names, desc="获取进化信息"):
                result = self.get_evolution_info(pokemon)
                if result:
                    base_pokemon, evolution_info = result
                    df.loc[df['宝可梦'] == base_pokemon, '进化条件'] = evolution_info
                time.sleep(0.5)
            
            print("\n进化信息已更新到LevelUpMoves表")

            # 保存更新后的数据
            with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name='LevelUpMoves', index=False)
                
                # 调整列宽
                worksheet = writer.sheets['LevelUpMoves']
                worksheet.column_dimensions['A'].width = 30  # 宝可梦名称列
                worksheet.column_dimensions['B'].width = 50  # 进化等级列
                worksheet.column_dimensions['C'].width = 150  # 升级技能列
                
        except Exception as e:
            print(f"更新Excel文件失败: {e}")

    def __del__(self):
        """清理资源"""
        if hasattr(self, 'driver'):
            self.driver.quit()

def test_evolution_scraper():
    scraper = PokemonEvolutionScraper()
    
    # 测试用的宝可梦列表
    test_pokemon = [
        'Charmeleon',    # 基础进化链中间形态
        'Charizard',     # 基础进化链最终形态
        'Charmander',    # 基础进化链初始形态
        'Pikachu',       # 特殊进化链
        'Eevee',         # 多分支进化
        'Mewtwo',        # 没有进化的传说宝可梦
        'Ditto'          # 没有进化的特殊宝可梦
    ]
    
    print("开始测试进化信息获取...")
    for pokemon in test_pokemon:
        print(f"\n处理 {pokemon}...")
        result = scraper.get_evolution_info(pokemon)
        if result:
            base_pokemon, evolution_info = result
            print(f"基础宝可梦: {base_pokemon}")
            print(f"进化信息: {evolution_info}")
        else:
            print("没有进化信息")
        time.sleep(0.5)
    
    scraper.__del__()

if __name__ == "__main__":
    # test_evolution_scraper()  # 取消注释以运行测试
    
    # 或者运行完整的Excel更新
    scraper = PokemonEvolutionScraper()
    excel_file = 'output/pokemon_data.xlsx'
    print("开始获取进化信息...")
    scraper.update_excel_with_evolution_info(excel_file)
    scraper.__del__() 