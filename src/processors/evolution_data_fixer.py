import pandas as pd
from pathlib import Path

class EvolutionDataFixer:
    def __init__(self):
        self.excel_file = Path('output/pokemon_data.xlsx')
        
    def fix_empty_evolution_data(self):
        """修复进化条件列的空值"""
        try:
            print("读取Excel文件...")
            with pd.ExcelFile(self.excel_file) as xls:
                df = pd.read_excel(xls, sheet_name='LevelUpMoves')
            
            print("处理空值...")
            # 将进化条件列的空值替换为'null'
            if '进化条件' in df.columns:
                df['进化条件'] = df['进化条件'].fillna('null')
                print("已将空值替换为'null'")
            else:
                print("未找到进化条件列")
                return
            
            print("\n保存更新后的数据...")
            # 保存更新后的数据
            with pd.ExcelWriter(self.excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='LevelUpMoves', index=False)
                
                # 调整列宽
                worksheet = writer.sheets['LevelUpMoves']
                worksheet.column_dimensions['A'].width = 30  # 宝可梦名称列
                worksheet.column_dimensions['B'].width = 50  # 进化等级列
                worksheet.column_dimensions['C'].width = 150  # 升级技能列
            print("完成!")
            
        except Exception as e:
            print(f"处理失败: {e}")

def main():
    fixer = EvolutionDataFixer()
    fixer.fix_empty_evolution_data()

if __name__ == "__main__":
    main() 