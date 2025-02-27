from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess
import shutil

REQUIRED_FILES = [
    "libaoti_custom_ops.so",
    "libbackend_with_compiler.so",
    "libc10.so",
    "libjitbackend_test.so",
    "libnnapi_backend.so",
    "libshm.so",
    "libtorch.so",
    "libtorch_cpu.so",
    "libtorch_global_deps.so",
    "libtorch_python.so",
    "libtorchbind_test.so",
]

def download_libtorch():
    # URL e arquivo zip
    libtorch_cpu_zip = "libtorch-cxx11-abi-shared-with-deps-2.5.1+cpu.zip"
    libtorch_cpu_url = (
        "https://download.pytorch.org/libtorch/cpu/"
        "libtorch-cxx11-abi-shared-with-deps-2.5.1%2Bcpu.zip"
    )
    
    # Caminho base: d_libs/
    pkg_dir = os.path.join(os.path.dirname(__file__), "d_libs")
    libtorch_dir = os.path.join(pkg_dir, "libtorch")
    cpu_dir = os.path.join(libtorch_dir, "cpu")
    lib_path = os.path.join(cpu_dir, "lib")  # É aqui que os .so devem estar

    # 1) Verifica se todos os arquivos necessários já existem
    all_files_present = True
    if os.path.exists(lib_path):
        for f in REQUIRED_FILES:
            if not os.path.exists(os.path.join(lib_path, f)):
                all_files_present = False
                break
    else:
        all_files_present = False

    if all_files_present:
        print("Todos os arquivos requeridos já estão presentes. Pulando download.")
        return
    else:
        print("Nem todos os arquivos estão presentes. Baixando libtorch...")

    # 2) Se faltou algum arquivo, remove tudo e baixa novamente
    if os.path.exists(pkg_dir):
        shutil.rmtree(pkg_dir)
    os.makedirs(libtorch_dir, exist_ok=True)

    # Baixa o arquivo zip
    subprocess.check_call(["wget", libtorch_cpu_url, "-O", libtorch_cpu_zip])

    # Descompacta no libtorch_dir
    subprocess.check_call(["unzip", "-o", libtorch_cpu_zip, "-d", libtorch_dir])

    # Renomeia libtorch -> cpu
    extracted_dir = os.path.join(libtorch_dir, "libtorch")
    if os.path.exists(extracted_dir):
        os.rename(extracted_dir, cpu_dir)
    else:
        print("Erro: diretório extraído não encontrado!")

    # Remove o zip
    os.remove(libtorch_cpu_zip)
    print("Libtorch baixado e extraído com sucesso.")

    # Só para debug, lista o que ficou em d_libs/
    result = subprocess.run(["ls", pkg_dir], capture_output=True, text=True)
    print("Conteúdo de d_libs/:", result.stdout)

download_libtorch()