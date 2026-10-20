import os
import re
import json

TAIL = {"См. также", "Примечания", "Литература", "Ссылки"}


def read_article(path):
    with open(path, encoding="utf-8") as f:
        title = f.readline().strip()
        text = f.read()
    return title, text


def remove_formulas(text):
    kept = []
    for line in text.split("\n"):
        if line.startswith("  "):
            continue
        kept.append(line)
    return "\n".join(kept)


def cut_tail(text):
    kept = []
    for line in text.split("\n"):
        if line.startswith("==") and line.strip("= ") in TAIL:
            break
        kept.append(line)
    return "\n".join(kept)


def clean(text):
    text = remove_formulas(text)
    text = cut_tail(text)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.strip()


def split_sentences(paragraph):
    return re.split(r"(?<=[.!?])\s+", paragraph)


def make_chunks(title, text, max_chars=800, min_chars=80):
    chunks = []
    section = "Введение"
    buffer = ""

    for line in text.split("\n"):
        line = line.strip()
        if line == "":
            continue
        if line.startswith("=="):
            if len(buffer) >= min_chars:
                chunks.append({"title": title, "section": section, "text": buffer})
            buffer = ""
            section = line.strip("= ")
            continue

        for piece in split_sentences(line):
            if buffer != "" and len(buffer) + len(piece) + 1 > max_chars:
                if len(buffer) >= min_chars:
                    chunks.append({"title": title, "section": section, "text": buffer})
                buffer = ""
            if buffer == "":
                buffer = piece
            else:
                buffer = buffer + " " + piece

    if len(buffer) >= min_chars:
        chunks.append({"title": title, "section": section, "text": buffer})
    return chunks


if __name__ == "__main__":
    all_chunks = []
    for name in sorted(os.listdir("data")):
        path = os.path.join("data", name)
        title, text = read_article(path)
        text = clean(text)
        chunks = make_chunks(title, text)
        print(name, title, "->", len(chunks))
        all_chunks.extend(chunks)

    for i, c in enumerate(all_chunks):
        c["id"] = i

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=1)
    print("всего:", len(all_chunks))