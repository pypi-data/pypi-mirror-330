'''
Pawpyrus is a minimalist open-source paper data storage based on QR codes and
ArUco. It generates a PDF from any small-sized binary file (recommended size
<100kb). Further, the paper data storage can be scanned and decoded (recommended
resolution 300dpi).

Details: https://pypi.org/project/pawpyrus
Git repo: https://codeberg.org/screwery/pawpyrus
'''

__version__ = '2025.2.27.0'
__repository__ = 'https://codeberg.org/screwery/pawpyrus'
__bugtracker__ = 'https://codeberg.org/screwery/pawpyrus/issues'

from argparse import ArgumentParser, RawDescriptionHelpFormatter #
from datetime import datetime
from glob import glob
from hashlib import sha256
from io import StringIO
from itertools import product
import json
import logging
from math import floor, dist
from os import mkdir
from os.path import join, realpath
from random import random
import sys

from pyzbar.pyzbar import decode #
from reportlab.graphics import renderPDF #
from reportlab.lib.units import mm #
from reportlab.pdfgen import canvas #
from svglib.svglib import svg2rlg #

from bitarray import bitarray #
import cv2 # opencv-python + opencv-contrib-python
from more_itertools import sliced #
import numpy #
from qrcode import QRCode #
from qrcode.util import QRData, MODE_ALPHA_NUM #
from tqdm import tqdm #

def calculate_bit_chunk():
    '''
    Calculate bit chunk size
    '''
    index = 0
    while 1:
        index += 1
        if (CC_CAPACITY / (2 ** index)) < 1:
            break
    return index - 1

def calculate_hash_size():
    '''
    Calculate hash block size
    '''
    index = 0
    while 1:
        index += 1
        if ((CC_BASIS ** index) / (2 ** 256)) > 1:
            break
    return int(index)

# -----=====| CONST |=====-----

# Logging
C_LOG_LEVEL = logging.INFO
C_TQDM_ASCII = '.#'         # just beauty

# Encoder
C_ENC_STR = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$%*+-./:'
C_PAD_CHAR = ' '
C_CHUNK_SIZE = 11
C_OFT_BSIZE = 2
C_RUNID_BSIZE = 4
C_BNUM_BSIZE = 4

# Markers & data blocks
C_ARUCO_DICT = cv2.aruco.DICT_5X5_50
C_DATA_CSIZE = 195          # max alphanumeric for version 6 QR
C_DOT_SPACING = 3           # just beauty
C_COLNUM = 5
C_ROWNUM = 7
C_QR_VER = 6
C_QR_CORR = 1               # Low
C_QR_SPACING = 7            # minimal
C_MIN_MPER_RATE = 1e-9      # temporary solution
C_MARKER_COORD = ((0, 1), (1, 2), (2, 3), (3, 0))

# Font
C_FONT = 'Courier-Bold'
C_FONT_SIZE = 10

# Page geometry
C_PAGE_W = 210              # mm, A4 page
C_PAGE_H = 297              # mm, A4 page
C_LEFT_M = 25               # mm
C_RIGHT_M = 25              # mm
C_TOP_M = 20                # mm
C_LINE_H = 5                # mm

# -----

CC_PAW_SIZE = (4 * C_QR_VER) + 17
CC_CELL_SIZE = CC_PAW_SIZE + C_QR_SPACING
CC_PAGE_WIDTH = CC_CELL_SIZE * C_COLNUM + C_QR_SPACING
CC_PAGE_HEIGHT = CC_CELL_SIZE * C_ROWNUM + C_QR_SPACING
CC_DOT_CENT = floor(C_QR_SPACING / 2)
CC_DECODING_DICT = {charc: numr for numr, charc in enumerate(C_ENC_STR)}
CC_BASIS = len(C_ENC_STR)
CC_RUNID_MAX = (CC_BASIS ** C_RUNID_BSIZE) - 1
CC_BMAX = (CC_BASIS ** C_BNUM_BSIZE) - 1
CC_CAPACITY = CC_BASIS ** C_CHUNK_SIZE
CC_BIT_CHUNK = calculate_bit_chunk()
CC_LOSS_PC = (CC_CAPACITY - (2 ** CC_BIT_CHUNK)) / CC_CAPACITY * 100
CC_HASH_SIZE = calculate_hash_size()
CC_MIN_CSIZE = C_RUNID_BSIZE + (C_BNUM_BSIZE * 2) + CC_HASH_SIZE
CC_LEFT_MARGIN = C_LEFT_M * mm
CC_BYTE_CSIZE = int(CC_BIT_CHUNK / 8) + 1
CC_CONTENT_W = C_PAGE_W - C_LEFT_M - C_RIGHT_M

