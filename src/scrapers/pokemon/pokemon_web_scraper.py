import requests
from bs4 import BeautifulSoup, Tag
from typing import Dict, Optional, List
import time
import re
import json
from pathlib import Path

class PokemonWebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        # 获取宝可梦的类型（用于动态生成选择器）
        self.type_class = None
        self.cache_file = Path('pokemon_name_cache.json')
        self.name_cache = self._load_cache()
    
    def _load_cache(self) -> dict:
        """加载名称缓存"""
        if self.cache_file.exists():
            return json.loads(self.cache_file.read_text(encoding='utf-8'))
        return {}
    
    def _get_type_class_and_prefix(self, soup) -> tuple:
        """从网页获取实际的类名和前缀"""
        try:
            # 先找到属性链接
            type_link = soup.find('a', title=lambda x: x and x.endswith('（属性）'))
            if type_link:
                # 获取属性名称（去掉"（属性）"）
                type_name = type_link['title'].replace('（属性）', '')
                # 找到包含此属性的td标签
                type_td = type_link.find_parent('td', class_=lambda x: x and 'roundy' in x)
                if type_td:
                    # 获取完整的类名
                    class_str = ' '.join(type_td['class'])
                    print(f"找到属性: {type_name}, 完整类名: {class_str}")
                    return class_str, type_name
        except Exception as e:
            print(f"获取类名失败: {e}")
        return None, None

    def scrape_pokemon_info(self, name_en: str, max_retries: int = 3) -> Optional[Dict]:
        """爬取宝可梦详细信息"""
        url = f"https://wiki.52poke.com/wiki/{name_en}"
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)
                
                # 保存网页内容到文件，方便调试
                # with open('datadebug_page.html', 'w', encoding='utf-8') as f:
                #     f.write(response.text)
                # print(f"\n网页内容已保存到 debug_page.html")
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 打印页面标题，确认是否正确访问
                print(f"正在爬取: {soup.title.text}")
                
                # 获取实际的类名
                class_str, type_name = self._get_type_class_and_prefix(soup)
                if class_str:
                    self.type_class = type_name
                    print(f"宝可梦类型: {type_name}")
                    # 使用动态类名查找元素
                    poison_cells = soup.find_all('td', class_=class_str)
                
                # 使用动态类名查找元素
                # base_tables = soup.find_all('table', class_='roundy bgwhite fulltable')
                
                # print(f"找到的毒属性单元格: {poison_cells}")    
                # 初始化数据字典
                data = {
                    'category_cn': self._get_category(soup),
                    'abilities_normal': self._get_abilities(poison_cells),
                    'ability_hidden': self._get_hidden_ability(soup),
                    'catch_rate': self._get_catch_rate(poison_cells),
                    'base_exp': self._get_base_exp(poison_cells),
                    'ev_yield': self._get_ev_yield(soup),
                    'egg_groups': self._get_egg_groups(poison_cells),
                    'egg_cycles': self._get_egg_cycles(poison_cells),
                    'gender_ratio': self._get_gender_ratio(soup),
                    'pokedex_numbers': self._get_pokedex_numbers(soup)
                }
                
                name_cn = self.name_cache[name_en]
                # 打印调试信息
                print("\n爬取结果：")
                print(f"中文名称: {name_cn if 'name_cn' in locals() else ''}")
                print(f"英文名称: {name_en}")
                print(f"分类（网页）: {data['category_cn']}")
                print(f"一般特性（网页）: {data['abilities_normal']}")
                print(f"隐藏特性（网页）: {data['ability_hidden']}")
                print(f"捕获率（网页）: {data['catch_rate']}")
                print(f"基础经验值（网页）: {data['base_exp']}")
                print(f"蛋组（网页）: {data['egg_groups']}")
                print(f"孵化周期（网页）: {data['egg_cycles']}")
                print(f"性别比例（网页）: {data['gender_ratio']}")
                
                # 打印基础点数
                ev_data = data['ev_yield']
                print(f"HP基础点数（网页）: {ev_data['HP']}")
                print(f"攻击基础点数（网页）: {ev_data['攻击']}")
                print(f"防御基础点数（网页）: {ev_data['防御']}")
                print(f"特攻基础点数（网页）: {ev_data['特攻']}")
                print(f"特防基础点数（网页）: {ev_data['特防']}")
                print(f"速度基础点数（网页）: {ev_data['速度']}")
                
                # 打印图鉴编号
                dex_data = data['pokedex_numbers']
                print(f"关都图鉴编号（网页）: {dex_data.get('关都', '')}")
                print(f"城都图鉴编号（网页）: {dex_data.get('城都', '')}")
                print(f"丰缘图鉴编号（网页）: {dex_data.get('丰缘', '')}")
                print(f"神奥图鉴编号（网页）: {dex_data.get('神奥', '')}")
                print(f"合众图鉴编号（网页）: {dex_data.get('合众', '')}")
                print(f"卡洛斯图鉴编号（网页）: {dex_data.get('卡洛斯', '')}")
                print(f"阿罗拉图鉴编号（网页）: {dex_data.get('阿罗拉', '')}")
                print(f"伽勒尔图鉴编号（网页）: {dex_data.get('伽勒尔', '')}")
                print(f"帕底亚图鉴编号（网页）: {dex_data.get('帕底亚', '')}")
                
                time.sleep(1)  # 请求间隔
                return data
                
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"获取{name_en}的详细信息失败: {e}")
                time.sleep(2)
        
        return None

    def _get_category(self, soup) -> str:
        """获取宝可梦分类（如"毒针宝可梦"）"""
        try:
            category = soup.select_one('a[href*="Category:"][title*="宝可梦"]')
            return category.text.replace('宝可梦', '') if category else ""
        except:
            return ""

    def _get_abilities(self, poison_cells: List[Tag]) -> str:
        """获取普通特性"""
        try:
            # 找到宽度为50%的单元格
            for cell in poison_cells:
                if cell.get('width') == '50%' and not ('隐藏特性' in cell.text or '隱藏特性' in cell.text):
                    # 找到所有特性链接
                    ability_links = cell.find_all('a', title=lambda x: x and x.endswith('（特性）'))
                    if ability_links:
                        # 返回所有特性，用"或"连接，去掉"（特性）"后缀
                        abilities = [link['title'].replace('（特性）', '') for link in ability_links]
                        return ' 或 '.join(abilities)
        except Exception as e:
            print(f"获取普通特性失败: {e}")
        return ""

    def _get_hidden_ability(self, soup) -> str:
        """获取隐藏特性"""
        try:
            # 找到包含"隐藏特性"文本的small标签
            hidden_tag = soup.find('small', string=lambda x: '隱藏特性' in str(x))
            print(f"获取隐藏特性标签: {hidden_tag}")
            if hidden_tag:
                # 获取同一单元格中的特性链接
                ability_link = hidden_tag.find_previous('a')
                print(f"获取特性链接: {ability_link}")
                if ability_link:
                    return ability_link.text.strip()
            # else:
            #     # 尝试其他方法
            #     ability_cell = soup.find('td', width='50%', class_='roundy bl-毒 bw-1')
            #     if ability_cell and ('隱藏特性' in ability_cell.text or '隐藏特性' in ability_cell.text):
            #         ability_link = ability_cell.find('a')
            #         print(f"备选方法获取特性链接: {ability_link}")
            #         if ability_link:
            #             return ability_link.text.strip()
        except Exception as e:
            print(f"获取隐藏特性失败: {e}")
            print(f"页面内容: {hidden_tag.parent.text if 'hidden_tag' in locals() else 'None'}")
        return ""

    def _get_catch_rate(self, poison_cells: List[Tag]) -> str:
        """获取捕获率（使用预先找到的单元格）"""
        try:
            for cell in poison_cells:
                explain_span = cell.find('span', class_='explain')
                if explain_span and '%' in explain_span.text:
                    return explain_span.text.strip()
        except Exception as e:
            print(f"捕获率提取错误: {e}")
        return ""

    def _get_base_exp(self, poison_cells: List[Tag]) -> str:
        """获取基础经验值"""
        try:
            for cell in poison_cells:
                if '基础经验值' in cell.text:
                    exp_text = cell.text.strip()
                    # 提取第一个数字
                    match = re.search(r'(\d+)', exp_text)
                    if match:
                        return match.group(1)
        except Exception as e:
            print(f"获取基础经验值失败: {e}")
        return ""

    def _get_ev_yield(self, soup: BeautifulSoup) -> Dict[str, int]:
        """获取基础点数（使用预先找到的表格）"""
        ev_stats = {'HP': 0, '攻击': 0, '防御': 0, '特攻': 0, '特防': 0, '速度': 0}
        try:
            # 找到包含"取得基础点数"的表格
            ev_section = soup.find('b', string=lambda x: '取得基础点数' in str(x))
            if ev_section:
                # 找到包含基础点数的表格
                ev_table = ev_section.find_parent('td').find('table', class_='roundy bgwhite fulltable')
                if ev_table:
                    # 直接查找每个属性的单元格
                    stat_cells = {
                        'HP': ev_table.find('td', class_='roundy bw-1 bgl-HP bd-HP'),
                        '攻击': ev_table.find('td', class_='roundy bw-1 bgl-攻击 bd-攻击'),
                        '防御': ev_table.find('td', class_='roundy bw-1 bgl-防御 bd-防御'),
                        '特攻': ev_table.find('td', class_='roundy bw-1 bgl-特攻 bd-特攻'),
                        '特防': ev_table.find('td', class_='roundy bw-1 bgl-特防 bd-特防'),
                        '速度': ev_table.find('td', class_='roundy bw-1 bgl-速度 bd-速度')
                    }
                    
                    # 获取每个属性的值
                    for stat, cell in stat_cells.items():
                        if cell:
                            # 获取最后一个数字（基础点数值）
                            text = cell.get_text(strip=True)
                            numbers = re.findall(r'\d+', text)
                            if numbers:
                                ev_stats[stat] = int(numbers[-1])
                    
                    print(f"基础点数单元格内容: {[f'{stat}: {cell.text}' for stat, cell in stat_cells.items() if cell]}")
        except Exception as e:
            print(f"获取基础点数失败: {e}")
            print(f"表格内容: {ev_section.text if 'ev_section' in locals() else 'None'}")
        return ev_stats

    def _get_egg_groups(self, poison_cells: List[Tag]) -> str:
        """获取蛋组"""
        try:
            for cell in poison_cells:
                if '蛋组' in cell.text:
                    return cell.text.strip()
        except:
            return ""

    def _get_egg_cycles(self, poison_cells: List[Tag]) -> str:
        """获取孵化周期和步数"""
        try:
            for cell in poison_cells:
                if '孵化周期' in cell.text:
                    # 提取数字部分
                    numbers = re.findall(r'\d+', cell.text)
                    if len(numbers) >= 2:
                        # 返回 "20周期（5140步）" 格式
                        return f"{numbers[0]}周期（{numbers[1]}步）"
                    elif numbers:
                        return numbers[0]  # 至少返回周期数
            print(f"孵化周期单元格内容: {[cell.text for cell in poison_cells]}")  # 调试信息
        except Exception as e:
            print(f"获取孵化周期失败: {e}")
        return ""

    def _get_gender_ratio(self, soup) -> str:
        """获取性别比例"""
        try:
            # 找到性别比例表格
            ratio_cell = soup.find('span', style='color:#FF6060;')
            if ratio_cell:
                return ratio_cell.text.strip()
        except Exception as e:
            print(f"获取性别比例失败: {e}")
        return ""

    def _get_pokedex_numbers(self, soup) -> Dict[str, str]:
        """获取各地区图鉴编号"""
        numbers = {}
        try:
            # 找到所有地区编号单元格
            region_cells = soup.find_all('td', class_=lambda x: x and x.startswith('bgl-') and 'roundyleft' in x)
            for cell in region_cells:
                region = cell.find('b').text
                if region in ['关都', '城都', '丰缘', '神奥', '合众', '卡洛斯', '阿罗拉', '伽勒尔', '帕底亚']:
                    number = cell.find_next('td', class_=lambda x: x and x.startswith('bd-'))
                    if number and '#' in number.text:
                        numbers[region] = number.text.split('#')[1].strip()
        except:
            pass
        return numbers