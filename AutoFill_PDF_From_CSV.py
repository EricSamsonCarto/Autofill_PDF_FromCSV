import os
import pandas as pd 
import eel

from pathlib import Path
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from PyPDF2.generic import (BooleanObject, IndirectObject, NameObject,
                            NumberObject)

eel.init(r'C:\Users\eric.samson\Documents\Python\Workplaces\PyPDF2_improvements\web\web')

@eel.expose
def dataframe_to_PDF(df_or_CSV, PDF_template, output_filename, colkey="default", checkbox_fields="default"):
    #----------------------------------------------------
    #Create output folder location:
    folder = Path(PDF_template).parent.absolute()
    pdf_name = os.path.basename(PDF_template).split('.')[0] + '_AUTOFILLOUTPUT'  
    outputfolder = os.path.join(folder, pdf_name)

    try:
        os.mkdir(outputfolder)
    except OSError:
        print("Directory Already Exists")
    else:
        print("Created Directory")

    #add checkbox list to a list:
    if checkbox_fields != 'default':
        checkbox_fields = checkbox_fields.split(",")
        checkbox_fields = [x.strip() for x in checkbox_fields]
    
    #add .pdf extensions if the user didn't include them
    extension = '.pdf'
    if extension not in output_filename:
        output_filename = output_filename + '.pdf'
    if extension not in PDF_template:
        PDF_template = PDF_template + '.pdf'
    
    #Convert to dataframe if from csv
    if isinstance(df_or_CSV, str):
        if '.csv' not in df_or_CSV:
            df_or_CSV = df_or_CSV + '.csv'
            df = pd.read_csv(df_or_CSV)
    else:
        df = df_or_CSV
    
    #send all records to dictionaries
    dict_records = df.to_dict('records')

    #----------------------------------------------------

    #Set up set appearances function
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

    #Set up Function for checkboxvalues
    def updateCheckboxValues(page, fields):
        for j in range(0, len(page['/Annots'])):
            writer_annot = page['/Annots'][j].getObject()
            for field in fields:
                if writer_annot.get('/T') == field:
                    writer_annot.update({
                        NameObject("/V"): NameObject(fields[field]),
                        NameObject("/AS"): NameObject(fields[field])
                        })

    #loop through dictionaries to create one PDF per row
    colkey_counter = 0
    for dic in dict_records:
        colkey_counter += 1
        if checkbox_fields != 'default':
            check_dic = {k:v for k,v in dic.items() if k in checkbox_fields}
            dic = {k:v for k,v in dic.items() if k not in checkbox_fields}
            check_dic_clean = {k:v for k,v in check_dic.items() if pd.notnull(v)}

        #Read in template PDF
        f = open(PDF_template, "rb")
        pdf = PdfFileReader(f)
        #get number of pages within the template pdf
        numPages = pdf.getNumPages()
        page_num_list = [x for x in range(0,numPages)]

        writer = PdfFileWriter()
        for page_num in page_num_list:
            page = pdf.getPage(page_num)
            set_need_appearances_writer(writer)
            writer.updatePageFormFieldValues(page, fields=dic)
            writer.addPage(page)
            if checkbox_fields != 'default':
                updateCheckboxValues(page, check_dic_clean)
            
            #default colkey argument
            if colkey =='default':
                value = str(colkey_counter)
            else:
                value = str(dic[colkey])
            
            #Set up filename
            new_name = output_filename.split('.')[0] + '_' + value + '.' + output_filename.split('.')[1]
            out_pdf = os.path.join(outputfolder, new_name)

        with open(out_pdf,"wb") as new:
            writer.write(new)

        f.close()
    
eel.start('index.html', size={1000, 200})
