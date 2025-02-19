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
│   │   ├── pokemon/
│   │   │   ├── pokemon_web_scraper.py      # 宝可梦基础信息爬虫
│   │   │   ├── pokemon_image_downloader.py  # 宝可梦图片下载器
│   │   │   ├── pokemon_levelup_scraper.py   # 升级技能爬虫
│   │   │   ├── pokemon_evolution_scraper.py # 进化信息爬虫
│   │   │   ├── pokemon_web_info.py         # 额外信息爬虫
│   │   │   └── skill_gif_scraper.py        # 技能GIF爬虫
│   │   ├── ability/
│   │   │   └── ability_description_scraper.py # 特性描述爬虫
│   │   ├── item/
│   │   │   └── item_description_scraper.py    # 道具描述爬虫
│   │   └── move/
│   │       └── move_description_scraper.py     # 技能描述爬虫
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── pokemon/
│   │   │   ├── pokemon_to_excel.py          # 宝可梦数据处理
│   │   │   ├── pokemon_form_data_fixer.py   # 形态数据修复
│   │   │   └── evolution_data_fixer.py      # 进化数据修复
│   │   ├── ability/
│   │   │   └── ability_to_excel.py          # 特性数据处理
│   │   ├── item/
│   │   │   └── item_to_excel.py             # 道具数据处理
│   │   ├── move/
│   │   │   ├── move_to_excel.py             # 技能数据处理
│   │   │   └── move_format_converter.py      # 技能格式转换
│   │   └── common/
│   │       ├── excel_column_merger.py        # 表格列合并
│   │       ├── assistant_excel_merger.py     # 表格合并
│   │       ├── null_value_fixer.py          # 空值处理
│   │       └── create_index_xlsx.py         # 创建索引表
│   └── utils/
│       ├── __init__.py
│       └── translations.py                   # 翻译映射
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

#### 宝可梦爬虫 (pokemon/)
- `pokemon_web_scraper.py`: 爬取基础信息
- `pokemon_image_downloader.py`: 下载图片
- `pokemon_levelup_scraper.py`: 爬取升级技能
- `pokemon_evolution_scraper.py`: 爬取进化信息
- `pokemon_web_info.py`: 爬取额外信息
- `skill_gif_scraper.py`: 爬取技能GIF

#### 特性爬虫 (ability/)
- `ability_description_scraper.py`: 爬取特性描述

#### 道具爬虫 (item/)
- `item_description_scraper.py`: 爬取道具描述

#### 技能爬虫 (move/)
- `move_description_scraper.py`: 爬取技能描述

### 数据处理模块 (src/processors/)

#### 宝可梦数据处理 (pokemon/)
- `pokemon_to_excel.py`: 处理基础数据
- `pokemon_form_data_fixer.py`: 修复形态数据
- `evolution_data_fixer.py`: 修复进化数据

#### 特性数据处理 (ability/)
- `ability_to_excel.py`: 处理特性数据

#### 道具数据处理 (item/)
- `item_to_excel.py`: 处理道具数据

#### 技能数据处理 (move/)
- `move_to_excel.py`: 处理技能数据
- `move_format_converter.py`: 转换技能格式

#### 通用处理工具 (common/)
- `excel_column_merger.py`: 合并表格列
- `assistant_excel_merger.py`: 合并表格
- `null_value_fixer.py`: 处理空值
- `create_index_xlsx.py`: 创建索引表

### 工具模块 (src/utils/)
- `translations.py`: 翻译映射工具

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

## 功能模块

### 爬虫 (Scrapers)

1. 宝可梦爬虫 (`src/scrapers/pokemon/pokemon_gen_scraper.py`)
   - 从 Pokemon Showdown 爬取各世代宝可梦数据
   - 保存为 `json/pokemons_by_gen.json`

2. 招式爬虫 (`src/scrapers/move/move_gen_scraper.py`)
   - 从 52poke wiki 爬取各世代招式数据
   - 保存为 `json/moves_by_gen.json`

