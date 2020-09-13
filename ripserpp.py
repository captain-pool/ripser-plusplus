import numpy as np
import io
import subprocess
import os
import shlex
import sys

def write_ltm(matrix, f):
  with open(f, "w") as f:
    x, y = np.tril_indices_from(matrix, -1)
    a = x[0]
    for idx in range(len(x)):
      pair = x[idx], y[idx]
      if a != pair[0]:
        f.write("\n")
        a = pair[0]
      f.write("%f," % matrix[pair])

def vietoris_rips_filteration(distance_matrix, dimension, verbose=False, pyripser_pp_bin="/rpp/python/build/libpyripser++.so"):
    pyripser_pp_bin = os.environ['PYRIPSER_PP_BIN'] = os.environ.get('PYRIPSER_PP_BIN', pyripser_pp_bin)
    sys.path.append(os.path.dirname(os.path.dirname(pyripser_pp_bin)))
    import ripser_plusplus_python as rppp
    rppp.run("--format distance --dim %d" % dimension, distance_matrix)
    return np.loadtxt("/tmp/features.txt").astype(np.int32)


def vietoris_rips_filteration_slow(distance_matrix, dimension, verbose=False, ripserpp_bin_path="/rpp/build/ripser++"):
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
  write_ltm(distance_matrix.astype("float16"), "/tmp/distmat.txt")
  command = ripserpp_bin_path + " --dim %d /tmp/distmat.txt" % dimension
  command = shlex.split(command)
  proc = subprocess.Popen(
      command,
      stdout=subprocess.PIPE,
      stderr=devnull)
  opipe = io.BytesIO(proc.communicate()[0])
  #ipipe.seek(0)
  #proc.stdin.write(ipipe.read())
  return np.loadtxt(opipe).astype(np.int32)
