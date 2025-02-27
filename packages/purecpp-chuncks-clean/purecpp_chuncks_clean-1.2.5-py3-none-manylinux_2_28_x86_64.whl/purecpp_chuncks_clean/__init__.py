import os
import sys
import ctypes
import dependencias_libs
# Descobre o caminho aonde ficou a pasta "lib" do libtorch
# (ajuste conforme a estrutura real quando instalado)
HERE = os.path.join(os.path.dirname(__file__), "..", "..")

lib_dir = os.path.join(HERE, "dependencias_libs", "d_libs", "libtorch", "cpu", "lib")

# Carrega manualmente as bibliotecas necessárias, *antes* de importar o módulo C++
try:
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libaoti_custom_ops.so"))
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libbackend_with_compiler.so"))
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libc10.so"))
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libjitbackend_test.so"))
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libnnapi_backend.so"))
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libshm.so"))
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libtorch.so"))
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libtorch_cpu.so"))
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libtorch_global_deps.so"))
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libtorch_python.so"))
    ctypes.cdll.LoadLibrary(os.path.join(lib_dir, "libtorchbind_test.so"))
    # ... e assim por diante, se houver mais .so que o PyTorch exija
except OSError as e:
    # Se quiser, você pode tratar o erro aqui de forma mais amigável
    raise ImportError(f"Não foi possível carregar libtorch: {e}")

# Só agora importamos o módulo compilado,
# que depende de libtorch.so etc.

from .RagPUREAI_chuncks_clean import *