C_HELP_DESC = (
    f'pawpyrus {__version__}: Minimalist paper data storage '
    + 'based on QR codes'
    )
C_HELP_EPILOG = f'Bug tracker: {__bugtracker__}'
C_HELP_JOBNAME = 'Job name. Will be printed in page header. Required.'
C_HELP_IFILE = 'File to encode, or "-" to read from stdin. Required.'
C_HELP_IMAGES = 'Paper storage scans to decode.'
C_HELP_OFILE = 'PDF file to save. Required.'
C_HELP_CODES = 'Files with lists of QR codes content, gathered manually.'
C_HELP_DECODED = 'File to save decoded data. Required.'
C_HELP_DEBUG = 'Directory where to collect debug data if necessary.'
C_HELP_ENC = 'Encode data as paper storage PDF file'
C_HELP_DEC = 'Decode data from paper storage scans'

C_SVG_ROOT_O = (
    f'<svg width="{C_PAGE_W}mm" height="{C_PAGE_H}mm" viewBox="0 0'
    + f' {C_PAGE_W} {C_PAGE_H}" version="1.1" '
    + 'xmlns="http://www.w3.org/2000/svg">'
    + '<path style="fill:#000000;stroke:none;fill-rule:evenodd" d="'
    )

C_PDF_CREDITS = f'pawpyrus {__version__}. Available at: {__repository__}'

# -----=====| LOGGING |=====-----

logging.basicConfig(format='[%(levelname)s] %(message)s', level=C_LOG_LEVEL)

debug_data = json.dumps({
    'Encoding string':     C_ENC_STR,
    'Padding char':        C_PAD_CHAR,
    'Basis':               CC_BASIS,
    'Char chunk size':     C_CHUNK_SIZE,
    'Bits chunk size':     CC_BIT_CHUNK,
    'Offset block size':   C_OFT_BSIZE,
    'Max offset':          CC_BASIS ** C_OFT_BSIZE,
    'Efficiency loss [%]': CC_LOSS_PC,
    'Run ID Block Size':   C_RUNID_BSIZE,
    'Run ID Range':        [0, CC_RUNID_MAX],
    'Block Num Size':      C_BNUM_BSIZE,
    'Max Blocks':          CC_BMAX,
    'Hash block size':     CC_HASH_SIZE,
    'Min data chunk size': CC_MIN_CSIZE
}, indent=4)
logging.debug('Alpha encoder metadata: %s', debug_data)

# -----=====| ALPHANUMERIC ENCODING |=====-----

def encode_int(intnum, char_size): #
    '''
    Encode integer to alphanumeric string
    '''
    line = str()
    for index in range(char_size):
        powbi1 = CC_BASIS ** (index + 1)
        powbi = CC_BASIS ** index
        line += C_ENC_STR[int(intnum % powbi1 / powbi)]
    return line

def decode_int(code):
    '''
    Decode alphanumeric string to integer
    '''
    char_size = len(code)
    intnum = 0
    for index in range(char_size):
        intnum += CC_DECODING_DICT[code[index]] * (CC_BASIS ** index)
    return intnum

