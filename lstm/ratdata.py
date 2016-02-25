from scipy.io import loadmat
import numpy as np

def load_data(features, locations):
  if features.endswith(".mat"):
    X = loadmat(features)
    X = X['mm'].T
  elif features.endswith(".dat"):
    X = np.loadtxt(features)
  elif features.endswith(".npy"):
    X = np.load(features)
  else:
    assert False, "Unknown feature file format"

  if locations.endswith(".mat"):
    y = loadmat(locations)
    y = y['loc'] / 3.5
  elif locations.endswith(".dat"):
    y = np.loadtxt(locations)
  elif locations.endswith(".npy"):
    y = np.load(locations)
  else:
    assert False, "Unknown location file format"

  print "Original data: ", X.shape, y.shape, np.min(X), np.max(X), np.mean(X), np.std(X), np.min(y), np.max(y)
  assert X.shape[0] == y.shape[0], "Number of samples in features and locations does not match"
  return (X, y)

def reshape_data(X, y, seqlen):
  assert X.shape[0] == y.shape[0]
  nsamples = X.shape[0]
  nsamples = int(nsamples / seqlen) * seqlen

  # truncate remaining samples, if not divisible by sequence length
  X = X[:nsamples]
  y = y[:nsamples]

  nb_inputs = X.shape[1]
  nb_outputs = y.shape[1]

  X = np.reshape(X, (-1, seqlen, nb_inputs))
  y = np.reshape(y, (-1, seqlen, nb_outputs))

  print "After reshaping: ", X.shape, y.shape
  return (X, y)

def split_data(X, y, train_set, shuffle):
  assert X.shape[0] == y.shape[0]
  nsamples = X.shape[0]

  if 0 <= train_set <= 1:
    ntrain = int(nsamples * train_set)
    nvalid = nsamples - ntrain
  else:
    ntrain = int(train_set)
    nvalid = nsamples - ntrain

  if shuffle:
    train_idx = np.random.choice(range(nsamples), ntrain, replace=False)
    valid_idx = np.setdiff1d(range(nsamples), train_idx)
  else:
    train_idx = range(ntrain)
    valid_idx = range(ntrain, ntrain + nvalid)

  train_X = X[train_idx]
  train_y = y[train_idx]
  valid_X = X[valid_idx]
  valid_y = y[valid_idx]

  print "After splitting: ", train_X.shape, train_y.shape, valid_X.shape, valid_y.shape
  return (train_X, train_y, valid_X, valid_y)

def add_data_params(parser):
  parser.add_argument("--features", default="1_16_London_RNN_data_2x400_at19_bin100-RAW_feat.dat")
  parser.add_argument("--locations", default="1_16_London_RNN_data_2x400_at19_bin100-RAW_pos.dat")
  parser.add_argument("--train_set", type=float, default=0.9)
  parser.add_argument("--split_shuffle", type=str2bool, default="1")
  parser.add_argument("--seqlen", type=int, default=100)

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
