import pandas as pd
import json
import re
from pathlib import Path
from tqdm import tqdm

class MoveFormatConverter:
    def __init__(self):
        self.excel_file = Path('output/pokemon_data.xlsx')
        
    def convert_move_format(self):
        """将升级技能列的数据转换为JSON格式"""
        try:
            print("读取Excel文件...")
            with pd.ExcelFile(self.excel_file) as xls:
                df = pd.read_excel(xls, sheet_name='Sheet1')
            
            if '升级技能' not in df.columns:
                print("未找到升级技能列")
                return
                
            print("转换技能格式...")
            df['升级技能'] = df['升级技能'].apply(self._convert_to_json)
            
            print("\n保存更新后的数据...")
            with pd.ExcelWriter(self.excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
                
                # 调整列宽
                # worksheet = writer.sheets['Sheet1']
                # worksheet.column_dimensions['A'].width = 30  # 宝可梦名称列
                # worksheet.column_dimensions['B'].width = 50  # 进化条件列
                # worksheet.column_dimensions['C'].width = 150  # 升级技能列
            
            print("完成!")
            
        except Exception as e:
            print(f"转换失败: {e}")
    
    def _convert_to_json(self, move_text: str) -> str:
        """将单个技能文本转换为JSON格式"""
        if pd.isna(move_text):
            return json.dumps({"init": [], "levels": {}})
            
        try:
            # 初始化结果字典
            result = {"init": [], "levels": {}}
            
            # 使用正则表达式匹配括号内的内容
            initial_moves = re.search(r'\((.*?)\)', move_text)
            level_pattern = r'\[(.*?)\]'  # 匹配 [L3:Vine Whip]
            
            # 处理初始技能
            if initial_moves:
                init_moves = initial_moves.group(1).split(',')
                result["init"] = [move.strip() for move in init_moves]
            
            # 处理等级技能
            level_matches = re.findall(level_pattern, move_text)
            for level_move in level_matches:
                level_move = level_move.strip()
                if ':' in level_move:
                    level, move = level_move.split(':', 1)
                    level = level.strip()
                    move = move.strip()
                    
                    # 如果该等级已存在，将技能添加到列表中
                    if level in result["levels"]:
                        if isinstance(result["levels"][level], list):
                            result["levels"][level].append(move)
                        else:
                            # 将单个技能转换为列表
                            result["levels"][level] = [result["levels"][level], move]
                    else:
                        # 新等级，直接添加技能
                        result["levels"][level] = [move]
            
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            print(f"转换技能格式失败: {move_text}")
            print(f"错误: {e}")
            return json.dumps({"init": [], "levels": {}})

def main():
    converter = MoveFormatConverter()
    converter.convert_move_format()

if __name__ == "__main__":
    main() 