def encode_info(raw_data, runid_float, chunk_size=None):
    '''
    Encode byte string to a set of alphanumeric chunks
    '''
    if chunk_size is None:
        chunk_size = CC_MIN_CSIZE
    if chunk_size < CC_MIN_CSIZE:
        raise ValueError('Too small chunk size')
    # Create output struct
    result = {'RunID': None, 'Hash': None, 'Length': None, 'Codes': []}
    # Run ID: unique program run identifier
    runid_int = int(CC_RUNID_MAX * runid_float)
    result['RunID'] = hex(runid_int)[2:].zfill(len(hex(CC_RUNID_MAX)[2:]))
    runid = encode_int(runid_int, C_RUNID_BSIZE)
    # Compute data hash
    hash_obj = sha256(raw_data)
    result['Hash'] = hash_obj.hexdigest()
    hash_int = int.from_bytes(hash_obj.digest(), 'little')
    hashi = encode_int(hash_int, CC_HASH_SIZE)
    # Encode data
    bit_array = bitarray(endian='little')
    bit_array.frombytes(raw_data)
    offset = CC_BIT_CHUNK - (len(bit_array) % CC_BIT_CHUNK)
    bit_array.extend(bitarray('0' * offset, endian='little'))
    line = str()
    for index in range(0, len(bit_array), CC_BIT_CHUNK):
        intnum = int.from_bytes(bit_array[index:index + CC_BIT_CHUNK], 'little')
        line += encode_int(intnum, C_CHUNK_SIZE)
    line += encode_int(offset, C_OFT_BSIZE)
    pure_chunk_size = chunk_size - C_RUNID_BSIZE - C_BNUM_BSIZE
    # Encode length
    blocks_positions = range(0, len(line), pure_chunk_size)
    result['Length'] = int(len(blocks_positions) + 1)
    if result['Length'] >= CC_BMAX:
        raise OverflowError('Too many blocks')
    length = encode_int(result['Length'], C_BNUM_BSIZE)
    # Create chunks
    zero_bnum = encode_int(0, C_BNUM_BSIZE)
    newblock = (runid + zero_bnum + length + hashi).ljust(chunk_size, C_PAD_CHAR)
    result['Codes'].append(newblock)
    for index, item in enumerate(blocks_positions):
        bnumber = encode_int(index + 1, C_BNUM_BSIZE)
        data_chunk = line[item:item + pure_chunk_size]
        newblock1 = (runid + bnumber + data_chunk).ljust(chunk_size, C_PAD_CHAR)
        result['Codes'].append(newblock1)
    return result

def extract_data(line):
    '''
    Extract RunID, block index, and data chunk from alphanumeric string
    '''
    runid = hex(decode_int(line[: C_RUNID_BSIZE]))
    runid = runid[2:].zfill(len(hex(CC_RUNID_MAX)[2:]))
    index = decode_int(line[C_RUNID_BSIZE : C_RUNID_BSIZE + C_BNUM_BSIZE])
    content = line[C_RUNID_BSIZE + C_BNUM_BSIZE :].rstrip(C_PAD_CHAR)
    return {'RunID': runid, 'Index': index, 'Content': content}

def extract_metadata(content):
    '''
    Extract data length and hash from alphanumeric header block
    '''
    length_ = decode_int(content[: C_BNUM_BSIZE])
    hash_ = decode_int(content[C_BNUM_BSIZE : C_BNUM_BSIZE + CC_HASH_SIZE])
    hash_ = hash_.to_bytes(32, 'little').hex().zfill(64)
    return {'Length': length_, 'Hash': hash_}

def decode_info(codes):
    '''
    Decode alphanumeric chunks
    '''
    result = []
    # Extract blocks
    extracted = [extract_data(line) for line in codes]
    extracted = {item['Index']: item for item in extracted}
    # Check header
    try:
        header = extracted[0]
    except KeyError as exc:
        raise RuntimeError('No root block in input data!') from exc
    # Extract metadata
    metadata = extract_metadata(header['Content'])
    # Check blocks
    missing_blocks = []
    for index in range(1, metadata['Length']):
        try:
            if extracted[index]['RunID'] != header['RunID']:
                raise RuntimeError('Some blocks are not of this header')
            result.append(extracted[index]['Content'])
        except KeyError:
            missing_blocks.append(str(index))
    if missing_blocks:
        raise RuntimeError(
            f'Some blocks are missing: {"; ".join(missing_blocks)}'
            )
    # Decode
    code = ''.join(result)
    output_data = {
        'RunID': str(header['RunID']),
        'Blocks': int(metadata['Length']),
        'Hash': str(metadata['Hash']),
        'Data': None
        }
    bit_array = bitarray(endian='little')
    offset = decode_int(code[-C_OFT_BSIZE:])
    encoded_data = code[:-C_OFT_BSIZE]
    for index in range(0, len(encoded_data), C_CHUNK_SIZE):
        intnum = decode_int(encoded_data[index:index + C_CHUNK_SIZE])
        new_bits = bitarray(endian='little')
        new_bits.frombytes(intnum.to_bytes(CC_BYTE_CSIZE, byteorder='little'))
        bit_array.extend(new_bits[:CC_BIT_CHUNK])
    bit_array = bit_array[:-offset]
    output_data['Data'] = bit_array.tobytes()
    if sha256(output_data['Data']).hexdigest() != output_data['Hash']:
        raise RuntimeError('Data damaged (hashes are not the same)')
    return output_data

