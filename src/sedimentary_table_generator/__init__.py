from PIL import Image, ImageDraw, ImageFont

class __tableSettings:
	def __init__(self) -> None:
		self.top_header_vertical_padding_modifier = 0.5  # Modifies the height of the top header
		self.left_header_width = 'auto'  # If set to "auto", the width will be adapted to the text
		self.cell_width = 'auto'
		self.cell_height = 'auto'

		self.padding = 10  # The padding between text and the table when calculating "auto" values
		self.title_top_padding = 5  # Padding above title
		self.title_bottom_padding = 20  # Padding between title and table

		self.alternating_background_color = 100, 100, 100
		self.image_background_color = 0, 0, 0, 0
		
		self.border_thickness = 1
		self.border_color = 0, 0, 0

		self.body_background_color = 255, 255, 255
		self.top_header_background_color = 40, 40, 40
		self.left_header_background_color = 40, 40, 40

		self.title_text_color = 0, 0, 0
		self.left_header_text_color = 220, 220, 220
		self.top_header_text_color = 220, 220, 220
		self.body_text_color = 0, 0, 0

		self.title_text_size = 35
		self.header_text_size = 20
		self.body_text_size = 20

		self.title_font = ''  # Fonts must be truetype (.ttf) files
		self.header_font = ''
		self.body_font = ''

		self.color_mode = 'RGBA'
		self.fallback_to_bundled_font = True  # If the font can't be loaded, fallback to one of Pillow's bundled fonts


ts = __tableSettings()

