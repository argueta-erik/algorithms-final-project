def naive_search(text, pattern):
	matches = [] # empty list
	n = len(text)
	m = len(pattern)
	comparisons = 0

	if m == 0:
		return matches
	if m > n:	# means it will never match
		return matches

	for i in range(n - m + 1):		# text.length - pattern.length + 1 ; meaning:
		found = True
		for j in range(m):
			comparisons += 1
#			print(f"text[{i} + {j}] ?= pattern[{j}]")
#			print(f"{text[ i + j]} ?= {pattern[j]}")

			if text[i + j] != pattern[j]:
#				print("No Match...")
				found = False
#				print()
				break

			if found:
#				print("MATCH")
				matches.append(i)
#				print(f"Appending i ({i}) to matches...")
#				print(f"Current Matches: {matches}")
#				print("\n")

	return matches, comparisons

text = "AABAACAADAABAABA"
pattern = "AABA"
result, comparisons = naive_search(text, pattern)
#print("====================================================")
#print("RESULTS:")
#print(f"Text: AABAACAADAABAABA; Length: {len(text)}")
#print(f"Pattern = AABA; Length: {len(pattern)}")
print("Naive Search Matches:", result)
print("Total Comparisons: ", comparisons)
