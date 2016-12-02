"""

"""

import numpy as np


class PCH(object):

	def __init__(self, input_pch, input_deck=None):

		if input_deck:
			for row in input_deck:
				if 'SOL' in row:
					self.sol =  row.split(' ')[1]
			self.sub, self.format, self.output_types, self.output_set =\
				self.get_pch_request_from_deck(deck=input_deck)


		if input_pch and not input_deck:
			self.sol = float('NaN')
			self.sub = self.get_subcases_from_punch(pch=input_pch)

	def get_pch_request_from_deck(self, deck):
		output_format   = []
		output_types    = []
		output_sets     = []
		output_subcases = []

		for i, row in enumerate(deck):
			if 'PUNCH' in row:
				if 'SORT2' in row:
					o_format = 2
				else:
					o_format = 1

				requested_subcase, requested_set = self.get_request_subcase(deck=deck, request=[i, row])
				output_subcases.append(int(requested_subcase))
				output_format.append(o_format)
				output_types.append(row.strip().split('(')[0])
				output_sets.append(int(requested_set))

		return list(set(output_subcases)), list(set(output_format)), list(set(output_types)), list(set(output_sets))

	def get_request_subcase(self, deck, request):
		subcase = float('NaN')
		subcase_set = request[1].split(' ')[-1]

		for i in range(request[0], 0, -1):
			if 'SUBCASE' in deck[i]:
				subcase_line = deck[i]
				break
			else:
				pass

		subcase = subcase_line.strip().split()[-1]

		return subcase, subcase_set

	def get_subcases_from_punch(self, pch):
		subcases = []
		all_header_rows = []
		for row in pch:
			if 'SUBCASE' in row:
				subcases.append(int(row.strip().split()[-2]))

		return list(set(subcases))


class FRF_PCH(object):

	def __init__(self, input):
		self.header, self.output_sets, self.num_ds = self.read_header(input)
		self.length = len(input)

		self.format = self.format_switch()

	def read_header(self, input):
		header = []
		count = []
		extra_lines = []
		read_header = 0

		for i, row in enumerate(input):
			if row[0] == '$' and read_header == 0:
				header.append(row)
			elif i > 0 and input[i-1][0] == '$':
				count.append(i)
				read_header = 1
			elif i > 0 and row[0] == '-':
				read_header = 1
				if input[i-1][0] == ' ':
					extra_lines.append(i)
			else:
				read_header = 1
				pass

		num_ds = np.diff(extra_lines)

		# header_count = []
		# for val in num_ds:
		# 	if val!=


		output_sets = len(set(np.diff(count)))
		return header, output_sets, num_ds

	def format_switch(self):

		if 'POINT' in self.header[-1]:
			format = 2
		elif 'FREQ' in self.header[-1]:
			format = 1
		else:
			format = float('NaN')
		return format