# -----=====| PAWPRINTS |=====-----

# QR Code
def tomcat_pawprint(data):
    '''
    Create data-containing QR matrix
    '''
    wrapped_data = QRData(data.encode('ascii'), mode=MODE_ALPHA_NUM)
    qr_code = QRCode(version=C_QR_VER, error_correction=C_QR_CORR, border=0)
    qr_code.add_data(wrapped_data)
    qr_code.make(fit=False)
    matrix = numpy.array(qr_code.get_matrix())
    matrix = numpy.vectorize(int)(matrix)
    return matrix

# ArUco Marker
def kitty_pawprint(aruco_index):
    '''
    Create ArUco marker matrix
    '''
    matrix = cv2.aruco.getPredefinedDictionary(C_ARUCO_DICT)
    matrix = matrix.generateImageMarker(aruco_index, C_QR_SPACING)
    matrix = numpy.vectorize(lambda x: int(not bool(x)))(matrix)
    return matrix

def create_pixel_sheets(codes):
    '''
    Create pixel array from data-containing QRs and ArUco markers matrices
    '''
    # Create output list
    result = []
    # Chunk codes to rows and pages
    page_data = list(sliced(list(sliced(codes, C_COLNUM)), C_ROWNUM))

    for page_number, page in enumerate(page_data):
        # Create page
        matrix = numpy.zeros((CC_PAGE_HEIGHT, CC_PAGE_WIDTH))
        tqdm_total = sum(len(item) for item in page)
        tqdm_desc = f'Create pawprints, page {page_number + 1} of {len(page_data)}'
        for row, col in tqdm(product(range(C_ROWNUM), range(C_COLNUM)),
                             total=tqdm_total, desc=tqdm_desc, ascii=C_TQDM_ASCII):
            try:
                # Create pawprint on the page
                start_x = (C_QR_SPACING * 2) + (CC_CELL_SIZE * col)
                start_y = (C_QR_SPACING * 2) + (CC_CELL_SIZE * row)
                pawprint = tomcat_pawprint(page[row][col])
                startspx = start_x + CC_PAW_SIZE
                startspy = start_y + CC_PAW_SIZE
                matrix[start_y:startspy, start_x:startspx] = pawprint
            except IndexError:
                # If there are no codes left
                break
        # Create dot margin (beauty, no functionality)
        matrix[CC_DOT_CENT, C_QR_SPACING + 2::C_DOT_SPACING] = 1
        cell_p = CC_CELL_SIZE * len(page)
        matrix[C_QR_SPACING + 2:cell_p:C_DOT_SPACING, CC_DOT_CENT] = 1
        # Create markers
        grid = {
            0: (0, 0),
            1: (CC_CELL_SIZE * C_COLNUM, 0),
            2: (0, cell_p),
            3: (CC_CELL_SIZE, 0)
            }
        for index, item in grid.items():
            itemsp = (item[0] + C_QR_SPACING, item[1] + C_QR_SPACING)
            matrix[item[1]:itemsp[1], item[0]:itemsp[0]] = kitty_pawprint(index)
        # Append page
        result.append(matrix)
    # Return
    return result

# -----=====| DRAW |=====-----

# numpy 2D array to black pixel coordinates
def matrix_to_pixels(matrix):
    '''
    Convert matrices to a list of pixels
    '''
    pcoord = product(range(matrix.shape[0]), range(matrix.shape[1]))
    result = [(crdx, crdy) for crdy, crdx in pcoord if matrix[crdy][crdx]]
    return result

