

#---------------------------------------------------------------------------------------------------
#-NEW
#---------------------------------------------------------------------------------------------------

# setup.py
import os
import sys
import shutil
import zipfile
import requests
import platform
import ctypes
from setuptools import setup, find_packages
from setuptools.command.install import install

# Vamos mover a lógica de libtorch_config pra cá:
def download_and_extract_libtorch():
    LIBTORCH_DIR = "./libtorch"
    if platform.system() == "Windows":
        LIBTORCH_CPU_URL = "https://download.pytorch.org/libtorch/cpu/libtorch-win-shared-with-deps-debug-2.6.0%2Bcpu.zip"
        LIBTORCH_CPU_ZIP = "libtorch-win.zip"
    else:
        LIBTORCH_CPU_URL = "https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-2.5.1%2Bcpu.zip"
        LIBTORCH_CPU_ZIP = "libtorch-linux.zip"

    LIBTORCH_CPU_PATH = os.path.join(LIBTORCH_DIR, "cpu")
    LIBTORCH_LIB_PATH = os.path.join(LIBTORCH_CPU_PATH, "lib")
    LIBTORCH_BIN_PATH = os.path.join(LIBTORCH_CPU_PATH, "bin")

    # Se já existir, não faz download de novo (ou ajuste conforme precisar).
    if os.path.exists(LIBTORCH_CPU_PATH):
        print("A libtorch já foi baixada e extraída.")
        return

    print(f"Baixando libtorch de: {LIBTORCH_CPU_URL}")
    with requests.get(LIBTORCH_CPU_URL, stream=True) as r:
        r.raise_for_status()
        with open(LIBTORCH_CPU_ZIP, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Extraindo
    os.makedirs(LIBTORCH_DIR, exist_ok=True)
    if platform.system() == "Windows":
        with zipfile.ZipFile(LIBTORCH_CPU_ZIP, "r") as zip_ref:
            zip_ref.extractall(LIBTORCH_DIR)
    else:
        os.system(f"unzip {LIBTORCH_CPU_ZIP} -d {LIBTORCH_DIR}")

    # Move pasta libtorch -> libtorch/cpu
    shutil.move(os.path.join(LIBTORCH_DIR, "libtorch"), LIBTORCH_CPU_PATH)

    # Ajusta variáveis de ambiente pra poder usar as libs.
    if platform.system() == "Windows":
        os.environ["PATH"] = LIBTORCH_BIN_PATH + ";" + os.environ.get("PATH", "")
    else:
        os.environ["LD_LIBRARY_PATH"] = LIBTORCH_LIB_PATH + ":" + os.environ.get("LD_LIBRARY_PATH", "")

    # Tenta carregar as libs pra verificar se deu certo
    try:
        if platform.system() == "Windows":
            for dll_file in os.listdir(LIBTORCH_BIN_PATH):
                if dll_file.endswith(".dll"):
                    ctypes.CDLL(os.path.join(LIBTORCH_BIN_PATH, dll_file))
        else:
            for so_file in os.listdir(LIBTORCH_LIB_PATH):
                if so_file.endswith(".so"):
                    ctypes.CDLL(os.path.join(LIBTORCH_LIB_PATH, so_file))
        print("LibTorch carregada com sucesso!")
    except OSError as e:
        print("Erro ao carregar a LibTorch:", e)
        sys.exit(1)


class PostInstallCommand(install):
    """Executa download da libtorch no fim do processo de install."""
    def run(self):
        # 1) Executa instalação normal
        install.run(self)

        # 2) Faz o download/extração da libtorch
        download_and_extract_libtorch()


# Dependendo da plataforma, monte seu package_data:
package_data = {}

if sys.platform.startswith("win"):
    package_data["pureai"] = [
        # Exemplo de DLLs/pyds que você queira incluir
        "win_module.pyd",
        "win_dependency.dll",
        # ...
    ]
elif sys.platform.startswith("linux"):
    package_data["pureai"] = [
        "*.so",
        "*.so.6",
        # ...
    ]

setup(
    name="dependencias_libs",
    version="0.3.11",
    description="All-in-one solution for building RAG pipelines",
    author='Seu Nome',
    author_email='seu.email@exemplo.com',
    packages=find_packages(),
    package_data=package_data,
    include_package_data=True,
    cmdclass={"install": PostInstallCommand},   # <--- Importante!
    license="MIT",
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)

#---------------------------------------------------------------------------------------------------
#-
#---------------------------------------------------------------------------------------------------

# from setuptools import setup, find_packages
# from setuptools.command.install import install
# import os
# import subprocess
# import shutil

# class CustomInstallCommand(install):
#     """Comando customizado para baixar e extrair o libtorch durante a instalação."""
#     def run(self):
#         # Executa a instalação padrão
#         install.run(self)
#         # Executa a rotina de download do libtorch
#         self.download_libtorch()

#     def download_libtorch(self):
#         # Defina os nomes e URLs
#         libtorch_cpu_zip = "libtorch-cxx11-abi-shared-with-deps-2.5.1+cpu.zip"
#         libtorch_cpu_url = (
#             "https://download.pytorch.org/libtorch/cpu/"
#             "libtorch-cxx11-abi-shared-with-deps-2.5.1%2Bcpu.zip"
#         )
#         # Caminho para o diretório do pacote (aqui consideramos que o pacote se chama "libs")
#         pkg_dir = os.path.join(os.path.dirname(__file__), "libs")
#         # Diretório onde os arquivos serão colocados: deve ser "libtorch/cpu" dentro de "libs"
#         libtorch_dir = os.path.join(pkg_dir, "libtorch")
#         cpu_dir = os.path.join(libtorch_dir, "cpu")

#         # Remove o arquivo zip e o diretório de destino se já existirem
#         if os.path.exists(libtorch_cpu_zip):
#             os.remove(libtorch_cpu_zip)
#         if os.path.exists(cpu_dir):
#             shutil.rmtree(cpu_dir)

#         # Cria o diretório de destino (garantindo que libtorch existe)
#         os.makedirs(libtorch_dir, exist_ok=True)

#         # Baixa o arquivo zip
#         print("Baixando libtorch...")
#         subprocess.check_call(["wget", libtorch_cpu_url, "-O", libtorch_cpu_zip])

#         # Descompacta o arquivo dentro de libtorch_dir
#         print("Extraindo libtorch...")
#         subprocess.check_call(["unzip", "-o", libtorch_cpu_zip, "-d", libtorch_dir])

#         # Após extrair, normalmente os arquivos estarão em libtorch_dir/libtorch
#         extracted_dir = os.path.join(libtorch_dir, "libtorch")
#         if os.path.exists(extracted_dir):
#             # Renomeia o diretório extraído para "cpu"
#             os.rename(extracted_dir, cpu_dir)
#         else:
#             print("Erro: diretório extraído não encontrado!")

#         # Remove o arquivo zip baixado
#         os.remove(libtorch_cpu_zip)
#         print("Libtorch baixado e extraído com sucesso.")

# setup(
#     name="dependencias_libs",
#     version="0.1.3",
#     packages=find_packages(),  # Isso encontrará a pasta "libs" (desde que contenha __init__.py)
#     include_package_data=True,
#     cmdclass={"install": CustomInstallCommand},
#     description="Pacote de dependências que baixa e prepara o libtorch",
#     author="Seu Nome",
#     author_email="seu.email@exemplo.com",
# )
