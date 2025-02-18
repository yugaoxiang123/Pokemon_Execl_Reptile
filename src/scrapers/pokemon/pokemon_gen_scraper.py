import re
import json
from pathlib import Path
from typing import Optional, List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class PokemonGenScraper:
    def __init__(self):
        self.base_url = "https://dex.pokemonshowdown.com/pokemon/"
        self.output_dir = Path('json')
        self.output_dir.mkdir(exist_ok=True)
        # 查找所有世代的标题
        self.gen_pattern = re.compile(r'Generation ([1-9])')
        # 设置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # 初始化WebDriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # 设置等待时间
        self.wait = WebDriverWait(self.driver, 10)

    def _get_page_content(self) -> str:
        """获取页面内容"""
        try:
            # 访问页面
            url = self.base_url
            self.driver.get(url)
            
            # 等待页面初始加载完成
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "utilichart"))
            )

            # 获取初始高度
            initial_height = self.driver.execute_script("return document.querySelector('.utilichart').style.height")
            target_height = int(initial_height.replace('px', ''))
            current_scroll = 0
            
            print(f"总高度: {target_height}px")
            print("开始滚动页面加载所有内容...")
            
            while current_scroll < target_height:
                # 滚动一定距离
                current_scroll += 1000
                self.driver.execute_script(f"document.querySelector('.pfx-panel').scrollTop = {current_scroll};")
                
                # 等待新内容加载
                time.sleep(0.5)  # 短暂等待
                
                # 每滚动10次输出一次进度
                if current_scroll % 10000 == 0:
                    print(f"已滚动至 {current_scroll}px / {target_height}px")

            print("页面内容加载完成")
            time.sleep(2)  # 最后等待一下确保所有内容都加载完成
            
            # 获取渲染后的页面源码
            return BeautifulSoup(self.driver.page_source, 'html.parser')
            
        except Exception as e:
            print(f"加载页面时出错: {e}")
            import traceback
            print(traceback.format_exc())
            return None
    
    def _parse_gen_section(self, gen_section) -> List[str]:
        """解析每个世代部分的宝可梦"""
        pokemons = []
        # 找到该世代后的所有 li.result 元素，直到下一个世代的标题
        current = gen_section.find_next_sibling('li', class_='result')
        
        while current:
            # 检查是否到达下一个世代
            h3_tag = current.find('h3')
            if h3_tag and self.gen_pattern.match(h3_tag.get_text()):
                break
            
            # 获取宝可梦名称
            pokemon_name = current.find('span', class_='pokemonnamecol')
            if pokemon_name:
                name = pokemon_name.get_text().strip()
                # # 移除可能的 -Mega, -Gmax 等后缀
                # name = name.split('-')[0]
                if name and name not in pokemons:
                    pokemons.append(name)
                
            current = current.find_next_sibling('li', class_='result')
        
        return pokemons
        
    def scrape(self) -> dict[int, list[str]]:
        """爬取宝可梦世代数据"""
        print("开始爬取宝可梦数据...")
        soup = self._get_page_content()
        if not soup:
            print("获取页面内容失败")
            return {}
        
        pokemons_by_gen = {}
        
        # 查找所有世代的标题
        gen_headers = soup.find_all('h3')
        for header in gen_headers:
            if self.gen_pattern.match(header.get_text()):
                gen_num = int(header.get_text()[-1])
                print(f"处理第{gen_num}世代...")
                
                # 获取该世代的所有宝可梦
                pokemons = self._parse_gen_section(header.parent)
                if pokemons:
                    pokemons_by_gen[gen_num] = pokemons
                    print(f"第{gen_num}世代找到 {len(pokemons)} 个宝可梦")
        
        # 保存数据
        output_file = self.output_dir / 'pokemons_by_gen.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(pokemons_by_gen, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {output_file}")
        
        return pokemons_by_gen

    def __del__(self):
        """确保关闭浏览器"""
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    scraper = PokemonGenScraper()
    pokemons_by_gen = scraper.scrape()
    
    # 打印示例数据
    print("\n示例数据:")
    for gen, pokemons in pokemons_by_gen.items():
        print(f"\n第{gen}世代的前5个宝可梦:")
        print(pokemons[:5])
if __name__ == "__main__":
    main() 