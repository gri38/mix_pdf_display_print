from pathlib import Path
import sys
import fitz
import argparse
import io


parser = argparse.ArgumentParser(description='Mix 2 pdf files into one with same pages count and 2 layers (dispaly and print)')
parser.add_argument("display_pdf_file", help="path the the pdf file used for display layer")
parser.add_argument("print_pdf_file", help="path the the pdf file used for print layer")
parser.add_argument("out_pdf_file", help="path the the output pdf file")
args = parser.parse_args()

path_display = args.display_pdf_file
path_print = args.print_pdf_file
path_out = args.out_pdf_file

display_doc = fitz.open(path_display)
print_doc = fitz.open(path_print)

page_count = display_doc.pageCount
if page_count != print_doc.pageCount:
    print("error: inputs don't have same page count.")
    sys.exit(-1)

out_doc = fitz.open()

print_group = out_doc.add_ocg("print", on=0, usage="Print")
display_group = out_doc.add_ocg("display", on=1, usage="View")
print_ocmd = out_doc.set_ocmd(0, [print_group], ve=["and", print_group, ["not",display_group]])

for page_index in range(page_count):
    display_page = display_doc.load_page(page_index)
    print_page = print_doc.load_page(page_index)
    page = out_doc.new_page()
    rect = fitz.Rect(0, 0, page.rect.width, page.rect.height)
    page.show_pdf_page(rect, print_doc, page_index, oc=print_ocmd)
    page.show_pdf_page(rect, display_doc, page_index, oc=display_group)

out_doc.save(path_out)
