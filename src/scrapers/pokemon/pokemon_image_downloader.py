import time
import requests
import pandas as pd
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
from tqdm import tqdm

class PokemonImageDownloader:
    def __init__(self):
        self.base_url = "https://dex.pokemonshowdown.com/pokemon/{name_en}"
        self.image_dir = Path('images')
        self.image_dir.mkdir(parents=True, exist_ok=True)
        
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

    def download_image(self, name_en: str) -> Optional[str]:
        """下载宝可梦图片"""
        # 构建文件路径
        file_path = self.image_dir / f"{name_en}.png"
        
        # 如果图片已存在，直接返回路径
        if file_path.exists():
            return str(file_path)

        try:
            # 访问页面
            url = self.base_url.format(name_en=name_en.lower())
            self.driver.get(url)
            
            # 等待页面加载完成
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
            
            # 获取渲染后的页面源码
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            img = None
            
            # 方法1: 通过类型标签查找
            if not img:
                print("尝试通过类型标签查找图片...")
                type_dl = soup.find('dl', class_='typeentry')
                if type_dl:
                    img = type_dl.find_previous_sibling('img', class_='sprite')
                    if img:
                        print("通过类型标签找到图片")
            
            # 方法2: 通过标题h1标签查找
            if not img:
                print("尝试通过标题查找图片...")
                h1 = soup.find('h1', class_="subtle")
                if h1:
                    img = h1.find_next_sibling('img', class_='sprite')
                    if img:
                        print("通过标题找到图片")
            
            # 方法3: 通过 warning div 查找
            if not img:
                print("尝试通过 warning div 查找图片...")
                warning_div = soup.find('div', class_='warning')
                if warning_div:
                    img = warning_div.find_next_sibling('img', class_='sprite')
                    if img:
                        print("通过 warning div 找到图片")
            
            # 方法4: 直接查找
            if not img:
                print("尝试直接查找 sprite 图片...")
                img = soup.find('img', class_='sprite')
                if img:
                    print("直接找到 sprite 图片")
            
            if img and img.get('src'):
                img_url = img['src']
                if not img_url.startswith('http'):
                    img_url = "https:" + img_url
                
                # 下载图片
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"成功下载图片: {name_en}")
                    return str(file_path)
                else:
                    print(f"下载图片失败: HTTP {response.status_code}")
                    print(f"图片URL: {img_url}")
            else:
                print(f"未找到图片元素: {name_en}")
                print(f"页面URL: {url}")
            
        except Exception as e:
            print(f"下载图片失败 {name_en}: {e}")
        return None

    def batch_download_from_excel(self, excel_file: str):
        """从Excel文件批量下载图片并更新表格"""
        try:
            # 读取Excel文件
            print(f"读取Excel文件: {excel_file}")
            df = pd.read_excel(excel_file)
            
            # 获取英文名称列
            if '英文名称' in df.columns:
                name_column = '英文名称'
            else:
                raise ValueError("找不到英文名称列")
            
            # 添加图鉴路径列
            if '图鉴路径' not in df.columns:
                df['图鉴路径'] = None
            
            # 获取所有英文名称
            pokemon_names = df[name_column].dropna().unique().tolist()
            print(f"找到 {len(pokemon_names)} 个宝可梦")
            
            # 创建进度条
            success_count = 0
            failed_names = []
            
            for pokemon in tqdm(pokemon_names, desc="下载图片"):
                # 检查是否已存在图片
                file_path = self.image_dir / f"{pokemon}.png"
                if file_path.exists():
                    # 更新表格中对应的行
                    df.loc[df[name_column] == pokemon, '图鉴路径'] = str(file_path)
                    success_count += 1
                    continue
                
                # 如果不存在，下载图片
                result = self.download_image(pokemon)
                if result:
                    # 更新表格中对应的行
                    df.loc[df[name_column] == pokemon, '图鉴路径'] = result
                    success_count += 1
                else:
                    failed_names.append(pokemon)
                time.sleep(0.5)  # 添加短暂延迟
            
            # 保存更新后的Excel文件
            print("\n保存更新后的Excel文件...")
            df.to_excel(excel_file, index=False)
            
            # 打印统计信息
            print(f"\n下载完成!")
            print(f"成功: {success_count}")
            print(f"失败: {len(failed_names)}")
            if failed_names:
                print("失败的宝可梦:")
                for name in failed_names:
                    print(f"- {name}")
                
        except Exception as e:
            print(f"批量下载出错: {e}")

    def __del__(self):
        """清理资源"""
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    downloader = PokemonImageDownloader()
    
    # 从Excel文件批量下载
    excel_file = 'output/pokemon_data.xlsx'
    print("开始批量下载...")
    downloader.batch_download_from_excel(excel_file)
    
    # 清理资源
    downloader.__del__()

if __name__ == "__main__":
    main() 