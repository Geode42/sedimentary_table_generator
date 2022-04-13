from PIL import Image, ImageDraw, ImageFont

class __tableSettings:
	def __init__(self) -> None:
		self.left_header_width = 'auto'  # If set to "auto", the width will be adapted to the text
		self.cell_width = 'auto'
		self.cell_height = 'auto'
		self.min_body_cell_width = None
		self.min_left_header_cell_width = None
		self.min_cell_height = None
		self.center_top_label_if_top_left_cell_is_occupied = False
		self.center_left_label_if_top_left_cell_is_occupied = False

		self.vertical_padding = 20  # The padding between text and the table when calculating "auto" values
		self.horizontal_padding = 20
		self.left_header_horizontal_padding_modifier = 1.5
		self.top_header_vertical_padding_modifier = 0.5  # Modifies the height of the top header
		self.title_top_padding = 20  # Padding above title
		self.title_table_padding = 40  # Padding between title and table (if top label isn't present)
		self.title_label_padding = 20  # Padding between title and top label
		self.top_label_bottom_padding = 20
		self.top_of_image_top_label_padding = 20  # Padding between the top of the image and the top label (if there's no title)
		self.left_label_right_padding = 20
		self.left_label_left_padding = 20
		self.image_right_padding = 0

		self.alternating_background_color = 130, 130, 130
		self.header_alternating_background_color = 20, 20, 20
		self.image_background_color = 255, 255, 255
		
		self.border_thickness = 1
		self.border_color = 0, 0, 0

		self.body_background_color = 255, 255, 255
		self.top_header_background_color = 40, 40, 40
		self.left_header_background_color = 40, 40, 40

		self.title_text_color = 0, 0, 0
		self.label_text_color = 0, 0, 0
		self.left_header_text_color = 220, 220, 220
		self.top_header_text_color = 220, 220, 220
		self.body_text_color = 0, 0, 0

		self.title_text_size_modifier = 1.75  # Every other text size is based on the body text size
		self.label_text_size_modifier = 1.25
		self.header_text_size_modifier = 1
		self.body_text_size = 20

		self.title_font = ''  # Fonts must be truetype (.ttf) files
		self.label_font = ''
		self.header_font = ''
		self.body_font = ''

		self.color_mode = 'RGBA'
		self.fallback_to_bundled_font = True  # If the font can't be loaded, fallback to one of Pillow's bundled fonts


ts = __tableSettings()

