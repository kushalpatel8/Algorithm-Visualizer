def boyer_moore(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0 or m > n:
        return
        
    bad_char = {}
    for i in range(m):
        bad_char[pattern[i]] = i
        
    s = 0
    while s <= n - m:
        j = m - 1
        yield s, s + j, j, "inspect", f"Align at shift {s}: Starting right-to-left scan from pattern[{j}] ('{pattern[j]}')", {"bad_char": bad_char}
        
        while j >= 0 and pattern[j] == text[s + j]:
            yield s, s + j, j, "match", f"Right-to-left match: text[{s + j}] == pattern[{j}] ('{pattern[j]}')", {"bad_char": bad_char}
            j -= 1
            
        if j < 0:
            yield s, s, -1, "found", f"Pattern matched at index {s}!", {"bad_char": bad_char, "found_at": s}
            shift = (m - bad_char.get(text[s + m], -1)) if s + m < n else 1
            s += shift
            if s <= n - m:
                yield s, s, -1, "shift", f"Shifted pattern by {shift} to position {s}", {"bad_char": bad_char}
        else:
            mismatched_char = text[s + j]
            last_pos = bad_char.get(mismatched_char, -1)
            shift = max(1, j - last_pos)
            yield s, s + j, j, "mismatch", f"Mismatch: text[{s + j}] ('{mismatched_char}') != pattern[{j}] ('{pattern[j]}'). Shift = max(1, {j} - {last_pos}) = {shift}", {"bad_char": bad_char}
            s += shift
            if s <= n - m:
                yield s, s, -1, "shift", f"Shifted pattern by {shift} to position {s}", {"bad_char": bad_char}