def sliding_window(lst, window_size):
  current_batch = []
  for e in lst:
    if len(current_batch) == window_size:
      yield current_batch
      current_batch = []
    current_batch.append(e)

  if current_batch:
    yield current_batch

