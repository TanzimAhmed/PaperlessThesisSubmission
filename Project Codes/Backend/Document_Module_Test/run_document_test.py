from pages import DocumentTest

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
