
[![LinkedIn][linkedin-shield]][linkedin-url]

<p align="center">
  <h2 align="center">AutoFill PDF From CSV</h2>
  <p align="center">
    A python function that auto fills a template pdf's form fields, creating one PDF per row from a csv or dataframe<br>
  </p>
</p>

<div align="center">
<img src="" width="450px">
</div>

<!-- ABOUT THE PROJECT -->
  <br><b>DataFrame_or_CSV_to_PDF.py</b> python functions
  <br><b>AutoFill_PDF_From_CSV.py</b> functions formatted for creating the eel application
  <br><b>app</b> is a folder holding the front end files used to create the gui.

<h3>App Usage</h3>
Running AutoFill_PDF_From_CSV.py will open up the application, the below gif illustrates how to use it:

<div align="center">
<img src="" width="400px">
</div>

For easier usage, you can download the latest version of the exe program from the Releases tab, made with pyinstaller.

<h3>Python Usage</h3> 

```bash
df_csv_to_PDF(df_or_csv, PDF_template, output_filename, colkey=None, checkbox_fields=None, output_loc=None)
```

<b>df_or_csv</b> (dataframe or csv path): input data, must be a pandas dataframe or full path to csv file.<br>
<b>PDF_template</b> (pdf path): PDF to fill with input data, full path to PDF file.<br>
<b>output_filename</b> (string): string of what the output files should be named. <br>
<b>colkey</b> (string, optional): Option to pass a unique column key to identify each file. If column values are not unique, files will be overwritten. Defaults to None and uses a number counter to differentiate files.<br>
<b>output_loc</b> (directory path, optional): String full path to directory of output location. Defaults to None and outputs to directory of PDF_template.<br>
<b>checkbox_fields</b> (list, optional): Option to pass a list of columns that represent checkbox form fields. Defaults to None.<br>

### Built With
* [PyPDF2](https://github.com/mstamy2/PyPDF2)
* [Pandas](https://pandas.pydata.org/)
* [Eel](https://github.com/samuelhwilliams/Eel)

<!-- CONTACT -->
## Contact
Eric Samson: [@EricSamsonGIS](https://twitter.com/EricSamsonGIS) <br>
Email: ericsamsonwx@gmail.com <br>
Website: [EricSamson.com](https://ericsamson.com) <br>

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/iamericsamson
