def chunked(sequence, n):
    """Returns an iterator which produces chunks from the sequence of size n."""
    chunk = []

    for index, item in enumerate(sequence):
        chunk.append(item)

        if (index + 1) % n == 0:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
