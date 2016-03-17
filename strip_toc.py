
def stripToc(input):

    # Assume input list split at lines

    str_beg = '<!-- MarkdownTOC -->'
    str_end = '<!-- /MarkdownTOC -->'

    b = []
    toc = False

    for line in input:
        if line == str_beg:
            toc = True
        elif line == str_end:
            toc = False
            continue
        if (not toc):
            b.append(line)
    return b
