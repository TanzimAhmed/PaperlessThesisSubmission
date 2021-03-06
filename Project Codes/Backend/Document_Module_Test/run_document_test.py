from pages import DocumentTest, PdfDocumentTest

pdf_test = PdfDocumentTest('test_template.pdf')
# pdf_test.print_properties()
if pdf_test.is_valid_format():
    print('Format is Valid')
else:
    print('Format is NOT valid')
    print('Errors: ')
    for error in pdf_test.errors:
        print(error)
print('\n\n')
print('Fonts:', pdf_test.fonts)
print('Line Height:', pdf_test.line_height)
print('Margins:', pdf_test.margin)
print('Height, Width:', pdf_test.page_height, pdf_test.page_width)
# print(pdf_test.line_height)

"""
document_test = DocumentTest('test_template_.docx')
print('Document Properties: ')
print(document_test.get_page_properties())
print(document_test.get_text_properties())
print()
if document_test.is_valid_format():
    print('Format is Okay')
else:
    print(f'Sorry, The format contains errors. Errors: {document_test.errors}')
# document_test.check_paragraph_styles()
# document_test.check_heading_styles()
"""
