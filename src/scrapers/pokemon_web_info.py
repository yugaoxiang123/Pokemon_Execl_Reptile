import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from pokemon_web_scraper import PokemonWebScraper

class PokemonWebInfoProcessor:
    def __init__(self):
        self.cache_file = Path('pokemon_name_cache.json')
        self.web_scraper = PokemonWebScraper()
        
    def process_web_data(self, output_file: str):
        """处理网页数据并生成新表格"""
        print("读取宝可梦名称缓存...")
        with open(self.cache_file, 'r', encoding='utf-8') as f:
            name_cache = json.load(f)
            
        # 创建基础数据框
        df = pd.DataFrame({
            'name_en': list(name_cache.keys()),
            'name_cn': list(name_cache.values())
        })
        
        # 添加网页数据爬取部分
        print("从网页获取额外信息...")
        web_data = []
        for name_en in tqdm(df['name_en'], desc="爬取网页数据"):
            info = self.web_scraper.scrape_pokemon_info(name_en)
            if info:
                # 处理基础点数（EV）数据
                ev_yield = info['ev_yield']
                info['ev_hp'] = ev_yield.get('HP', 0)
                info['ev_atk'] = ev_yield.get('攻击', 0)
                info['ev_def'] = ev_yield.get('防御', 0)
                info['ev_spa'] = ev_yield.get('特攻', 0)
                info['ev_spd'] = ev_yield.get('特防', 0)
                info['ev_spe'] = ev_yield.get('速度', 0)
                
                # 处理地区图鉴编号
                pokedex = info['pokedex_numbers']
                for region in ['关都', '城都', '丰缘', '神奥', '合众', '卡洛斯', '阿罗拉', '伽勒尔', '帕底亚']:
                    info[f'dex_{region}'] = pokedex.get(region, '')
                
                # 删除已处理的字典
                del info['ev_yield']
                del info['pokedex_numbers']
            else:
                # 如果获取失败，填充空值
                info = {
                    'category_cn': '', 'abilities_normal': '', 'ability_hidden': '',
                    'catch_rate': '', 'base_exp': '', 'egg_groups': '',
                    'egg_cycles': '', 'gender_ratio': '',
                    'ev_hp': 0, 'ev_atk': 0, 'ev_def': 0,
                    'ev_spa': 0, 'ev_spd': 0, 'ev_spe': 0,
                    'dex_关都': '', 'dex_城都': '', 'dex_丰缘': '',
                    'dex_神奥': '', 'dex_合众': '', 'dex_卡洛斯': '',
                    'dex_阿罗拉': '', 'dex_伽勒尔': '', 'dex_帕底亚': ''
                }
            web_data.append(info)
            
        # 将网页数据添加到DataFrame
        web_df = pd.DataFrame(web_data)
        df = pd.concat([df, web_df], axis=1)
        
        # 重命名列
        column_rename = {
            'name_cn': '中文名称',
            'name_en': '英文名称',
            'category_cn': '分类（网页）',
            'abilities_normal': '一般特性（网页）',
            'ability_hidden': '隐藏特性（网页）',
            'catch_rate': '捕获率（网页）',
            'base_exp': '基础经验值（网页）',
            'egg_groups': '蛋组（网页）',
            'egg_cycles': '孵化周期（网页）',
            'gender_ratio': '性别比例（网页）',
            'ev_hp': 'HP基础点数（网页）',
            'ev_atk': '攻击基础点数（网页）',
            'ev_def': '防御基础点数（网页）',
            'ev_spa': '特攻基础点数（网页）',
            'ev_spd': '特防基础点数（网页）',
            'ev_spe': '速度基础点数（网页）',
            'dex_关都': '关都图鉴编号（网页）',
            'dex_城都': '城都图鉴编号（网页）',
            'dex_丰缘': '丰缘图鉴编号（网页）',
            'dex_神奥': '神奥图鉴编号（网页）',
            'dex_合众': '合众图鉴编号（网页）',
            'dex_卡洛斯': '卡洛斯图鉴编号（网页）',
            'dex_阿罗拉': '阿罗拉图鉴编号（网页）',
            'dex_伽勒尔': '伽勒尔图鉴编号（网页）',
            'dex_帕底亚': '帕底亚图鉴编号（网页）'
        }
        
        # 重命名列
        df = df.rename(columns=column_rename)
        
        # 确保输出目录存在
        Path(output_file).parent.mkdir(exist_ok=True)
        
        # 保存到Excel
        print(f"保存数据到 {output_file}")
        df.to_excel(output_file, index=False)

def test_scraper():
    """测试爬虫功能"""
    scraper = PokemonWebScraper()
    test_pokemon = "Meowth"  # 测试尼多娜
    print(f"\n测试爬取 {test_pokemon} 的数据...")
    
    info = scraper.scrape_pokemon_info(test_pokemon)
    if info:
        print("\n爬取结果：")
        for key, value in info.items():
            print(f"{key}: {value}")
    else:
        print("爬取失败")

def main():
    # 先测试爬虫
    test_scraper()
    
    # 确认是否继续处理所有数据
    response = input("\n是否继续处理所有宝可梦数据？(y/n): ")
    if response.lower() == 'y':
        processor = PokemonWebInfoProcessor()
        processor.process_web_data('output/pokemon_web_info.xlsx')

if __name__ == "__main__":
    main() 