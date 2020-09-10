import numpy as np
import io
import subprocess
import os

def vietoris_rips_filteration(distance_matrix, dimension, ripserpp_bin_path="./build/ripser++"):
  ripserpp_bin_path = os.envion.get('RIPSERPP_BIN_PATH', ripserpp_bin_dir)
  if not ripserpp_bin_path  \
     or os.path.exists(ripser_bin_path) \
     or not os.path.isifile(ripser_bin_path):
    raise Exception("Path to Ripser++ binary is not set!")
  if not np.allclose(distance_matrix, distance_matrix.T):
    raise Exception("Not a distance matrix!")
  if not np.all(np.diag(distance_matrix) == 0):
    raise Exception("Not a Distance Matrix!")

  ipipe = io.StringIO()
  np.savetxt(ipipe, distance_matrix)
  proc = subprocess.Popen(
      [ripserpp_bin_path, "--format", "distance", "--dim", str(dimension)],
      stdout=subprocess.PIPE,
      stdin=subprocess.PIPE)
  ipipe.seek(0)
  proc.stdin.write(ipipe.read())
  opipe = io.StringIO(proc.communicate()[0])
  proc.stdin.close()
  return np.loadtxt(opipe).astype(np.int32)
