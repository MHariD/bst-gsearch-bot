from googlesearch import search


def g_search(query):
    return '\n'.join(search(query, tld="co.in", num=5, stop=5, pause=2))
