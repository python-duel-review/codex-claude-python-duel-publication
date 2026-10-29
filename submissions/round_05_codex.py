def decode_message(text):
    if not isinstance(text, str) or len(text) > 60:
        raise ValueError("Vhod mora biti niz z največ 60 znaki.")

    stack = []
    result = ""
    i = 0
    while i < len(text):
        char = text[i]
        if "a" <= char <= "z":
            result += char
        elif "1" <= char <= "9":
            if i + 1 >= len(text) or text[i + 1] != "[":
                raise ValueError("Enomestnemu številu mora neposredno slediti [.")
            stack.append((result, int(char)))
            result = ""
            i += 1
        elif char == "]":
            if not stack:
                raise ValueError("Odvečen zaklepaj.")
            prefix, count = stack.pop()
            result = prefix + result * count
        else:
            raise ValueError("Neveljaven znak ali sintaksa.")

        if len(result) > 120:
            raise ValueError("Dekodirani rezultat presega 120 znakov.")
        i += 1

    if stack:
        raise ValueError("Manjkajoč zaklepaj.")
    return result


# Test 1: zaporedne skupine in navadne črke.
assert decode_message("3[ab]c2[d]") == "abababcdd"

# Test 2: gnezdenje, prazne skupine in prazen niz.
assert decode_message("2[a3[b]]3[]") == "abbbabbb"
assert decode_message("") == ""

# Test 3: napačna sintaksa, predolg rezultat in neveljaven tip.
for invalid in ("10[a]", "2[a", "[a]", "0[a]", "A", "9[9[aa]]", True):
    try:
        decode_message(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError(f"Pričakovan ValueError za {invalid!r}.")
