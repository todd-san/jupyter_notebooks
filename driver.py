import frf_pch

# file_path = 'data/sort1/'
# file_name = 'deck'

file_path = 'data/'
file_name = 'handle'


deck = []
data = []


try:
	raw_deck = open(str(file_path)+(file_name)+str('.dat'))
	for row in raw_deck:
		deck.append(row[:-1])
		if 'BEGIN BULK' in row:
			break
except IOError:
	print 'INFO: did not load input deck'
	pass

try:
	raw_data = open(str(file_path)+(file_name)+str('.pch'))
	for row in raw_data:
		data.append(row[:-1])
except IOError:
	print 'INFO: did not load punch file'
	pass

result = frf_pch.PCH(input_pch=data, input_deck=deck)

print '====================================================================='
print '| Solution {} '.format(result.sol)
print '---------------------------------------------------------------------'
print '|             Subcases: {}'.format(result.sub)
print '|      Punched Set IDs: {}'.format(result.output_set)
print '|           Value Type: {}'.format(result.output_types)
print '|          File Format: {}'.format(result.format)
print '====================================================================='


