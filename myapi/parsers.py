from html.parser import HTMLParser
import copy 


class TableCollector(HTMLParser):
    '''
    Parses an html document and collects all table elements
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.tables = []     
        self.tag_count = 0
        self.curr = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.tag_count += 1
        if bool(self.tag_count):
            self.curr += f'<{tag}'
            for attr in attrs:
                self.curr += f' {attr[0]}="{attr[1]}"'
            self.curr += '>'

    def handle_data(self, data):
        if bool(self.tag_count):
            self.curr += data

    def handle_endtag(self, tag):
        if tag == 'table':
            self.tag_count -= 1
            if not self.tag_count:
                self.curr += '</table>'
                self.tables.append(self.curr)
                self.curr = ''
        if bool(self.tag_count):
            self.curr += f'</{tag}>'

class TableParser(HTMLParser):
    '''
    Parses an html table and stores table elements in an array
    '''
    def __init__(self, html):
        HTMLParser.__init__(self)

        self.parsed_rows = []
        self.row = []
        self.cell = self.Cell()
        self.tall_cells = []
        self.curr_row_tall_cells = []

        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'style' in attrs:
            style = self.style_str_to_dict(attrs['style'])
            self.cell.set_style(style)
        if tag == 'br':
            self.cell.data += '\n'
        if tag in ['td', 'th']:
            self.cell.set_attrs(attrs)

    def handle_data(self, data):
        if self.cell.data and self.cell.data[-1] not in [' ','(','[','{','$','\n'] and data[0] != ' ':
            self.cell.data += f' {data}'
        else:
            self.cell.data += data

    def handle_endtag(self, tag):
        if tag == 'div':
            self.cell.data += '\n'

        if tag in ['td', 'th']:
            self.cell.data = self.cell.data.strip()
            width = self.cell.attrs['colspan']
            for _ in range(width):
                self.row.append(self.cell)
            if self.cell.attrs['rowspan'] > 1:
                self.curr_row_tall_cells.append(self.cell)
            self.cell = self.Cell('', {}, {}, 
                                  self.cell.col + width, 
                                  self.cell.row)

        if tag == 'tr':
            curr_row = self.cell.row
            self.tall_cells = [cell for cell in self.tall_cells if 
                               (cell.row + cell.attrs['rowspan'] - curr_row) >= 1]
            for cell in self.tall_cells:
                width = cell.attrs['colspan']
                for _ in range(width):
                    self.row.insert(cell.col, cell)
                for curr_cell in set(self.row[cell.col+width:]):
                    curr_cell.col += width

            self.parsed_rows.append(self.row)
            self.tall_cells += self.curr_row_tall_cells
            self.row = []
            self.curr_row_tall_cells =[]
            self.cell.row += 1
            self.cell.col = 0

    def style_str_to_dict(self, style_str):
        style = {}
        kv_pairs = style_str.split(';')
        for kv_pair in kv_pairs:
            if len(kv_pair.split(':')) == 2:
                k, v = kv_pair.split(':')
                style[k.strip()] = v.strip()
        return style

    class Cell:
        def __init__(self, data='', attrs={}, style={}, col=0, row=0):
            self.data = data
            self.attrs = attrs
            self.style = style
            self.col = col
            self.row = row

        def __repr__(self):
            data = self.data.split('\n')
            return f'{data}'

        def set_attrs(self, attrs):
            self.attrs['colspan'] = int(attrs['colspan']) if 'colspan' in attrs else 1
            self.attrs['rowspan'] = int(attrs['rowspan']) if 'rowspan' in attrs else 1

        def set_style(self, style):
            attrs = ['text-align', 'vertical-align', 'font-weight', 'line-height']
            for attr in attrs:
                py_attr = attr.replace('-','_')
                if attr in style:
                    if attr == 'font-weight' and 'font_weight' in self.style:
                        if 'bold' in [self.style['font_weight'], style['font-weight']]:
                            self.style['font_weight'] = 'bold'
                        else:
                            self.style['font_weight'] = max(self.style['font_weight'], style['font-weight'])
                    else:
                        self.style[py_attr] = style[attr]
