#---------------------------------------------------------------------------------------------------
#-NEW
#---------------------------------------------------------------------------------------------------

# from setuptools import setup, find_packages
# from setuptools.command.install import install
# import os
# import platform
# import subprocess
# import shutil

# class CustomInstallCommand(install):
#     """Comando customizado para baixar e extrair o libtorch durante a instalação."""
#     def run(self):
#         # Executa a instalação padrão
#         super().run()

#         # Se for Linux, baixa e extrai a libtorch
#         if platform.system().lower() == "linux":
#             self.download_libtorch()
#             self.add_to_ld_library_path()

#     def download_libtorch(self):
#         libtorch_cpu_zip = "libtorch-cxx11-abi-shared-with-deps-2.5.1+cpu.zip"
#         libtorch_cpu_url = (
#             "https://download.pytorch.org/libtorch/cpu/"
#             "libtorch-cxx11-abi-shared-with-deps-2.5.1%2Bcpu.zip"
#         )

#         # Diretório do pacote "libs"
#         pkg_dir = os.path.join(os.path.dirname(__file__), "libs")

#         # Diretório final: libs/libtorch/cpu
#         libtorch_dir = os.path.join(pkg_dir, "libtorch")
#         cpu_dir = os.path.join(libtorch_dir, "cpu")

#         # Remove o zip antigo (se existir) e a pasta "cpu"
#         if os.path.exists(libtorch_cpu_zip):
#             os.remove(libtorch_cpu_zip)
#         if os.path.exists(cpu_dir):
#             shutil.rmtree(cpu_dir)

#         os.makedirs(libtorch_dir, exist_ok=True)

#         # Baixa o arquivo zip (usando "wget" ou requests, como preferir)
#         print("Baixando libtorch...")
#         subprocess.check_call(["wget", libtorch_cpu_url, "-O", libtorch_cpu_zip])

#         # Extrai
#         print("Extraindo libtorch...")
#         subprocess.check_call(["unzip", "-o", libtorch_cpu_zip, "-d", libtorch_dir])

#         # Normalmente extrai em libs/libtorch/libtorch, então renomeia para "cpu"
#         extracted_dir = os.path.join(libtorch_dir, "libtorch")
#         if os.path.exists(extracted_dir):
#             os.rename(extracted_dir, cpu_dir)
#             print(f"Renomeado {extracted_dir} para {cpu_dir}")
#         else:
#             print("Erro: diretório extraído não encontrado!")

#         # Remove o zip baixado
#         os.remove(libtorch_cpu_zip)
#         print("Libtorch baixado e extraído com sucesso.")

#     def add_to_ld_library_path(self):
#         """Adiciona libs/libtorch/cpu/lib ao LD_LIBRARY_PATH no momento da instalação."""
#         # Atenção: isso NÃO persiste para futuras sessões do usuário.
#         cpu_lib_dir = os.path.join(os.path.dirname(__file__), "libs", "libtorch", "cpu", "lib")
#         old_ld = os.environ.get("LD_LIBRARY_PATH", "")
#         new_ld = f"{cpu_lib_dir}:{old_ld}" if old_ld else cpu_lib_dir
#         os.environ["LD_LIBRARY_PATH"] = new_ld
#         print("LD_LIBRARY_PATH definido para:", os.environ["LD_LIBRARY_PATH"])


# setup(
#     name="dependencias_libs",
#     version="0.3.30",
#     packages=find_packages(),
#     include_package_data=True,
#     cmdclass={"install": CustomInstallCommand},
#     description="Pacote de dependências que baixa e prepara o libtorch (apenas em Linux)",
#     author="Seu Nome",
#     author_email="seu.email@exemplo.com",
# )

#---------------------------------------------------------------------------------------------------
#-
#---------------------------------------------------------------------------------------------------

from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess
import shutil

class CustomInstallCommand(install):
    """Comando customizado para baixar e extrair o libtorch durante a instalação."""
    def run(self):
        # Executa a instalação padrão
        install.run(self)
        # Executa a rotina de download do libtorch
        self.download_libtorch()

    def download_libtorch(self):
        # Defina os nomes e URLs
        libtorch_cpu_zip = "libtorch-cxx11-abi-shared-with-deps-2.5.1+cpu.zip"
        libtorch_cpu_url = (
            "https://download.pytorch.org/libtorch/cpu/"
            "libtorch-cxx11-abi-shared-with-deps-2.5.1%2Bcpu.zip"
        )
        # Caminho para o diretório do pacote (aqui consideramos que o pacote se chama "libs")
        pkg_dir = os.path.join(os.path.dirname(__file__), "libs")
        # Diretório onde os arquivos serão colocados: deve ser "libtorch/cpu" dentro de "libs"
        libtorch_dir = os.path.join(pkg_dir, "libtorch")
        cpu_dir = os.path.join(libtorch_dir, "cpu")

        # Remove o arquivo zip e o diretório de destino se já existirem
        if os.path.exists(libtorch_cpu_zip):
            os.remove(libtorch_cpu_zip)
        if os.path.exists(cpu_dir):
            shutil.rmtree(cpu_dir)

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

setup(
    name="dependencias_libs",
    version="0.4.1",
    packages=find_packages(),  # Isso encontrará a pasta "libs" (desde que contenha __init__.py)
    include_package_data=True,
    cmdclass={"install": CustomInstallCommand},
    description="Pacote de dependências que baixa e prepara o libtorch",
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
)
