from slugify import slugify


def addAnchors(input):

    # assumes list input and returns list

    # Will add an anchor above every header that starts with a number.
    # These headers get stripped in the Markdown conversion, as apparently
    # anchors can't start with leading digits.  This works Ok for
    # toc generation, as pandoc adds in the auto-identifiers.  But for
    # internal wiki links, I have lots of links using [](#20150213-heading),
    # and these anchors don't get generate correctly.

    b = []

    for line in input:
        if (line) and (line[0] == '#'):  # line may be blank (index would fail)
            link = line.lstrip('# ')
            if (link) and (link[0].isdigit()):  # same here
                anchor = '<a id=' + slugify(link, '-') + '></a>'
                b.append(anchor)
                b.append('\n')  # pandoc expects blank line before header
        b.append(line)
    return b
