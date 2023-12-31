from pypdf import PdfReader
from pypdf import PdfWriter
import argparse
import os


########################################################################################################################
def remove_pages(in_file, out_file, rem_pages):
    in_pdf = None
    try:
        in_pdf = PdfReader(in_file)
    except FileNotFoundError:
        print('Could not open file. Aborting')
        exit(1)

    print('Removing pages: ' + str(rem_pages))
    pages = []
    try:
        pages = [int(x) for x in str(rem_pages).split(',')]
    except ValueError:
        print('Could not parse REMOVE_PAGES. Aborting.')
        exit(1)

    out_pdf = PdfWriter()
    for i in range(len(in_pdf.pages)):
        if i + 1 not in pages:
            out_pdf.append(in_pdf, [i])

    out_pdf.write(out_file)
    out_pdf.close()


########################################################################################################################
def append_pages(in_file, out_file, app_pages):
    in_pdf = None
    try:
        in_pdf = PdfReader(in_file)
    except FileNotFoundError:
        print('Could not open file. Aborting')
        exit(1)

    print('Appending pages: ' + str(app_pages))
    pages = []
    try:
        pages = [int(x) for x in str(app_pages).split(',')]
    except ValueError:
        print('Could not parse APPEND_PAGES. Aborting.')
        exit(1)

    out_pdf = PdfWriter()
    for i in range(len(pages)):
        out_pdf.append(in_pdf, [pages[i] - 1])

    out_pdf.write(out_file)
    out_pdf.close()


########################################################################################################################
def merge_pdfs(out_file, merge_files):
    print('Merging PDFs: ' + str(merge_files))
    pages = [x for x in str(merge_files).split(',')]

    out_pdf = PdfWriter()
    for s in pages:
        print('Try open PDF: ' + s)
        in_pdf = None
        try:
            in_pdf = PdfReader(s)
        except FileNotFoundError:
            print('Could not open file. Aborting')
            exit(1)
        out_pdf.append(in_pdf)

    out_pdf.write(out_file)
    out_pdf.close()


########################################################################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple PDF utility program.')
    parser.add_argument('-i', dest='in_file', help='The input PDF file path')
    parser.add_argument('-o', dest='out_file', help='The output PDF file path')
    parser.add_argument('-r', dest='remove_pages', help='remove pages from PDF')
    parser.add_argument('-a', dest='append_pages', help='append pages from PDF')
    parser.add_argument('-m', dest='merge_pdfs', help='merge multiple PDFs to one')
    args = parser.parse_args()

    input_file = ''
    if args.in_file is None and args.merge_pdfs is None:
        print('No input PDF file given. Aborting.')
        exit(1)
    if args.merge_pdfs is None:
        input_file = args.in_file
        print('Input file: ' + input_file)

    output_file = ''
    if args.out_file is None:
        print('No output PDF file given. Set to default.')
        output_file = os.getcwd() + '\simpdf_out.pdf'
    else:
        output_file = args.out_file
    print('Output file: ' + output_file)

    if args.remove_pages is not None:
        remove_pages(input_file, output_file, args.remove_pages)
    if args.append_pages is not None:
        append_pages(input_file, output_file, args.append_pages)
    if args.merge_pdfs is not None:
        merge_pdfs(output_file, args.merge_pdfs)
