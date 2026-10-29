def decode_message(text):
    if type(text) is not str:
        raise ValueError("Vhod mora biti niz (str)")
    if len(text) > 60:
        raise ValueError("Vhod je daljši od 60 znakov")

    LIMIT = 120
    stack = []   # (besedilo pred skupino, ponovitve)
    cur = ""     # besedilo trenutne ravni
    i = 0
    while i < len(text):
        ch = text[i]
        if "a" <= ch <= "z":
            cur += ch
        elif "1" <= ch <= "9":
            if i + 1 >= len(text) or text[i + 1] != "[":
                raise ValueError(f"Števka mora stati neposredno pred '[' (mesto {i})")
            stack.append((cur, int(ch)))
            cur = ""
            i += 2
            continue
        elif ch == "]":
            if not stack:
                raise ValueError(f"Odvečen zaklepaj na mestu {i}")
            prev, k = stack.pop()
            cur = prev + cur * k
        elif ch == "[":
            raise ValueError(f"Oklepaj brez števke na mestu {i}")
        else:
            raise ValueError(f"Neveljaven znak {ch!r} na mestu {i}")
        # Nič se ne krajša, zato prekoračitev kjerkoli pomeni prekoračitev rezultata.
        if len(cur) > LIMIT:
            raise ValueError("Dekodirani rezultat presega 120 znakov")
        i += 1

    if stack:
        raise ValueError("Nezaprt oklepaj")
    return cur


# --- Testi ---
assert decode_message("3[ab]c") == "abababc"
assert decode_message("2[a3[b]]") == "abbbabbb"

try:
    decode_message("3[ab")
    assert False, "Pričakovan ValueError"
except ValueError:
    pass
