
[![LinkedIn][linkedin-shield]][linkedin-url]

<p align="center">
  <h2 align="center">AutoFill PDF From CSV</h2>
  <p align="center">
    A python function that auto fills a template pdf's form fields, creating one PDF per row from a csv or dataframe<br>
  </p>
</p>

<!-- ABOUT THE PROJECT -->
  Description: <br>
  This function will add
  
<h3>Usage</h3> 

```bash
dataframe_to_PDF(df_or_CSV, PDF_template, output_filename, colkey="default", checkbox_fields="default")
```

<b>df_or_CSV</b>: Full Path to CSV or a pandas dataframe <br>
<b>PDF_Template</b>: Full Path to the PDF template <br>
<b>output_filename</b>: Name for the output PDFs. <br>
<b>colkey</b>: A column used as a key for the PDFs. Must be a unique field otherwise PDFs will overwrite. "default"
will attached number at the end of the file for each row in the input table. <br>
<b>checkbox_fields</b>: if there are fields within your table that are for a form field checkbox within the PDF, they will need to 
be passed to this function as a list using this argument. Otherwise, the script will not interpret the checkbox fields correctly<br>
  
  <img src="https://lh3.googleusercontent.com/jqjeu7Me452qzRuVmN14eAg2UEpQyqU8ddkwsJX3xavJQKYqAYdabksl76aorKelR-xwbUcA9p0Y3GabXRpoFSH56QCIWqXPmfR5_1wtL-NAM4ZWQiIDFYBiFvj9aCsDKwRE-zC_QQ=w2400" width="400px">


### Built With
* [PyPDF2](https://github.com/mstamy2/PyPDF2)
* [Pandas](https://pandas.pydata.org/)

<!-- CONTACT -->
## Contact
Eric Samson: [@MyTwitter](https://twitter.com/EricSamsonGIS) <br>
Email: ericsamsonwx@gmail.com <br>
Website: [EricSamson.com](https://ericsamson.com) <br>

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/iamericsamson
