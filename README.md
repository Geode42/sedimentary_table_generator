# Sedimentary Table Generator

## Requirements
- [Pillow](https://pypi.org/project/Pillow)

...that's it.

## What is it?
This is a relatively small package that allows you to generate tables, and save them as a .png file (or whatever other filetype you want).

## Example
``` Python
from sedimentary_table_generator import *

rows = [
	['a', 1],
	['b', 2],
	['c', 3]]

left_header = ['Row 1', 'Row 2', 'Row 3']
top_header = ['Letters', 'Numbers']
title = 'Letter Indexes'

ts.border_color = 255, 0, 0
ts.border_thickness = 3
ts.alternating_colors = 120, 120, 120

draw_table(rows, left_header, top_header, title, filename='table.png')
```
**Explanation:**
- `ts.border_color = 255, 0, 0` (+2 lines after it): The table generator has 26 settings, all of which are contained within "`ts`". When the function is run, it gets all of its settings from this object. So, whenever you want to change some formatting, simply type "`ts.`" plus whatever attribute you want to modify, and set that equal to a value.
- `draw_table(rows, left_header, top_header, title, filename='table.png')`: This function actually draws the table. It can take four values, `rows`, `left_header`, `top_header`, `title`, and `filename`, which should be pretty self explanatory. Note that only `rows` is required, the other three are optional. See the example above for well, an example.

**Note:** The `draw_table` function always returns the PIL image. If `filename` is specified, it saves the table to that filename as well.

## All Table Settings
``` Python
top_header_vertical_padding_modifier = 0.5  # Modifies the height of the top header
left_header_width = 'auto'  # If set to "auto", the width will be adapted to the text
cell_width = 'auto'
cell_height = 'auto'

padding = 10  # The padding between text and the table when calculating "auto" values
title_top_padding = 5  # Padding above title
title_bottom_padding = 20  # Padding between title and table

alternating_background_color = 100, 100, 100
image_background_color = 0, 0, 0, 0
		
border_thickness = 1
border_color = 0, 0, 0

body_background_color = 255, 255, 255
top_header_background_color = 40, 40, 40
left_header_background_color = 40, 40, 40

title_text_color = 0, 0, 0
left_header_text_color = 220, 220, 220
top_header_text_color = 220, 220, 220
body_text_color = 0, 0, 0

title_text_size = 35
header_text_size = 20
body_text_size = 20

title_font = ''  # Fonts must be truetype (.ttf) files
header_font = ''
body_font = ''

color_mode = 'RGBA'
fallback_to_bundled_font = True  # If the font can't be loaded, fallback to one of Pillow's bundled fonts
```