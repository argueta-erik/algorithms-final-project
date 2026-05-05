def naive_search_with_count(text, pattern):
	matches = [] # empty list
	comparisons = 0

	n = len(text)
	m = len(pattern)

	if m == 0:
		return matches, comparisons
	if m > n:	# means it will never match
		return matches, comparisons

	for i in range(n - m + 1):
		found = True
		for j in range(m):
			comparisons += 1

			if text[i + j] != pattern[j]:
				found = False
				break
			if found:
				matches.append(i)
	return matches, comparisons

#text = "AAAAAABAAAAABAAAAABAAAA"
#pattern = "AAAAAAB"
text= "AABAACAADAABAABA"
pattern = "AABA"
matches, comparisons = naive_search_with_count(text, pattern)
print("Naive Search Matches:", matches)
print("Naive Comparisons:", comparisons)

