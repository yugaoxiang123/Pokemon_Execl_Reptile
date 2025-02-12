"""宝可梦形态翻译数据"""

# 特殊形态的中文翻译对照
FORM_TRANSLATIONS = {
    # 基础形态
    'Mega': '超级',
    'Gmax': '超极巨化',
    'Alola': '阿罗拉',
    'Galar': '伽勒尔',
    'Paldea': '帕底亚',
    'Hisui': '洗翠',
    'X': 'X',
    'Y': 'Y',
    
    # 性别形态
    'M': '♂',
    'F': '♀',
    
    # 天气形态
    'Sunny': '晴天形态',
    'Rainy': '雨天形态',
    'Snowy': '雪云形态',
    
    # 特殊战斗形态
    'Combat': '战斗',
    'Blaze': '火焰',
    'Aqua': '水流',
    'Attack': '攻击形态',
    'Defense': '防御形态',
    'Speed': '速度形态',
    'Origin': '原始形态',
    'Primal': '原始形态',
    'Sky': '天空形态',
    
    # 特殊外形
    'Sandy': '砂土蝶',
    'Trash': '垃圾蝶',
    'Sunshine': '阳光形态',
    'School': '鱼群形态',
    'Spiky-eared': '刺刺耳',
    
    # 洛托姆形态
    'Heat': '加热',
    'Wash': '清洗',
    'Frost': '结冰',
    'Fan': '旋转',
    'Mow': '割草',
    
    # 大小形态
    'Small': '小型',
    'Large': '大型',
    'Super': '特大',
    
    # 时间形态
    'Midnight': '黑夜形态',
    'Dusk': '黄昏形态',
    
    # 花舞鸟形态
    'Pom-Pom': '啪滋啪滋风格',
    'Pa\'u': '呼拉呼拉风格',
    'Sensu': '轻盈轻盈风格',
    
    # 条纹形态
    'Blue-Striped': '蓝条纹',
    'White-Striped': '白条纹',
    
    # 太乐巴戈斯形态
    'Terastal': '太晶化',
    'Stellar': '星晶化',
    'Tera': '太晶',
    
    # 特殊状态
    'Crowned': '王者',
    'Eternamax': '无极巨化',
    'Rapid-Strike': '急流',
    'Bloodmoon': '血月',
    'Therian': '灵兽',
    'Gulping': '吞食',
    'Gorging': '大吃',
    'Antique': '古董',
    'Low-Key': '低调',
    'Masterpiece': '杰作',
    'Artisan': '工匠',
    'Roaming': '流浪',
    'Hero': '英雄',
    'Four': '四只',
    'Three-Segment': '三节',
    
    # 厄鬼椪形态
    'Wellspring': '水泉',
    'Hearthflame': '炉火',
    'Cornerstone': '基石',
    'Teal': '青色',
    
    # 奈克洛兹玛形态
    'Dusk-Mane': '黄昏之鬃',
    'Dawn-Wings': '拂晓之翼',
    
    # 颜色形态
    'Blue': '蓝色',
    'Yellow': '黄色',
    'White': '白色',
    
    # 霸主形态
    'Totem': '霸主',
    
    # 特殊形态
    'Fancy': '花纹',
    'Pokeball': '精灵球花纹',
    'Eternal': '永恒',
    'Blade': '剑形态',
}

