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
import requests
from openpyxl.utils import get_column_letter

class SkillGifScraper:
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

    def get_gif_urls(self, name_en: str) -> Dict[str, str]:
        """获取宝可梦的GIF图片URL"""
        try:
            url = self.base_url.format(name_en=name_en.lower())
            self.driver.get(url)
            
            # 等待页面加载完成
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
            
            # 找到并点击Flavor按钮
            flavor_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[value='details']"))
            )
            flavor_button.click()
            
            # 等待GIF图片加载
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.sprites img"))
            )
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # 获取所有GIF图片URL
            gif_urls = {}
            sprite_tables = soup.find_all('table', class_='sprites')
            
            for table in sprite_tables:
                images = table.find_all('img')
                for img in images:
                    src = img.get('src', '')
                    if src and 'sprites/ani' in src:  # 确保是动画精灵图
                        # 根据URL确定图片类型
                        if 'ani-back-shiny' in src:  # 背面闪光
                            gif_urls['shiny_back'] = src
                        elif 'ani-back' in src:      # 背面普通
                            gif_urls['normal_back'] = src
                        elif 'ani-shiny' in src:     # 正面闪光
                            gif_urls['shiny_front'] = src
                        elif 'ani' in src:           # 正面普通
                            gif_urls['normal_front'] = src
            
            return gif_urls
            
        except Exception as e:
            print(f"获取{name_en}的GIF图片失败: {e}")
            return {}

    def download_gifs(self, name_en: str, gif_urls: Dict[str, str]) -> str:
        """下载GIF图片到本地"""
        try:
            # 创建宝可梦专属文件夹
            pokemon_dir = Path('pokemon_gifs') / name_en
            pokemon_dir.mkdir(parents=True, exist_ok=True)
            
            # 下载所有GIF
            for gif_type, url in gif_urls.items():
                if not url.startswith('http'):
                    url = f"https:{url}"
                
                # 构建文件名
                file_name = f"{gif_type}.gif"
                file_path = pokemon_dir / file_name
                
                # 下载文件
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"已下载: {file_path}")
                else:
                    print(f"下载失败: {url}")
            
            return str(pokemon_dir)
            
        except Exception as e:
            print(f"下载GIF失败 {name_en}: {e}")
            return ""

    def update_excel_with_gif_urls(self, excel_file: str):
        """更新Excel文件，添加GIF图片URL和本地路径"""
        try:
            print(f"读取Excel文件: {excel_file}")
            # 读取现有的Excel文件
            with pd.ExcelFile(excel_file) as xls:
                df = pd.read_excel(xls, sheet_name='Sheet1')
            
            # 获取所有宝可梦名称
            pokemon_names = df['英文名称'].dropna().unique().tolist()
            print(f"找到 {len(pokemon_names)} 个宝可梦")
            
            # 获取图鉴路径列的索引
            image_path_idx = df.columns.get_loc('图鉴路径')
            
            # 创建GIF路径列
            if 'GIF路径' not in df.columns:
                df.insert(image_path_idx + 1, 'GIF路径', None)
            
            # 获取每个宝可梦的GIF URL并下载
            for pokemon in tqdm(pokemon_names, desc="获取和下载GIF图片"):
                gif_urls = self.get_gif_urls(pokemon)
                if gif_urls:
                    # 下载GIF并获取本地路径
                    local_path = self.download_gifs(pokemon, gif_urls)
                    
                    # 更新DataFrame
                    mask = df['英文名称'] == pokemon
                    if local_path:
                        df.loc[mask, 'GIF路径'] = local_path
                time.sleep(0.5)
            
            # 保存更新后的数据
            with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
                
                # 调整列宽
                worksheet = writer.sheets['Sheet1']
                for idx, col in enumerate(df.columns, 1):
                    if col == 'GIF路径':
                        worksheet.column_dimensions[get_column_letter(idx)].width = 30
            
            print("\nGIF图片和路径已更新到Sheet1表")
            
        except Exception as e:
            print(f"更新Excel文件失败: {e}")

    def __del__(self):
        """清理资源"""
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    scraper = SkillGifScraper()
    excel_file = 'output/pokemon_data.xlsx'
    print("开始获取宝可梦gif信息...")
    scraper.update_excel_with_gif_urls(excel_file)
    scraper.__del__()

if __name__ == "__main__":
    main() 