from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess
import shutil


def download_libtorch():
    # Defina os nomes e URLs
    libtorch_cpu_zip = "libtorch-cxx11-abi-shared-with-deps-2.5.1+cpu.zip"
    libtorch_cpu_url = (
        "https://download.pytorch.org/libtorch/cpu/"
        "libtorch-cxx11-abi-shared-with-deps-2.5.1%2Bcpu.zip"
    )
    # Caminho para o diretório do pacote (aqui consideramos que o pacote se chama "libs")
    pkg_dir = os.path.join(os.path.dirname(__file__), "d_libs")
    print("\n\n\n\n\n\n\n\n\n\n\nPacote dir:\n\n\n\n\n\n\n\n", pkg_dir)
    # Diretório onde os arquivos serão colocados: deve ser "libtorch/cpu" dentro de "libs"
    libtorch_dir = os.path.join(pkg_dir, "libtorch")
    cpu_dir = os.path.join(libtorch_dir, "cpu")

    if os.path.exists(pkg_dir):
        shutil.rmtree(pkg_dir) 

    # Cria o diretório de destino (garantindo que libtorch existe)
    os.makedirs(libtorch_dir, exist_ok=True)

    # Baixa o arquivo zip
    print("Baixando libtorch...")
    subprocess.check_call(["wget", libtorch_cpu_url, "-O", libtorch_cpu_zip])

    # Descompacta o arquivo dentro de libtorch_dir
    print("Extraindo libtorch...")
    subprocess.check_call(["unzip", "-o", libtorch_cpu_zip, "-d", libtorch_dir])

    # Após extrair, normalmente os arquivos estarão em libtorch_dir/libtorch
    extracted_dir = os.path.join(libtorch_dir, "libtorch")
    if os.path.exists(extracted_dir):
        # Renomeia o diretório extraído para "cpu"
        os.rename(extracted_dir, cpu_dir)
    else:
        print("Erro: diretório extraído não encontrado!")

    # Remove o arquivo zip baixado
    os.remove(libtorch_cpu_zip)
    print("Libtorch baixado e extraído com sucesso.")

    result = subprocess.run(["ls", pkg_dir], capture_output=True, text=True)
    print(result.stdout)

download_libtorch()

