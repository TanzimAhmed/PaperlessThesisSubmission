from pages import DocumentTest

document_test = DocumentTest('Test_template.docx')
print(document_test.get_page_properties())
print(document_test.get_text_properties())
# document_test.check_paragraph_styles()
# document_test.check_heading_styles()


"""
set_x = {'apple', 'banana', 'coconut'}
set_x.add('apple')
set_x.remove('banana')
set_x.update(['mango', 'orange'])
print('apple' in set_x)
print({'apple', 'orange'} <= set_x)
print(set_x)

set_y = set()
set_y.update(['apple', 'mango', 'orange', 'banana'])
print(set_y)
"""
