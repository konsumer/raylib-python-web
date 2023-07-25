def struct_clone(source, a):
    if not a:
        a = _mod._malloc(source.size)
    _mod._memcpy(a, source._address, source.size)
    out = source.__class__(address=a, to_alloc=False)
    return out