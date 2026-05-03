def rabin_karp_search(text, pattern):
    matches = []
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return matches

    d = 256
    q = 101
    pattern_hash = 0
    window_hash = 0
    h = 1

    for _ in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        window_hash = (d * window_hash + ord(text[i])) % q

    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            if text[i:i + m] == pattern:
                matches.append(i)

        if i < n - m:
            window_hash = (d * (window_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if window_hash < 0:
                window_hash += q

    return matches


text = "AABAACAADAABAABA"
pattern = "AABA"
result = rabin_karp_search(text, pattern)
print("Rabin Karp Matches:", result)