def draw_svg_node (crdx, crdy, pixel_size):
    '''
    Draw SVG node
    '''
    corner1 = C_LEFT_M + (crdx * pixel_size)
    corner2 = C_TOP_M + (5 * C_LINE_H) + (crdy * pixel_size)
    corner3 = C_LEFT_M + ((crdx + 1) * pixel_size)
    corner4 = C_TOP_M + (5 * C_LINE_H) + ((crdy + 1) * pixel_size)
    return (
        f'M {corner1:.3f},{corner2:.3f} '
        + f'H {corner3:.3f} V {corner4:.3f} H {corner1:.3f} Z'
        )

def draw_svg(pixel_sheets):
    '''
    Create SVG from a list of pixels
    '''
    svg_pages = []
    drawing_width = pixel_sheets[0].shape[1]
    pixel_size = CC_CONTENT_W / drawing_width
    logging.debug('Pixel Size: %.3f mm', pixel_size)
    for page_number, page_matrix in enumerate(pixel_sheets):
        # Create Pixels
        page = matrix_to_pixels(page_matrix)
        # Draw page
        svg_page = [C_SVG_ROOT_O]
        paths = []
        # Add Pixels
        tqdm_desc = f'Draw pixels, page {page_number + 1} of {len(pixel_sheets)}'
        for crdx, crdy in tqdm(page, total=len(page), desc=tqdm_desc,
                               ascii=C_TQDM_ASCII):
            paths.append(draw_svg_node (crdx, crdy, pixel_size))
        svg_page.append(' '.join(paths))
        svg_page.append('">')
        svg_page.append('</svg>')
        # Merge svg
        svg_pages.append(''.join(svg_page))
    return svg_pages


def calc_line_tm(rownum):
    '''
    Calculate text line top coordinate
    '''
    return (C_PAGE_H - C_TOP_M - (C_LINE_H * rownum)) * mm

def create_pdf(dataset, svg_pages, output_file_name, job_name):
    '''
    Convert SVGs to a PDF file
    '''
    canvas_pdf = canvas.Canvas(output_file_name)
    timestamp = str(datetime.now().replace(microsecond=0))
    tqdm_desc = 'Convert pages to PDF'
    for page_number, page in tqdm(enumerate(svg_pages), total=len(svg_pages),
                                  desc=tqdm_desc, ascii=C_TQDM_ASCII):
        # Set font
        canvas_pdf.setFont(C_FONT, C_FONT_SIZE)
        # Convert SVG page
        object_page = svg2rlg(StringIO(page))
        # Captions
        jn_caption = f'Name: {job_name}'
        info_caption = (
            f'{timestamp}, run ID: {dataset["RunID"]}, {dataset["Length"]} '
            + f'blocks, page {page_number + 1} of {len(svg_pages)}'
            )
        hash_caption = f'SHA-256: {dataset["Hash"]}'
        canvas_pdf.drawString(CC_LEFT_MARGIN, calc_line_tm(1), jn_caption)
        canvas_pdf.drawString(CC_LEFT_MARGIN, calc_line_tm(2), info_caption)
        canvas_pdf.drawString(CC_LEFT_MARGIN, calc_line_tm(3), hash_caption)
        canvas_pdf.drawString(CC_LEFT_MARGIN, calc_line_tm(4), C_PDF_CREDITS)
        # Draw pawprints
        renderPDF.draw(object_page, canvas_pdf, 0, 0)
        # Newpage
        canvas_pdf.showPage()
    # Save pdf
    canvas_pdf.save()

# -----=====| DETECTION |=====-----

def find_center(coord_block):
    '''
    Calculate block center
    '''
    return (
        coord_block[0][0] + ((coord_block[2][0] - coord_block[0][0]) / 2),
        coord_block[0][1] + ((coord_block[2][1] - coord_block[0][1]) / 2)
        )

