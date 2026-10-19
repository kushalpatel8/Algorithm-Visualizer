def longest_substring_k_distinct(s, k):
    n = len(s)
    char_count = {}
    left = 0
    max_len = 0
    
    for right in range(n):
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
            yield left, right, max_len
            
        max_len = max(max_len, right - left + 1)
        yield left, right, max_len