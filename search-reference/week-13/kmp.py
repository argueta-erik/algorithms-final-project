def build_lps(pattern):
# example:
# pattern = "ababaca"
# lps = [0, 0, 1, 2, 3, 0, 1]		// representation
# creating a length matching the length of the pattern
# lps: Longest Prefix Suffix
#	It helps algo avoid redundant comparisons; if mismatch, LPS tells algo how many characters of pattern can be "reused" to skip ahead
	lps = [0] * len(pattern)	# len stores length of prefix
	length = 0
	i = 1

	while i < len(pattern):

#		print(f"{pattern[i]} ?= {pattern[length]}")

		if pattern[i] == pattern[length]:
#			print("MATCH!")
			length+= 1
			lps[i] = length
			i += 1
		else:	# if mismatch, two cases; defining failure function as in the slides
			if length != 0:
				length = lps[length - 1]
			else:
				lps[i] = 0
				i += 1		# so far, we are doing the transition of the while loop
	return lps


def kmp_search(text, pattern):
	if pattern == "":		# this code will help in project; make sure you are doing exception handling as well; program should not be crashing
		return []
	lps = build_lps(pattern)	# pre-processing done bc we defined it at the top...
	matches = []
	i = 0
	j = 0

	while i < len(text):
		# when successful match; move search window
		if text[i] == pattern[j]:
			i += 1
			j += 1
		if j == len(pattern):
			matches.append(i - j)
			j = lps[j - 1]
		elif i < len(text) and text[i] != pattern[j]:	# mismatch
			if j != 0:
				j = lps[j - 1]
			else:
				i += 1
	return matches



# Creating data to test
text = "aabbabaabaabca"
pattern = "aabaabc"
print("text = 'abbabaabaabca' ;  pattern = 'abaabc'")
lps_table = build_lps(pattern)
result = kmp_search(text, pattern)
print("Text  :", text)
print("Pattern  :", pattern)
print("LPS  :", lps_table)
print("Matches found at indices:   ", result)