3. 特性爬虫 (`src/scrapers/ability/ability_gen_scraper.py`)
   - 从 52poke wiki 爬取各世代特性数据
   - 保存为 `json/abilities_by_gen.json`

### 数据处理器 (Processors)

1. 宝可梦数据处理器
   - `pokemon_to_excel.py`: 处理基础数据
   - `pokemon_form_filter.py`: 过滤特殊形态
   - `pokemon_gen_extractor.py`: 提取世代信息
   - `pokemon_moves_extractor.py`: 提取技能数据
   - `pokemon_moves_converter.py`: 转换技能格式

2. 道具世代提取器 (`src/processors/item/item_gen_extractor.py`)
   - 从 `data/items.ts` 提取道具的世代信息
   - 更新 Excel 表格中的世代和编号数据

3. 特性世代提取器 (`src/processors/ability/ability_gen_extractor.py`)
   - 处理特性的世代信息
   - 更新相关数据表

4. 招式世代提取器 (`src/processors/move/move_gen_extractor.py`)
   - 处理招式的世代信息
   - 更新相关数据表

## 数据格式

### pokemons_by_gen.json
```json
{
  "1": ["Bulbasaur", "Ivysaur", "Venusaur", ...],
  "2": ["Chikorita", "Bayleef", "Meganium", ...],
  ...
}
```

### moves_by_gen.json
```json
{
  "1": ["Pound", "Karate Chop", "Double Slap", ...],
  "2": ["Move1", "Move2", "Move3", ...],
  ...
}
```

### abilities_by_gen.json
```json
{
  "3": ["Stench", "Drizzle", "Speed Boost", ...],
  "4": ["Ability1", "Ability2", ...],
  ...
}
```

#### pokemon_data.xlsx 字段说明
```
基础信息：
- 编号 (ID)
- 英文名称 (Name)
- 中文名称 (ChineseName)
- 世代 (Gen)
- 属性（中文）(Type)
- 属性（英文）(TypeEn)

能力值：
- 生命值 (HP)
- 攻击 (Attack)
- 防御 (Defense)
- 特攻 (SpAttack)
- 特防 (SpDefense)
- 速度 (Speed)

身体数据：
- 身高 (Height)
- 体重 (Weight)

特性：
- 特性（英文）(SpecialNature)
- 特性（中文）(ChineseSpecialNature)

网页数据：
- 捕获率 (CaptureRate)
- 孵化周期 (HatchCycle)
- 性别比例 (GenderRatio)
- 基础经验值 (BaseExp)

基础点数：
- HP基础点数 (BasePointHP)
- 攻击基础点数 (BasePointAtk)
- 防御基础点数 (BasePointDef)
- 特攻基础点数 (BasePointSpAtk)
- 特防基础点数 (BasePointSpDef)
- 速度基础点数 (BasePointSpeed)

其他信息：
- 进化条件 (EvolutionCondition)
- 升级技能 (LevelUpMoves, JSON格式)
```

### pokemon_moves.json
```json
{
  "Bulbasaur": "初始技能:[Tackle,Growl] 升级技能:[L3:Vine Whip,L6:Growth,L9:Leech Seed]",
  "Ivysaur": "初始技能:[Tackle,Growl] 升级技能:[L3:Vine Whip,L6:Growth,L9:Leech Seed]"
}
```

### type_translations.json
```json
{
  "Normal": "一般",
  "Fire": "火",
  "Water": "水",
  // ... 其他属性翻译
}
```

### 技能数据格式说明
1. 初始技能：宝可梦一级就能学会的技能
2. 升级技能：通过升级学习的技能，格式为"等级:技能名"
3. 示例格式：
   ```
   初始技能:[技能1,技能2] 升级技能:[L4:技能3,L8:技能4]
   ```

### 文件命名规范
- 原始数据：`pokemon_moves.json`
- 格式化后：`pokemon_moves_formatted.json`
- 翻译映射：`type_translations.json`
