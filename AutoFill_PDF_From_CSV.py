import os
import eel
import tkinter
import tkinter.filedialog
import pandas as pd

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, IndirectObject, NameObject

eel.init('app')

def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
    except OSError:
        print("Directory Already Exists")

def check_pdf_extension(in_string):
    extension = '.pdf'
    if extension not in in_string:
        return in_string + '.pdf'
    else:
        return in_string

def convert_csv_to_df(in_csv):
    if '.csv' in in_csv:
        return pd.read_csv(in_csv)

    full_path_csv = f'{in_csv}.csv'
    return pd.read_csv(full_path_csv)

def create_checkboxfields_dict(dct, fields):
    """create dictionary with only checkbox columns"""
    clean = {k:v for k,v in dct.items() if k in fields and pd.notnull(v)}
    dct = {k:v for k,v in dct.items() if k not in fields}
    return clean, dct

def remove_undeclared_checkboxfields(pdf, dct):
    """remove btn fields that weren't declared in the checkbox_fields variable"""
    reader = PdfFileReader(pdf)
    ff = reader.getFields()
    fields_to_remove = [x for x in ff if '/Btn' in ff[x].values()]
    return {k:v for k,v in dct.items() if k not in fields_to_remove}

def set_need_appearances_writer(writer: PdfFileWriter):
    try:
        catalog = writer._root_object
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)
            })
        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer

def pdf_writer_from_reader(reader: PdfFileReader):
    """
    Initializes a PdfFileWriter that can be used to write data to the given PDF
    stored inside of the PdfFileReader.
    """
    if not reader or reader.getNumPages() == 0:
        raise Exception(
            'Error initializing PdfFileWriter, given PdfFileReader is either null or contains no pages.'
        )

    pdf_writer = PdfFileWriter()

    # Add all PDF pages from reader -> writer
    pdf_writer.appendPagesFromReader(reader)

    # Copy over additional data from reader -> writer
    pdf_writer._info = reader.trailer["/Info"]
    reader_trailer = reader.trailer["/Root"]
    pdf_writer._root_object.update(
        {
            key: reader_trailer[key]
            for key in reader_trailer
            if key in ("/AcroForm", "/Lang", "/MarkInfo")
        }
    )

    # Set written data appearances to be visible
    pdf_writer = set_need_appearances_writer(pdf_writer)
    if "/AcroForm" in pdf_writer._root_object:
        pdf_writer._root_object["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    return pdf_writer

def updateCheckboxValues(page, fields):
        for j in range(len(page['/Annots'])):
            writer_annot = page['/Annots'][j].getObject()
            for field in fields:
                if writer_annot.get('/T') == field:
                    writer_annot.update({
                        NameObject("/V"): NameObject(fields[field]),
                        NameObject("/AS"): NameObject(fields[field])
                        })

def get_tkinter_root():
    root = tkinter.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)

@eel.expose
def btn_csv_click():
    get_tkinter_root()
    return tkinter.filedialog.askopenfilename(title = "Select file",filetypes = (("CSV Files","*.csv"),))

@eel.expose
def btn_pdf_click():
    get_tkinter_root()
    return tkinter.filedialog.askopenfilename(title = "Select file",filetypes = (("PDF Files","*.pdf"),))

@eel.expose
def btn_folder_click():
	get_tkinter_root()
	return tkinter.filedialog.askdirectory()

@eel.expose()
def csv_to_PDF(csv, PDF_template, output_loc, output_filename, colkey=None, checkbox_fields=None):
    """Function creates one PDF per row from a csv.
    Column names must match the form field names within PDF template. 

    Args:
        csv (path): input data, must be a  ull path to csv file.
        PDF_template (path): PDF to fill with input data, full path to PDF file.
        output_loc (directory path, optional): String full path to directory of output location.
        output_filename (string): string of what the output files should be named
        colkey (string, optional): Option to pass a unique column key to identify each file. If column
            values are not unique, files will be overwritten. Defaults to None and uses a number counter 
            to differentiate files.
        checkbox_fields (list, optional): Option to pass a list of columns that represent checkbox
            form fields. Defaults to None.
    """
    try:
        pdf_name = os.path.basename(PDF_template).split('.')[0] + '_AUTOFILLOUTPUT'
        outputfolder = os.path.join(output_loc, pdf_name)
        create_folder(outputfolder)

        output_filename = check_pdf_extension(output_filename)
        PDF_template = check_pdf_extension(PDF_template)

        df = convert_csv_to_df(csv)
        dict_records = df.to_dict('records')
        for colkey_counter, df_dic in enumerate(dict_records, start=1):
            #remove key if the value is null
            df_dic = {k: v for k, v in df_dic.items() if v == v}
            if checkbox_fields:
                checkbox_dict_clean, df_dic = create_checkboxfields_dict(df_dic, checkbox_fields)
            else:
                df_dic = remove_undeclared_checkboxfields(PDF_template, df_dic)

            reader = PdfFileReader(PDF_template)
            writer = pdf_writer_from_reader(reader)
            for page in range(reader.numPages):
                writer_page = writer.getPage(page)
                writer.updatePageFormFieldValues(writer_page, df_dic)
                if checkbox_fields:
                    updateCheckboxValues(writer_page, checkbox_dict_clean)

            colkey_value = str(colkey_counter) if not colkey else str(df_dic[colkey])
            front_of_filename = output_filename.split('.')[0]
            new_name = f'{front_of_filename}_{colkey_value}.pdf'
            out_pdf = os.path.join(outputfolder, new_name)

            with open(out_pdf,"wb") as new:
                writer.write(new)
        eel.finished()
    except Exception as e:
        eel.error()

eel.start('index.html', size=(600, 700))