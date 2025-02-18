# TabToy 使用教程

TabToy 是一个高效的跨平台电子表格导出工具，可以将 Excel 表格导出为 JSON、CSV 等多种格式。

## 1. 安装

1. 下载 TabToy
   - 访问 [TabToy Releases](https://github.com/davyxu/tabtoy/releases)
   - 下载最新版本的 Windows 执行文件 (tabtoy_windows_amd64.exe)
   - 将下载的文件重命名为 `tabtoy.exe`

2. 设置环境变量
   - 将 tabtoy.exe 放在一个固定目录（如 `C:\Tools\tabtoy\`）
   - 添加到系统环境变量 Path 中
   - 或者直接复制到项目目录下使用

## 2. 配置文件

1. 创建配置文件 `tabtoy.json`：
```json
{
    "Version": "v3",
    "InputFiles": [
        {
            "InputPath": "C:/Users/90953/Downloads/pokemon-parse/output/pokemon_data.xlsx",
            "SheetName": "Sheet1",
            "TableName": "pokemon",
            "TypeMapping": {
                "编号": "int",
                "中文名称": "string",
                "英文名称": "string",
                "生命值": "int",
                "攻击": "int",
                "防御": "int",
                "特攻": "int",
                "特防": "int",
                "速度": "int",
                "升级技能": "string",
                "进化条件": "string"
            }
        },
        {
            "InputPath": "C:/Users/90953/Downloads/pokemon-parse/output/pokemon_data.xlsx",
            "SheetName": "LevelUpMoves",
            "TableName": "levelup_moves",
            "TypeMapping": {
                "宝可梦": "string",
                "进化条件": "string",
                "升级技能": "string"
            }
        }
    ],
    "OutputFiles": [
        {
            "OutputPath": "pokemon_data.json",
            "Format": "json",
            "PrettyPrint": true
        }
    ]
}
```

## 3. 导出命令

1. 基本导出：
```bash
# 在配置文件所在目录执行
tabtoy.exe -config tabtoy.json
```

2. 带格式化的导出：
```bash
# 导出并格式化 JSON
tabtoy.exe -config tabtoy_pokemon_data.json -json_indent
.\tabtoy.exe -mode v2 -index tabtoy_pokemon_data.json -json_out pokemon_data.json
.\tabtoy.exe -mode=v3 -index tabtoy_pokemon_data.json -json_out pokemon_data.json
.\tabtoy.exe -mode=v3 -index=Index.xlsx -json_out=table_gen.json
tabtoy.exe -mode=v3 -index=Index.xlsx -json_out=table_gen.json
.\tabtoy.exe -mode=v3 -index=C:\Users\90953\Downloads\my-pokemon-excel-designer\Index.xlsx -json_out=C:\Users\90953\Downloads\my-pokemon-excel-designer\table_gen.json
```

## 4. 常见问题

1. 编码问题
   - 确保 Excel 文件保存为 UTF-8 编码
   - 如果出现中文乱码，可以尝试使用 `-utf8bom` 参数

2. 路径问题
   - 使用正斜杠 `/` 或双反斜杠 `\\` 作为路径分隔符
   - 建议使用绝对路径避免问题

3. 数据类型问题
   - 在 TypeMapping 中正确指定数据类型
   - 支持的类型：string, int, float, bool 等

## 5. 输出示例

导出的 JSON 文件格式如下：
```json
{
    "pokemon": [
        {
            "编号": 1,
            "中文名称": "妙蛙种子",
            "英文名称": "Bulbasaur",
            "生命值": 45,
            "攻击": 49,
            "防御": 49,
            "特攻": 65,
            "特防": 65,
            "速度": 45,
            "升级技能": "{\"init\":[\"Growl\",\"Tackle\"],\"levels\":{\"L3\":[\"Vine Whip\"]}}",
            "进化条件": "L16:Ivysaur"
        }
    ],
    "levelup_moves": [
        {
            "宝可梦": "Bulbasaur",
            "进化条件": "L16:Ivysaur",
            "升级技能": "(Growl,Tackle) [L3:Vine Whip]"
        }
    ]
}
```

## 6. 注意事项

1. 表格要求
   - 第一行必须是字段名
   - 数据类型要一致
   - 避免空行

2. 配置文件
   - 检查路径是否正确
   - 确保 TypeMapping 与实际数据类型匹配
   - 表名不要重复

3. 性能优化
   - 对于大型表格，建议使用 `-parallel` 参数
   - 可以使用 `-cache` 参数启用缓存