def decode_qr(barcode):
    '''
    Decode a single QR code
    '''
    result = {'Contents': None, 'Detected': {}}
    # pyzbar
    code = decode(barcode)
    if code:
        result['Contents'] = str(code[0].data.decode('ascii'))
        result['Detected']['pyzbar'] = True
    else: result['Detected']['pyzbar'] = False
    # opencv
    detector = cv2.QRCodeDetector()
    code = detector.detectAndDecode(barcode)[0]
    if code:
        if result['Contents'] is not None:
            if result['Contents'] != code:
                raise RuntimeError(
                    'Different decoding results: '
                    + f'OpenCV = {code}, PyZBar = {result["Contents"]}'
                    )
        else:
            result['Contents'] = str(code)
        result['Detected']['opencv'] = True
    else:
        result['Detected']['opencv'] = False
    return result


def read_page(file_name, debug_dir, file_index):
    '''
    Read a page: detect markers, align grid, detect, and decode single QRs
    '''
    # Read and binarize image
    picture = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
    threshold, picture = cv2.threshold(picture, 0, 255,
                                       cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # -----DEBUG-----
    if debug_dir is not None:
        debug_array = cv2.cvtColor(numpy.copy(picture), cv2.COLOR_GRAY2RGB)
    # ---------------

    logging.info('Image binarized (threshold: %.1f)', threshold)
    # Detect markers
    aruco_dict = cv2.aruco.getPredefinedDictionary(C_ARUCO_DICT)
    aruco_params = cv2.aruco.DetectorParameters()
    aruco_params.minMarkerPerimeterRate = C_MIN_MPER_RATE
    markers = cv2.aruco.detectMarkers(picture, aruco_dict,
                                      parameters=aruco_params)
    # Check markers
    if markers is None:
        raise RuntimeError('No markers were found')

    # -----DEBUG-----
    if debug_dir is not None:
        for item in range(len(markers[1])):
            for line_start, line_end in C_MARKER_COORD:
                tup_ls = tuple(int(i) for i in markers[0][item][0][line_start])
                tup_le = tuple(int(i) for i in markers[0][item][0][line_end])
                cv2.line(debug_array, tup_ls, tup_le, (255, 0, 0), 4)
            m_title = f'id={markers[1][item][0]}'
            title_coord = (
                int(markers[0][item][0][0][0]),
                int(markers[0][item][0][0][1]) - 20
                )
            cv2.putText(debug_array, m_title, title_coord,
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
    # ---------------

    # Check markers
    markers = { int(markers[1][item][0]): {'Coords': markers[0][item][0]}
                for item in range(len(markers[1])) }
    if tuple(sorted(markers.keys())) != (0, 1, 2, 3):
        raise RuntimeError('Some markers were not found')
    # Align grid
    marker_length = dist(markers[0]['Coords'][0], markers[0]['Coords'][1])
    for item in markers:
        markers[item]['Center'] = find_center(markers[item]['Coords'])
    width = dist(markers[0]['Center'], markers[1]['Center'])
    height = dist(markers[0]['Center'], markers[2]['Center'])
    cell_size = dist(markers[0]['Center'], markers[3]['Center'])
    col_num, row_num = round(width / cell_size), round(height / cell_size)
    logging.info('Layout detected: %d x %d', col_num, row_num)
    cell_size_x, cell_size_y = width / col_num, height / row_num
    vector_x = (
        (markers[1]['Center'][0] - markers[0]['Center'][0]) / width,
        (markers[1]['Center'][1] - markers[0]['Center'][1]) / width
        )
    vector_y = (
        (markers[2]['Center'][0] - markers[0]['Center'][0]) / height,
        (markers[2]['Center'][1] - markers[0]['Center'][1]) / height
        )
    for item in markers:
        markers[item]['Center'] = (
            markers[item]['Center'][0] + (marker_length * vector_x[0]),
            markers[item]['Center'][1] + (marker_length * vector_y[1])
            )
    # chunking by grid
    chunks = []
    cells = product(range(col_num), range(row_num))
    for cell_x, cell_y in cells:
        coord_start = markers[0]['Center']
        fullvec_x = tuple(item * cell_size_x for item in vector_x)
        fullvec_y = tuple(item * cell_size_y for item in vector_y)
        corners = (
            (cell_x, cell_y),
            (cell_x + 1, cell_y),
            (cell_x + 1, cell_y + 1),
            (cell_x, cell_y + 1)
            )
        chunk = [[
            coord_start[0] + (itemx * fullvec_x[0]) + (itemy * fullvec_y[0]),
            coord_start[1] + (itemx * fullvec_x[1]) + (itemy * fullvec_y[1])
            ] for itemx, itemy in corners]
        cell_xs = [itemx for itemx, itemy in chunk]
        cell_ys = [itemy for itemx, itemy in chunk]
        fragment = picture[
            round(min(cell_ys)):round(max(cell_ys)),
            round(min(cell_xs)):round(max(cell_xs))
            ]
        chunks.append({
            'Cell': (int(cell_x) + 1, int(cell_y) + 1),
            'Coords': chunk,
            'Image': fragment
            })
    # Detect and decode
    codes = []
    for chunk in tqdm(chunks, total=len(chunks), desc='Detect QR codes',
                      ascii=C_TQDM_ASCII):
        code = decode_qr(chunk['Image'])
        if code['Contents'] is not None:
            color = (0, 255, 0)
            codes.append(code)
        else:
            color = (0, 0, 255)

        # -----DEBUG-----
        if debug_dir is not None:
            if not code:
                base_name = (
                    f'unrecognized.page-{file_index}.'
                    + f'x-{chunk["Cell"][0]}.y-{chunk["Cell"][1]}.jpg'
                    )
                cv2.imwrite(join(debug_dir, base_name), chunk['Image'])
            for line_start, line_end in C_MARKER_COORD:
                tup_ls = tuple(int(i) for i in chunk['Coords'][line_start])
                tup_le = tuple(int(i) for i in chunk['Coords'][line_end])
                cv2.line(debug_array, tup_ls, tup_le, (255, 0, 0), 4)
            chunk_title = f'({chunk["Cell"][0]},{chunk["Cell"][1]})'
            title_coord = (
                int(chunk['Coords'][3][0]) + 10,
                int(chunk['Coords'][3][1]) - 30
                )
            cv2.putText(debug_array, chunk_title, title_coord,
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 4)
        # ---------------

    # -----DEBUG-----
    if debug_dir is not None:
        d_pagefile = join(debug_dir, f'page-{file_index}.jpg')
        cv2.imwrite(d_pagefile, debug_array)
    # ---------------

    return codes

# -----=====| ENCODE MAIN |=====-----

def encode_main(job_name, input_file_name, output_file_name):
    '''
    Encoder main function
    '''
    logging.info('pawpyrus %s Encoder', __version__)
    logging.info('Job Name: %s', job_name)
    if input_file_name == '-':
        logging.info('Input File: <stdin>')
    else:
        logging.info('Input File: "%s"', realpath(input_file_name))
    logging.info('Output File: "%s"', realpath(output_file_name))
    # Read rawdata
    if input_file_name == '-':
        raw_data = sys.stdin.buffer.read()
    else:
        with open(input_file_name, 'rb') as stream:
            raw_data = stream.read()
    # Create codes dataset
    dataset = encode_info(raw_data, random(), C_DATA_CSIZE)
    logging.info('Run ID: %s', dataset['RunID'])
    logging.info('SHA-256: %s', dataset['Hash'])
    logging.info('Blocks: %d', dataset['Length'])
    # Create pixelsheets
    pages = create_pixel_sheets(dataset['Codes'])
    # Draw SVG
    svg_pages = draw_svg(pages)
    # Draw PDF
    create_pdf(dataset, svg_pages, output_file_name, job_name)
    logging.info('Job finished')


# -----=====| DECODE MAIN |=====-----

def detect_counter(annotated_blocks, opencv_d, pyzbar_d):
    '''
    Statictic function: counts detected blocks by source
    '''
    result = []
    for block in annotated_blocks:
        odet, pdet = block['Detected']['opencv'], block['Detected']['pyzbar']
        result.append((odet == opencv_d) and (pdet == pyzbar_d))
    return result.count(True)

def decode_main(masked_image_input, text_input, debug_dir, output_file_name):
    '''
    Decoder main function
    '''
    image_input = []
    if masked_image_input is not None:
        for i in masked_image_input:
            image_input.extend([realpath(f) for f in glob(i)])
        image_input = sorted(list(set(image_input)))
    if (not image_input) and (text_input is None):
        raise ValueError('Input is empty: no images, no text!')
    logging.info('pawpyrus %s Decoder', __version__)

    # -----DEBUG-----
    if debug_dir is not None:
        logging.warning('DEBUG MODE ON')
        mkdir(debug_dir)
    # ---------------

    if image_input:
        logging.info('Image Input File(s): %s', ', '.join(image_input))
    if text_input is not None:
        logging.info('Text Input File: %s', realpath(text_input))
    logging.info('Output File: %s', realpath(output_file_name))
    annotated_blocks = []
    for file_index, file_name in enumerate(image_input):
        logging.info('Processing "%s"', file_name)
        annotated_blocks.extend(read_page(file_name, debug_dir, file_index + 1))

    # -----DEBUG-----
    if debug_dir is not None:
        detection_stats = {
            'total': len(annotated_blocks),
            'pyzbar_only': detect_counter(annotated_blocks, False, True),
            'opencv_only': detect_counter(annotated_blocks, True, False),
            'both': detect_counter(annotated_blocks, True, True),
            'neither': detect_counter(annotated_blocks, False, False)
            }
        dstats_filename = join(debug_dir, 'detection_stats.json')
        with open(dstats_filename, 'wt', encoding='utf-8') as out_stream:
            json.dump(detection_stats, out_stream, indent=4)
    # ---------------

    blocks = [block['Contents'] for block in annotated_blocks]
    if text_input is not None:
        with open(text_input, 'rt', encoding='utf-8') as text_file:
            tlines = text_file.readlines()
        blocks += [Line.rstrip('\n').rstrip(C_PAD_CHAR) for Line in tlines]
        blocks = [Line for Line in blocks if Line]

    # -----DEBUG-----
    if debug_dir is not None:
        b_filename = join(debug_dir, 'blocks.txt')
        with open(b_filename, 'wt', encoding='utf-8') as blocks_file:
            blocks_file.write('\n'.join(blocks))
    # ---------------

    result = decode_info(blocks)
    logging.info('Run ID: %s', result['RunID'])
    logging.info('Blocks: %d', result['Blocks'])
    logging.info('SHA-256: %s', result['Hash'])
    with open(output_file_name, 'wb') as out:
        out.write(result['Data'])
    logging.info('Job finished')


## ------======| PARSER |======------

def create_parser():
    '''
    Create CLI arguments parser
    '''
    default_parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=C_HELP_DESC,
        epilog=C_HELP_EPILOG
        )
    default_parser.add_argument('-v', '--version', action='version',
                                version=__version__)
    subparsers = default_parser.add_subparsers(title='Commands', dest='command')
    # Encode parser
    encode_p = subparsers.add_parser('Encode', help=C_HELP_ENC)
    encode_p.add_argument('-n', '--name', required=True, type=str,
                          dest='job_name', help=C_HELP_JOBNAME)
    encode_p.add_argument('-i', '--input', required=True, type=str,
                          dest='input_file',  help=C_HELP_IFILE)
    encode_p.add_argument('-o', '--output', required=True, type=str,
                          dest='output_file', help=C_HELP_OFILE)
    # Decode parser
    decode_p = subparsers.add_parser('Decode', help=C_HELP_DEC)
    decode_p.add_argument('-i', '--image', nargs='*', type=str,
                          dest='image_input', help=C_HELP_IMAGES)
    decode_p.add_argument('-t', '--text', type=str, default=None,
                          dest='text_input', help=C_HELP_CODES)
    decode_p.add_argument('-o', '--output', required=True, type=str,
                          dest='output_file', help=C_HELP_DECODED)
    decode_p.add_argument('-d', '--debug-dir', type=str, default=None,
                          dest='debug_dir', help=C_HELP_DEBUG)
    return default_parser

# -----=====| MAIN |=====-----

def main():
    '''
    Main function (entrypoint)
    '''
    parser = create_parser()
    ns = parser.parse_args(sys.argv[1:])
    if ns.command == 'Encode':
        encode_main(ns.job_name, ns.input_file, ns.output_file)
    elif ns.command == 'Decode':
        decode_main(ns.image_input, ns.text_input, ns.debug_dir, ns.output_file)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
