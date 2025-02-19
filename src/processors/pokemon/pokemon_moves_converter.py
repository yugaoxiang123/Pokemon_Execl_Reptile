import json
import os
from pathlib import Path
from tqdm import tqdm

class PokemonMovesConverter:
    def __init__(self):
        self.json_dir = Path('json')
        self.output_dir = Path('output')
        self.input_file = self.json_dir / 'pokemon_moves.json'
        self.output_file = self.json_dir / 'pokemon_moves_formatted.json'
        
        # 创建必要的目录
        self.json_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def load_data(self) -> dict:
        """加载原始JSON数据"""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载数据失败: {e}")
            return {}
    
    def save_data(self, data: dict):
        """保存处理后的JSON数据"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到: {self.output_file}")
        except Exception as e:
            print(f"保存数据失败: {e}")
    
    def convert_moves(self):
        """转换技能数据格式"""
        print("开始转换宝可梦技能数据...")
        
        try:
            # 加载原始数据
            data = self.load_data()
            if not data:
                return
            
            # 处理每个宝可梦的技能数据
            processed_data = {}
            print("处理数据中...")
            for pokemon, moves in tqdm(data.items()):
                if moves and isinstance(moves, str):
                    # 移除转义字符并解析JSON
                    moves = moves.replace('\\', '')
                    try:
                        moves_json = json.loads(moves)
                        processed_data[pokemon] = moves_json
                    except json.JSONDecodeError as e:
                        print(f"解析 {pokemon} 的技能数据失败: {e}")
                        processed_data[pokemon] = moves  # 保留原始数据
            
            # 保存处理后的数据
            self.save_data(processed_data)
            
            # 显示示例数据
            print("\n数据示例:")
            sample_items = list(processed_data.items())[:2]
            for name, moves in sample_items:
                print(f"\n{name}:")
                print(json.dumps(moves, ensure_ascii=False, indent=2))
            
            print(f"\n完成! 共处理了 {len(processed_data)} 个宝可梦的技能数据")
            
        except Exception as e:
            print(f"处理数据失败: {e}")
            import traceback
            print(traceback.format_exc())

def main():
    converter = PokemonMovesConverter()
    converter.convert_moves()

if __name__ == "__main__":
    main() 