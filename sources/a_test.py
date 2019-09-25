import gc

gc.set_debug(gc.DEBUG_SAVEALL)

print(gc.get_count())
lst = []
lst.append(lst)
list_id = id(lst)

print(list_id)

del lst
gc.collect()
for item in gc.garbage:
    print(item)
    assert list_id == id(item)