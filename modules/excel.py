import pandas as pd


def save_excel(self, df: pd.DataFrame, book_name: str, sheet_name: str):
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(book_name + ".xlsx", engine="xlsxwriter")
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    # Add a format.
    text_format = workbook.add_format({"text_wrap": True})
    # Resize columns for clarity and add formatting to column C.
    worksheet.set_column(4, 4, 70, text_format)
    # Close the Pandas Excel writer and output the Excel file.
    writer.close()
