def rabin_karp(text, pattern):
    d = 256
    q = 101
    n = len(text)
    m = len(pattern)
    if m == 0 or m > n:
        return
        
    h = pow(d, m - 1, q)
    p = 0
    t = 0
    
    for k in range(m):
        p = (d * p + ord(pattern[k])) % q
        t = (d * t + ord(text[k])) % q
        
    for i in range(n - m + 1):
        yield i, i, -1, "hash_check", f"Window [{i}..{i + m - 1}]: Text Hash = {t}, Pattern Hash = {p}", {"text_hash": t, "pattern_hash": p}
        
        if p == t:
            all_match = True
            for k in range(m):
                if text[i + k] == pattern[k]:
                    yield i, i + k, k, "match", f"Hash matched! Verifying: text[{i + k}] == pattern[{k}] ('{pattern[k]}')", {"text_hash": t, "pattern_hash": p}
                else:
                    yield i, i + k, k, "mismatch", f"Hash collision! text[{i + k}] ('{text[i + k]}') != pattern[{k}] ('{pattern[k]}')", {"text_hash": t, "pattern_hash": p}
                    all_match = False
                    break
            if all_match:
                yield i, i + m - 1, m - 1, "found", f"Pattern matched at index {i}!", {"text_hash": t, "pattern_hash": p, "found_at": i}
                
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
            yield i + 1, i + 1, -1, "shift", f"Rolling hash to window [{i + 1}..{i + m}]: new hash = {t}", {"text_hash": t, "pattern_hash": p}