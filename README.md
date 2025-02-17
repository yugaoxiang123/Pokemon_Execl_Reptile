# Pokemon Data Parser

这是一个用于解析和处理宝可梦数据的Python项目。项目可以从多个数据源获取宝可梦相关信息，并生成结构化的Excel数据表。

## 项目结构 

```
pokemon-parser/
├── README.md
├── TABTOY_GUIDE.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── ability_description_scraper.py
│   │   ├── item_description_scraper.py
│   │   ├── move_description_scraper.py
│   │   ├── pokemon_evolution_scraper.py
│   │   ├── pokemon_image_downloader.py
│   │   ├── pokemon_levelup_scraper.py
│   │   ├── pokemon_web_info.py
│   │   ├── pokemon_web_scraper.py
│   │   └── skill_gif_scraper.py
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── ability_to_excel.py
│   │   ├── assistant_excel_merger.py
│   │   ├── evolution_data_fixer.py
│   │   ├── excel_column_merger.py
│   │   ├── item_to_excel.py
│   │   ├── move_format_converter.py
│   │   ├── move_to_excel.py
│   │   ├── null_value_fixer.py
│   │   ├── pokemon_form_data_fixer.py
│   │   └── pokemon_to_excel.py
│   └── utils/
│       ├── __init__.py
│       └── translations.py
├── data/
│   ├── abilities.ts
│   ├── items.ts
│   ├── moves.ts
│   └── pokedex.ts
├── json/
│   ├── ability_descriptions.json
│   ├── ability_translations.json
│   ├── item_descriptions.json
│   ├── item_translations.json
│   ├── move_descriptions.json
│   ├── move_translations.json
│   └── pokemon_name_cache.json
├── output/
│   ├── ability_data.xlsx
│   ├── item_data.xlsx
│   ├── move_data.xlsx
│   ├── pokemon_data.xlsx
│   └── pokemon_web_info.xlsx
└── images/
    ├── pokemon_images/
    └── pokemon_gifs/
```

## 模块说明

### 爬虫模块 (src/scrapers/)

- `pokemon_web_scraper.py`: 从神奇宝贝百科网站爬取宝可梦基础信息
- `pokemon_image_downloader.py`: 下载宝可梦图片
- `pokemon_levelup_scraper.py`: 爬取宝可梦升级技能信息
- `pokemon_evolution_scraper.py`: 爬取宝可梦进化信息
- `skill_gif_scraper.py`: 爬取宝可梦技能GIF动画
- `ability_description_scraper.py`: 爬取特性描述信息
- `item_description_scraper.py`: 爬取道具描述信息
- `move_description_scraper.py`: 爬取技能描述信息
- `pokemon_web_info.py`: 爬取宝可梦额外信息（如基础点数、蛋组等）

### 数据处理模块 (src/processors/)

- `pokemon_to_excel.py`: 处理宝可梦数据并生成Excel表格
- `ability_to_excel.py`: 处理特性数据并生成Excel表格
- `item_to_excel.py`: 处理道具数据并生成Excel表格
- `move_to_excel.py`: 处理技能数据并生成Excel表格
- `move_format_converter.py`: 转换技能数据为JSON格式
- `pokemon_form_data_fixer.py`: 修复特殊形态宝可梦的数据
- `evolution_data_fixer.py`: 修复进化数据的空值
- `null_value_fixer.py`: 处理表格中的空值
- `excel_column_merger.py`: 合并不同Excel表格的列数据
- `assistant_excel_merger.py`: 合并同一Excel文件内不同表的数据

### 工具模块 (src/utils/)

- `translations.py`: 包含各种翻译映射（形态、属性等）

### 数据文件

- `data/abilities.ts`: 特性数据源文件
- `data/items.ts`: 道具数据源文件
- `data/moves.ts`: 技能数据源文件
- `data/pokedex.ts`: 宝可梦图鉴数据源文件

### 缓存文件 (json/)

- `ability_descriptions.json`: 特性描述缓存
- `ability_translations.json`: 特性翻译缓存
- `item_descriptions.json`: 道具描述缓存
- `item_translations.json`: 道具翻译缓存
- `move_descriptions.json`: 技能描述缓存
- `move_translations.json`: 技能翻译缓存
- `pokemon_name_cache.json`: 宝可梦名称缓存

## 功能特性

1. 数据解析与爬取
   - 解析宝可梦基础数据（属性、能力值等）
   - 爬取升级技能和进化信息
   - 下载技能GIF动画
   - 获取特性、道具和技能描述

2. 数据处理
   - 特殊形态数据修复
   - 进化数据空值处理
   - 表格列数据合并
   - 同一文件内表格合并
   - 技能数据JSON格式化
   - 空值统一处理
   - 自动列宽调整

3. 数据导出
   - 生成结构化Excel表格
   - 支持多表数据
   - 支持图片和GIF导出
   - 支持TabToy导出JSON

## 使用方法

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行爬虫：
   ```bash
   python src/scrapers/skill_gif_scraper.py  # 爬取技能GIF
   python src/scrapers/pokemon_evolution_scraper.py  # 爬取进化信息
   ```

3. 处理数据：
   ```bash
   python src/processors/move_format_converter.py  # 转换技能格式
   python src/processors/null_value_fixer.py  # 处理空值
   ```

4. 导出数据：
   - 参考 TABTOY_GUIDE.md 使用 TabToy 导出数据
