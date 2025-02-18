from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

def create_index_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = "Index"
    
    # 添加表头
    headers = ["模式", "表类型", "表文件名"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
    
    # 添加示例数据
    data = [
        ["类型表", "", "Type.xlsx"],
        ["数据表", "ability_data", "ability_data.xlsx"]
    ]
    for row_idx, row_data in enumerate(data, 2):
        for col_idx, value in enumerate(row_data, 1):
            ws.cell(row=row_idx, column=col_idx, value=value)
    
    wb.save("C:/Users/90953/Downloads/my-pokemon-excel-designer/Index.xlsx")

def create_type_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = "Type"
    
    # 添加表头
    headers = ["种类", "对象类型", "标识名", "字段名", "字段类型", "数组切割", "值", "索引", "标记"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
    
    # 添加示例数据
    data = [
        ["表头", "ability_data", "特性名称(英文)", "Name", "string", "", "", "", ""],
        ["表头", "ability_data", "特性名称(中文)", "ChineseName", "string", "", "", "", ""],
        ["表头", "ability_data", "评分", "Score", "int", "", "", "", ""],
        ["表头", "ability_data", "编号", "ID", "int", "", "", "", ""],
        ["表头", "ability_data", "特性描述", "Description", "string", "", "", "", ""]
    ]
    for row_idx, row_data in enumerate(data, 2):
        for col_idx, value in enumerate(row_data, 1):
            ws.cell(row=row_idx, column=col_idx, value=value)
    
    wb.save("C:\\Users\\90953\\Downloads\\my-pokemon-excel-designer\\Type.xlsx")
    # wb.save(r"C:\Users\90953\Downloads\baokemeng\my-pokemon\my-pokemon-excel-designer\Type.xlsx")

# def create_ability_data_xlsx():
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Sheet1"
    
#     # 添加表头
#     headers = ["特性名称(英文)", "特性名称(中文)", "评分", "编号", "特性描述"]
#     for col, header in enumerate(headers, 1):
#         cell = ws.cell(row=1, column=col, value=header)
#         cell.font = Font(bold=True)
    
#     wb.save("ability_data.xlsx")

def main():
    print("开始创建 Excel 文件...")
    create_index_xlsx()
    print("已创建 Index.xlsx")
    create_type_xlsx()
    print("已创建 Type.xlsx")
    # create_ability_data_xlsx()
    # print("已创建 ability_data.xlsx")
    print("\n所有文件创建完成！")
    print("请在 ability_data.xlsx 中填写具体的特性数据。")

if __name__ == "__main__":
    main()