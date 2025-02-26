from IPython.display import display, HTML
import sys




def render(content):
	display(content)
	

def asHTML(content):
	render(HTML(content))


def toStdout(content):
	sys.stdout.write(str(content))


def toStderr(content):
	sys.stderr.write(str(content))

def asHTMLTable(headers, rows):

	html_header = ''
	for header in headers:
		html_header += f'<th>{header}</th>'
	html_header = f'<tr>{html_header}</tr>'

	html_rows = ''
	for row in rows:
		_row = ''
		for col in row:
			_row += f'<td>{col}</td>'
		_row = f'<tr>{_row}</tr>'
		html_rows += _row
	asHTML(f'<table>{html_header} {html_rows}</table>')