# 特殊处理某些完整形态名称
SPECIAL_FORM_NAMES = {
    # 皮卡丘系列
    'Pikachu-Cosplay': '换装皮卡丘',
    'Pikachu-Rock-Star': '摇滚巨星皮卡丘',
    'Pikachu-Belle': '贵妇皮卡丘',
    'Pikachu-Pop-Star': '偶像皮卡丘',
    'Pikachu-PhD': '博士皮卡丘',
    'Pikachu-Libre': '面具摔角手皮卡丘',
    'Pikachu-Partner': '搭档皮卡丘',
    
    # 帕底亚肯泰罗
    'Tauros-Paldea-Combat': '帕底亚肯泰罗（战斗型）',
    'Tauros-Paldea-Blaze': '帕底亚肯泰罗（火焰型）',
    'Tauros-Paldea-Aqua': '帕底亚肯泰罗（水流型）',
    
    # 特殊形态
    'Nidoran-M': '尼多朗',
    'Nidoran-F': '尼多兰',
    'Deoxys-Attack': '代欧奇希斯（攻击形态）',
    'Deoxys-Defense': '代欧奇希斯（防御形态）',
    'Deoxys-Speed': '代欧奇希斯（速度形态）',
    'Wormadam-Sandy': '结草贵妇（砂土蝶）',
    'Wormadam-Trash': '结草贵妇（垃圾蝶）',
    'Giratina-Origin': '骑拉帝纳（原始形态）',
    'Shaymin-Sky': '谢米（天空形态）',
    'Wishiwashi-School': '弱丁鱼（鱼群形态）',
    
    # 阿尔宙斯属性形态
    'Arceus-Bug': '阿尔宙斯（虫属性）',
    'Arceus-Dark': '阿尔宙斯（恶属性）',
    'Arceus-Dragon': '阿尔宙斯（龙属性）',
    'Arceus-Electric': '阿尔宙斯（电属性）',
    'Arceus-Fairy': '阿尔宙斯（妖精属性）',
    'Arceus-Fighting': '阿尔宙斯（格斗属性）',
    'Arceus-Fire': '阿尔宙斯（火属性）',
    'Arceus-Flying': '阿尔宙斯（飞行属性）',
    'Arceus-Ghost': '阿尔宙斯（幽灵属性）',
    'Arceus-Grass': '阿尔宙斯（草属性）',
    'Arceus-Ground': '阿尔宙斯（地面属性）',
    'Arceus-Ice': '阿尔宙斯（冰属性）',
    'Arceus-Poison': '阿尔宙斯（毒属性）',
    'Arceus-Psychic': '阿尔宙斯（超能力属性）',
    'Arceus-Rock': '阿尔宙斯（岩石属性）',
    'Arceus-Steel': '阿尔宙斯（钢属性）',
    'Arceus-Water': '阿尔宙斯（水属性）',
    
    # 银伴战兽属性形态
    'Silvally-Bug': '银伴战兽（虫属性）',
    'Silvally-Dark': '银伴战兽（恶属性）',
    'Silvally-Dragon': '银伴战兽（龙属性）',
    'Silvally-Electric': '银伴战兽（电属性）',
    'Silvally-Fairy': '银伴战兽（妖精属性）',
    'Silvally-Fighting': '银伴战兽（格斗属性）',
    'Silvally-Fire': '银伴战兽（火属性）',
    'Silvally-Flying': '银伴战兽（飞行属性）',
    'Silvally-Ghost': '银伴战兽（幽灵属性）',
    'Silvally-Grass': '银伴战兽（草属性）',
    'Silvally-Ground': '银伴战兽（地面属性）',
    'Silvally-Ice': '银伴战兽（冰属性）',
    'Silvally-Poison': '银伴战兽（毒属性）',
    'Silvally-Psychic': '银伴战兽（超能力属性）',
    'Silvally-Rock': '银伴战兽（岩石属性）',
    'Silvally-Steel': '银伴战兽（钢属性）',
    'Silvally-Water': '银伴战兽（水属性）',
    
    # 特殊形态
    'Urshifu-Rapid-Strike': '武道熊师（急流）',
    'Urshifu-Rapid-Strike-Gmax': '武道熊师（急流超极巨化）',
    'Calyrex-Ice': '蕾冠王（白马）',
    'Calyrex-Shadow': '蕾冠王（黑马）',
    'Toxtricity-Low-Key': '颤弦蝾螈（低调）',
    'Dudunsparce-Three-Segment': '土龙节节（三节）',
    'Palafin-Hero': '海豚侠（英雄）',
    'Maushold-Four': '一家鼠（四只）',
    'Gimmighoul-Roaming': '索财灵（流浪）',
    'Poltchageist-Artisan': '斯魔茶（工匠）',
    'Sinistcha-Masterpiece': '来悲粗茶（杰作）',
    
    # 霸主形态
    'Salazzle-Totem': '焰后蜥（霸主）',
    'Vikavolt-Totem': '锹农炮虫（霸主）',
    'Ribombee-Totem': '蝶结萌虻（霸主）',
    
    # 特殊形态
    'Vivillon-Fancy': '彩粉蝶（花纹）',
    'Vivillon-Pokeball': '彩粉蝶（精灵球花纹）',
    'Floette-Eternal': '花叶蒂（永恒）',
    'Aegislash-Blade': '坚盾剑怪（剑形态）',
} 