def draw_table(rows, left_header=None, top_header=None, left_label=None, top_label=None, title=None, filename=None):
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

	title_text_size = round(ts.body_text_size * ts.title_text_size_modifier)
	label_text_size = round(ts.body_text_size * ts.label_text_size_modifier)
	header_text_size = round(ts.body_text_size * ts.header_text_size_modifier)

	load_font('title', ts.title_font, title_text_size)
	load_font('top-label', ts.label_font, label_text_size)
	fonts['left-label'] = ImageFont.TransposedFont(fonts['top-label'], Image.ROTATE_90)
	load_font('header', ts.header_font, header_text_size)
	load_font('body', ts.body_font, ts.body_text_size)

	# Misc stuff
	num_body_rows = len(rows)
	num_body_columns = len(rows[0])

	include_top_left_cell = False
	if top_header is not None:
		num_total_rows = num_body_rows + 1  # (top header)
		if len(top_header) > num_body_columns and left_header is not None:
			include_top_left_cell = True
	else:
		num_total_rows = num_body_rows
	if left_header is not None:
		num_total_columns = num_body_columns + 1  # (left header)
	else:
		num_total_columns = num_body_columns

	if left_header is not None:
		left_header_horizontal_padding = ts.horizontal_padding * ts.left_header_horizontal_padding_modifier
		if ts.left_header_width == 'auto':
			left_header_text_sizes = [fonts['header'].getlength(str(i)) for i in left_header] + ([fonts['header'].getlength(str(top_header[0]))] if include_top_left_cell else [])
			left_header_width = round(max(left_header_text_sizes) + left_header_horizontal_padding * 2)
		else:
			left_header_width = ts.left_header_width
	else:
		left_header_text_sizes = [0]
		left_header_width = 0
	if ts.cell_height == 'auto':
		cell_height = max(header_text_size, ts.body_text_size) + ts.vertical_padding * 2
	else:
		cell_height = ts.cell_height
	if top_header is not None:
		top_header_height = cell_height - round(ts.vertical_padding * 2 * (1 - ts.top_header_vertical_padding_modifier))
		top_header_text_lengths = [fonts['header'].getlength(str(i)) for i in top_header]
	else:
		top_header_height = 0
		top_header_text_lengths = [0]
	if ts.cell_width == 'auto':
		body_text_lengths = [fonts['body'].getlength(str(i)) for i in [item for sublist in rows for item in sublist]]  # I have no idea what's going on here, this line scares me
		body_cell_width = round(max(body_text_lengths + (top_header_text_lengths if not include_top_left_cell else top_header_text_lengths[1:])) + ts.horizontal_padding * 2)
	else:
		body_cell_width = ts.cell_width

	if left_label is not None:
		left_label_width, left_label_height = fonts['left-label'].getsize(str(left_label))
		left_label_width = label_text_size
		left_label_total_width = ts.left_label_left_padding + left_label_width + ts.left_label_right_padding
	else:
		left_label_width, left_label_height = 0, 0
		left_label_total_width = 0
	if top_label is not None:
		top_label_width, top_label_height = fonts['top-label'].getsize(str(top_label))
		top_label_height = label_text_size
		top_label_total_height = top_label_height + ts.top_label_bottom_padding
		if title is None:
			top_label_total_height += ts.top_of_image_top_label_padding
	else:
		top_label_width, top_label_height = 0, 0
		top_label_total_height = 0
	if title is not None:
		title_width, title_height = fonts['title'].getsize(str(title))
		title_width = round(title_width)
		title_height = title_text_size # This way the image height always stays the same, regardless of the title's contents (e.g. "_" would be shorter than "I")
		title_total_height = (ts.title_label_padding if top_label is not None else ts.title_table_padding) + title_height + ts.title_top_padding
	else:
		title_width, title_height, title_total_height = 0, 0, 0
	
	top_area_total_height = title_total_height + top_label_total_height

	# Min values
	if ts.min_body_cell_width is not None and body_cell_width < ts.min_body_cell_width:
		body_cell_width = ts.min_body_cell_width
	if left_header is not None and ts.min_left_header_cell_width is not None and left_header_width < ts.min_left_header_cell_width:
		left_header_width = ts.min_left_header_cell_width
	if ts.min_cell_height is not None and cell_height < ts.min_cell_height:
		cell_height = ts.min_cell_height
		if top_header is not None:
			top_header_height = cell_height - round(ts.vertical_padding * 2 * (1 - ts.top_header_vertical_padding_modifier))

	top_header_border_height = ts.border_thickness if top_header is not None else 0
	left_header_border_width = ts.border_thickness if left_header is not None else 0

	main_table_width = (num_body_columns + 1) * ts.border_thickness + left_header_border_width + left_header_width + body_cell_width * num_body_columns
	xres = left_label_total_width + main_table_width + ts.image_right_padding if main_table_width + left_label_total_width > title_width else title_width + ts.image_right_padding
	if title_width > main_table_width + left_label_total_width:
		global_x_offset = (title_width - main_table_width) // 2 + left_label_total_width
	else:
		global_x_offset = left_label_total_width
	yres = top_area_total_height + top_header_border_height + (num_body_rows + 1) * ts.border_thickness + top_header_height + num_body_rows * cell_height
	im = Image.new(ts.color_mode, (xres, yres), ts.image_background_color)
	d = ImageDraw.Draw(im)

	# ======= Draw Rects =======
	# Top header
	sx = global_x_offset + left_header_width + ts.border_thickness
	if include_top_left_cell:
		sx -= left_header_width + ts.border_thickness
	sy = top_area_total_height + ts.border_thickness
	ex = global_x_offset + main_table_width - 1
	ey = top_area_total_height + top_header_height + ts.border_thickness
	d.rectangle((sx, sy, ex, ey), ts.top_header_background_color)
	# Left header
	d.rectangle((global_x_offset + ts.border_thickness, top_area_total_height + top_header_height + ts.border_thickness + top_header_border_height, global_x_offset + ts.border_thickness + left_header_width, yres - 1), ts.left_header_background_color)
	# Body
	d.rectangle((global_x_offset + left_header_width + ts.border_thickness, top_area_total_height + top_header_height + ts.border_thickness + top_header_border_height, global_x_offset + main_table_width, yres - 1), ts.body_background_color)
	# Alternating colored-rows
	if ts.alternating_background_color is not None:
		for i in range(num_body_rows):
			if (i + 1) % 2 == 0:
				sx = global_x_offset + left_header_width + ts.border_thickness
				sy = top_area_total_height + ts.border_thickness + top_header_border_height + top_header_height + i * (cell_height + ts.border_thickness)
				ex = global_x_offset + main_table_width - 1
				ey = top_area_total_height + top_header_border_height + top_header_height + (i + 1) * (cell_height + ts.border_thickness)
				d.rectangle((sx, sy, ex, ey), ts.alternating_background_color)
	if ts.header_alternating_background_color is not None:
		for i in range(num_body_rows):
			if (i + 1) % 2 == 0:
				sx = global_x_offset + ts.border_thickness
				sy = top_area_total_height + ts.border_thickness + top_header_border_height + top_header_height + i * (cell_height + ts.border_thickness)
				ex = global_x_offset + ts.border_thickness + left_header_width
				ey = top_area_total_height + top_header_border_height + top_header_height + (i + 1) * (cell_height + ts.border_thickness)
				d.rectangle((sx, sy, ex, ey), ts.header_alternating_background_color)

	# ======= Draw lines =======
	line_origin_offset = (ts.border_thickness - 1 if ts.border_thickness % 2 == 0 else ts.border_thickness) // 2  # Pillow draws lines with the "origin" in the center, this offsets it to the top/left
	# Draw horizontal lines
	for i in range(num_total_rows + 1):
		line_x_start = global_x_offset if (i > 0 or top_header is None or include_top_left_cell) else global_x_offset + left_header_width + ts.border_thickness
		if i == 0:
			line_y = line_origin_offset + top_area_total_height
		elif top_header is not None and i == 1:
			line_y = line_origin_offset + top_area_total_height + top_header_height + top_header_border_height
		elif top_header is None:
			line_y = line_origin_offset + top_area_total_height + top_header_height + top_header_border_height + i * (cell_height + ts.border_thickness)
		else:
			line_y = line_origin_offset + top_area_total_height + top_header_height + top_header_border_height + (i - 1) * (cell_height + ts.border_thickness)
		d.line((line_x_start, line_y, global_x_offset + main_table_width - 1, line_y), ts.border_color, ts.border_thickness)
	
	# Draw vertical lines
	for i in range(num_total_columns + 1):
		line_y_start = top_area_total_height + ts.border_thickness if (i > 0 or left_header is None or include_top_left_cell) else top_area_total_height + top_header_height + line_origin_offset + top_header_border_height
		if left_header is not None and i == 0:
			line_x = global_x_offset + line_origin_offset
		elif left_header is not None and i == 1:
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
			if include_top_left_cell:
				x -= body_cell_width + ts.border_thickness
				if column == 0:
					x -= (left_header_width - body_cell_width) // 2
			y = top_area_total_height + ts.border_thickness + top_header_height // 2
			d.text((x, y), str(top_header[column]), ts.top_header_text_color, fonts['header'], 'mm')
	
	# Left header
	if left_header is not None:
		for row in range(len(left_header)):
			x = global_x_offset + ts.border_thickness + left_header_width // 2
			y = top_area_total_height + top_header_border_height + top_header_height + ts.border_thickness + row * (ts.border_thickness + cell_height) + cell_height // 2
			d.text((x, y), str(left_header[row]), ts.left_header_text_color, fonts['header'], 'mm')
	
	# Body text
	for column in range(num_body_columns):
		for row in range(num_body_rows):
			x = global_x_offset + left_header_border_width + left_header_width + ts.border_thickness + column * (ts.border_thickness + body_cell_width) + body_cell_width // 2
			y = top_area_total_height + top_header_border_height + top_header_height + ts.border_thickness + row * (ts.border_thickness + cell_height) + cell_height // 2
			d.text((x, y), str(rows[row][column]), ts.body_text_color, fonts['body'], 'mm')
	
	# Title
	if title is not None:
		d.text((xres // 2, ts.title_top_padding + title_height // 2), str(title), ts.title_text_color, fonts['title'], 'mm')
	
	# Left Label
	if left_label is not None:
		x = global_x_offset - left_label_width - ts.left_label_right_padding
		y = top_area_total_height + top_header_height + (num_body_rows * cell_height + (num_body_rows + 1) * ts.border_thickness) // 2 - left_label_height // 2
		if include_top_left_cell and ts.center_left_label_if_top_left_cell_is_occupied:
			y -= (top_header_height + ts.border_thickness) // 2
		d.text((x, y), str(left_label), ts.label_text_color, fonts['left-label'], 'mm')	
	# Top Label
	if top_label is not None:
		x = global_x_offset + ts.border_thickness * 2 + left_header_width + (num_body_columns * body_cell_width + (num_body_columns + 1) * ts.border_thickness) // 2
		if include_top_left_cell and ts.center_top_label_if_top_left_cell_is_occupied:
			x -= (left_header_width + ts.border_thickness) // 2
		y = top_area_total_height - ts.top_label_bottom_padding
		d.text((x, y), str(top_label), ts.label_text_color, fonts['top-label'], 'ms')

	# ======= Save / Return =======
	if filename is not None:
		im.save(filename)
	
	return im
