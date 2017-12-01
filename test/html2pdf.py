import pdfkit

n = 0

if n == 0:
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }

    pdfkit.from_url('https://giuliomarin.github.io/extra/webcam.html', '/Users/giulio/Desktop/images.pdf', options=options)