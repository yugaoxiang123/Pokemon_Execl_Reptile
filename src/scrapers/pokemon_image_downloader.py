import time
import requests
from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup

class PokemonImageDownloader:
    def __init__(self):
        self.base_url = "https://wiki.52poke.com/wiki/{name_en}"
        self.image_dir = Path('images')
        self.image_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def download_image(self, name_en: str) -> Optional[str]:
        """下载宝可梦图片"""
        # 构建文件路径
        file_path = self.image_dir / f"{name_en}.png"
        if file_path.exists():
            return str(file_path)

        try:
            # 访问图片页面
            url = self.base_url.format(name_en=name_en)
            response = self.session.get(url)
            
            # 从页面中提取实际图片URL
            soup = BeautifulSoup(response.text, 'html.parser')
            img_element = soup.select_one('td .image img')
            if not img_element:
                return None
                
            # 获取原始图片URL（不要缩略图）
            img_url = img_element['data-srcset'].split()[-2]
            if not img_url.startswith('http'):
                img_url = "https:" + img_url
            
            # 下载图片
            img_response = self.session.get(img_url, stream=True)
            if img_response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return str(file_path)
            
            time.sleep(1)  # 请求间隔
            
        except Exception as e:
            print(f"下载图片失败 {name_en}: {e}")
            return None 