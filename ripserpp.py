import numpy as np
import io
import subprocess
import os


def vietoris_rips_filteration(distance_matrix, dimension, verbose=False, ripserpp_bin_path="./build/ripser++"):
  ripserpp_bin_path = os.environ.get('RIPSERPP_BIN_PATH', ripserpp_bin_path)
  if not ripserpp_bin_path  \
     or not os.path.exists(ripserpp_bin_path) \
     or not os.path.isfile(ripserpp_bin_path):
    raise Exception("Path to Ripser++ binary is not set!")
  if not np.allclose(distance_matrix, distance_matrix.T):
    raise Exception("Not a distance matrix!")
  if not np.all(np.diag(distance_matrix) == 0):
    raise Exception("Not a Distance Matrix!")
  devnull = None if verbose else open(os.devnull, "w")
  ipipe = io.StringIO()
  np.savetxt(ipipe, distance_matrix)
  proc = subprocess.Popen(
      [ripserpp_bin_path, "--format", "distance", "--dim", str(dimension)],
      stdout=subprocess.PIPE,
      stdin=subprocess.PIPE,
      stderr=devnull)
  ipipe.seek(0)
  proc.stdin.write(ipipe.read().encode("utf-8"))
  opipe = io.StringIO(proc.communicate()[0].decode("utf-8"))
  proc.stdin.close()
  return np.loadtxt(opipe).astype(np.int32)