def draw_table(rows, left_header=None, top_header=None, title=None, filename=None):
	# Init fonts
	fonts = {}
	def load_font(name, location, size):
		try:
			fonts[name] = ImageFont.truetype(location, size)
		except OSError:
			if ts.fallback_to_bundled_font:
				if location == '':
					print(f"The font file for the {name} text wasn't defined, switching to fallback font")
				else:
					print(f'The font file for the {name} text (defined as "{location}") cannot be opened, most likely because the file does not exist; switching to fallback font')
				fonts[name] = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', size)
			else:
				if location == '':
					raise OSError(f"The font file for the {name} text wasn't defined")
				raise OSError(f'The font file for the {name} text (defined as "{location}") cannot be opened, most likely because the file does not exist')

	load_font('title', ts.title_font, ts.title_text_size)
	load_font('header', ts.header_font, ts.header_text_size)
	load_font('body', ts.body_font, ts.body_text_size)

	# Misc stuff
	num_body_rows = len(rows)
	num_body_columns = len(rows[0])

	if top_header is not None:
		num_total_rows = num_body_rows + 1  # (top header)
	else:
		num_total_rows = num_body_rows
	if left_header is not None:
		num_total_columns = num_body_columns + 1  # (left header)
	else:
		num_total_columns = num_body_columns

	if left_header is not None:
		left_header_text_sizes = [fonts['header'].getlength(str(i)) for i in left_header]
		if ts.left_header_width == 'auto':
			left_header_width = round(max(left_header_text_sizes) + ts.padding * 2)
		else:
			left_header_width = ts.left_header_width
	else:
		left_header_text_sizes = [0]
		left_header_width = 0
	if ts.cell_height == 'auto':
		cell_height = max(ts.header_text_size, ts.body_text_size) + ts.padding * 2
	else:
		cell_height = ts.cell_height
	if top_header is not None:
		top_header_height = cell_height - round(ts.padding * 2 * (1 - ts.top_header_vertical_padding_modifier))
		top_header_text_lengths = [fonts['header'].getlength(str(i)) for i in top_header]
	else:
		top_header_height = 0
		top_header_text_lengths = [0]
	if ts.cell_width == 'auto':
		body_text_lengths = [fonts['body'].getlength(str(i)) for i in [item for sublist in rows for item in sublist]]  # I have no idea what's going on here, this line scares me
		body_cell_width = round(max(body_text_lengths + top_header_text_lengths) + ts.padding * 2)
	else:
		body_cell_width = ts.cell_width
	if title is not None:
		title_width, title_height = fonts['body'].getsize(str(title))
		title_width, title_height = round(title_width), round(title_height)
		title_total_height = ts.title_bottom_padding + title_height + ts.title_top_padding
	else:
		title_width, title_height, title_total_height = 0, 0, 0


	top_header_border_height = ts.border_thickness if top_header is not None else 0
	left_header_border_width = ts.border_thickness if left_header is not None else 0

	main_table_width = (num_body_columns + 1) * ts.border_thickness + left_header_border_width + left_header_width + body_cell_width * num_body_columns
	xres = main_table_width if main_table_width > title_width else title_width
	if title_width > main_table_width:
		global_x_offset = (title_width - main_table_width) // 2
	else:
		global_x_offset = 0
	yres = title_total_height + top_header_border_height + (num_body_rows + 1) * ts.border_thickness + top_header_height + num_body_rows * cell_height
	im = Image.new(ts.color_mode, (xres, yres), ts.image_background_color)
	d = ImageDraw.Draw(im)

	# ======= Draw Rects =======
	# Top header
	d.rectangle((global_x_offset + left_header_width + ts.border_thickness, title_total_height + ts.border_thickness, xres - 1 - global_x_offset, title_total_height + top_header_height + ts.border_thickness), ts.top_header_background_color)
	# Left header
	d.rectangle((global_x_offset + ts.border_thickness, title_total_height + top_header_height + ts.border_thickness + top_header_border_height, global_x_offset + ts.border_thickness + left_header_width, yres - 1), ts.left_header_background_color)
	# Body
	d.rectangle((global_x_offset + left_header_width + ts.border_thickness, title_total_height + top_header_height + ts.border_thickness + top_header_border_height, xres - 1 - global_x_offset, yres - 1), ts.body_background_color)
	# Alternating colored-rows
	if ts.alternating_background_color is not None:
		for i in range(num_body_rows):
			if (i + 1) % 2 == 0:
				sx = global_x_offset + left_header_width + ts.border_thickness
				sy = title_total_height + ts.border_thickness + top_header_border_height + top_header_height + i * (cell_height + ts.border_thickness)
				ex = xres - 1 - global_x_offset
				ey = title_total_height + top_header_border_height + top_header_height + (i + 1) * (cell_height + ts.border_thickness)
				d.rectangle((sx, sy, ex, ey), ts.alternating_background_color)

	# ======= Draw lines =======
	line_origin_offset = (ts.border_thickness - 1 if ts.border_thickness % 2 == 0 else ts.border_thickness) // 2  # Pillow draws lines with the "origin" in the center, this offsets it to the top/left
	# Draw horizontal lines
	for i in range(num_total_rows + 1):
		line_x_start = global_x_offset if (i > 0 or top_header is None) else global_x_offset + left_header_width + ts.border_thickness
		if i == 0:
			line_y = line_origin_offset + title_total_height
		elif top_header is not None and i == 1:
			line_y = line_origin_offset + title_total_height + top_header_height + top_header_border_height
		elif top_header is None:
			line_y = line_origin_offset + title_total_height + top_header_height + top_header_border_height + i * (cell_height + ts.border_thickness)
		else:
			line_y = line_origin_offset + title_total_height + top_header_height + top_header_border_height + (i - 1) * (cell_height + ts.border_thickness)
		d.line((line_x_start, line_y, xres - 1 - global_x_offset, line_y), ts.border_color, ts.border_thickness)
	
	# Draw vertical lines
	for i in range(num_total_columns + 1):
		line_y_start = title_total_height + ts.border_thickness if i > 0 else title_total_height + top_header_height + line_origin_offset + top_header_border_height
		if left_header is not None and i == 0:
			line_x = global_x_offset + line_origin_offset
		elif top_header is not None and i == 1:
			line_x = global_x_offset + line_origin_offset + left_header_width + ts.border_thickness
		elif left_header is None:
			line_x = global_x_offset + line_origin_offset + left_header_width + left_header_border_width + i * (body_cell_width + ts.border_thickness)
		else:
			line_x = global_x_offset + line_origin_offset + ts.border_thickness + left_header_width + (i - 1) * (body_cell_width + ts.border_thickness)
		d.line((line_x, line_y_start, line_x, yres - 1), ts.border_color, ts.border_thickness)

	# ======= Draw text =======
	# Top header
	if top_header is not None:
		for column in range(len(top_header)):
			x = global_x_offset + left_header_border_width + left_header_width + ts.border_thickness + column * (ts.border_thickness + body_cell_width) + body_cell_width // 2
			y = title_total_height + ts.border_thickness + top_header_height // 2
			d.text((x, y), str(top_header[column]), ts.top_header_text_color, fonts['header'], 'mm')
	
	# Left header
	if left_header is not None:
		for row in range(len(left_header)):
			x = global_x_offset + ts.border_thickness + left_header_width // 2
			y = title_total_height + top_header_border_height + top_header_height + ts.border_thickness + row * (ts.border_thickness + cell_height) + cell_height // 2
			d.text((x, y), str(left_header[row]), ts.left_header_text_color, fonts['header'], 'mm')
	
	# Body text
	for column in range(num_body_columns):
		for row in range(num_body_rows):
			x = global_x_offset + left_header_border_width + left_header_width + ts.border_thickness + column * (ts.border_thickness + body_cell_width) + body_cell_width // 2
			y = title_total_height + top_header_border_height + top_header_height + ts.border_thickness + row * (ts.border_thickness + cell_height) + cell_height // 2
			d.text((x, y), str(rows[row][column]), ts.body_text_color, fonts['body'], 'mm')
	
	# Title
	if title is not None:
		d.text((global_x_offset + xres // 2, ts.title_top_padding + title_height // 2), str(title), ts.title_text_color, fonts['title'], 'mm')

	# ======= Save / Return =======
	if filename is not None:
		im.save(filename)
	
	return im
