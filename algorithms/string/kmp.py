def compute_lps(pattern, m, lps):
    length = 0
    lps[0] = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0 or m > n:
        return
        
    lps = [0] * m
    compute_lps(pattern, m, lps)
    
    i = 0  # text index
    j = 0  # pattern index
    
    while i < n:
        shift = i - j
        if text[i] == pattern[j]:
            yield shift, i, j, "match", f"Matching: text[{i}] ('{text[i]}') == pattern[{j}] ('{pattern[j]}')", {"lps": list(lps)}
            i += 1
            j += 1
            if j == m:
                found_idx = i - m
                yield found_idx, i - 1, m - 1, "found", f"Pattern found at index {found_idx}!", {"lps": list(lps), "found_at": found_idx}
                j = lps[j - 1]
                if i < n:
                    yield i - j, i, j, "shift", f"LPS skip: pattern aligned at shift {i - j} using lps[{m - 1}]={j}", {"lps": list(lps)}
        else:
            yield shift, i, j, "mismatch", f"Mismatch: text[{i}] ('{text[i]}') != pattern[{j}] ('{pattern[j]}')", {"lps": list(lps)}
            if j != 0:
                old_j = j
                j = lps[j - 1]
                yield i - j, i, j, "shift", f"LPS skip: pattern shifted from j={old_j} to j={j} (lps[{old_j - 1}]={j})", {"lps": list(lps)}
            else:
                i += 1
                if i < n:
                    yield i, i, 0, "shift", f"Shifted pattern to text index {i}", {"lps": list(lps)}