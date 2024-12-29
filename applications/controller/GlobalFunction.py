import openpyxl, pathlib, datetime
import pandas as pd


def generateExcel(menu, data):
    try:
        download_path = pathlib.Path.home() / "Downloads"
        file_name = f'{download_path}/Data {menu} {datetime.datetime.now().strftime("%d-%m-%Y")}.xlsx'
        df = pd.DataFrame.from_dict(data)
        df.to_excel(file_name, index=False, sheet_name=menu)

        # Use openpyxl's load_workbook method to open the Excel file and get the worksheet object
        wb = openpyxl.load_workbook(file_name)
        ws = wb[menu]

        # Iterate through all columns in the worksheet, use the column_dimensions property to get the column object, and set the auto_size attribute to True for automatic column width adjustment
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter # Get the column name
            for cell in col:
                try: # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column].width = adjusted_width

        # Use the save method to save the modified Excel file
        wb.save(file_name)
        return True, ''
    except Exception as e:
        print(e)
        return False, e