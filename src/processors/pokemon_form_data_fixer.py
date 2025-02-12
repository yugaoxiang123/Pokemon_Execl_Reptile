import pandas as pd
from pathlib import Path

class PokemonFormDataFixer:
    def __init__(self):
        self.excel_file = Path('output/pokemon_web_info.xlsx')
        
    def fix_empty_form_data(self):
        """修复形态宝可梦的空数据"""
        print("读取Excel文件...")
        df = pd.read_excel(self.excel_file)
        
        # 找到捕获率为空的行
        empty_catch_rate_mask = df['捕获率（网页）'].isna()
        empty_rows = df[empty_catch_rate_mask]
        
        if empty_rows.empty:
            print("没有找到需要修复的数据")
            return
        
        print(f"\n找到 {len(empty_rows)} 个需要修复的形态")
        
        # 获取所有列名，排除不需要复制的列
        columns_to_copy = df.columns.tolist()
        columns_to_copy.remove('英文名称')
        columns_to_copy.remove('中文名称')
        
        # 处理每个空数据的形态
        for idx, row in empty_rows.iterrows():
            form_name = row['英文名称']
            base_name = form_name.split('-')[0]  # 获取基础形态名称
            
            print(f"\n处理: {form_name} (基础形态: {base_name})")
            
            # 找到对应的基础形态数据
            base_form = df[df['英文名称'].str.match(f"^{base_name}$", case=True)]
            
            if base_form.empty:
                print(f"未找到基础形态 {base_name} 的数据")
                continue
                
            # 复制所有指定列的数据，不管是否为空
            for col in columns_to_copy:
                # if pd.isna(df.at[idx, col]):  # 只复制空值
                #     df.at[idx, col] = base_form.iloc[0][col]
                #     print(f"复制 {col}: {base_form.iloc[0][col]}")
                df.at[idx, col] = base_form.iloc[0][col]
                print(f"复制 {col}: {base_form.iloc[0][col]}")
        
        # 保存更新后的文件
        print("\n保存更新后的数据...")
        df.to_excel(self.excel_file, index=False)
        print("完成!")

def main():
    fixer = PokemonFormDataFixer()
    fixer.fix_empty_form_data()

if __name__ == "__main__":
    main() 