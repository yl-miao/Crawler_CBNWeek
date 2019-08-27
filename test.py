import pdfkit

options = {
    'minimum-font-size': '26',
    'page-height': '3.5in',
    'page-width': '2.55in',
    'margin-top': '0.01in',
    'margin-right': '0.01in',
    'margin-left': '0.01in',
    'margin-bottom': '0.01in',
    'encoding': "UTF-8",
    'outline-depth': 10,
}
path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
pdfkit.from_url("temp.html", "out.pdf", configuration=config, options=options)
