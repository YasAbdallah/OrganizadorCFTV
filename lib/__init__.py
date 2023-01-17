import logging
from psutil import disk_usage
import shutil
import os
from tkinter import filedialog, messagebox, Tk
from _tkinter import TclError


def log(root='', arqlog='', mensagem=''):
    formato = 'Data: %(asctime)s :: Linha n: %(lineno)s => %(message)s'
    logging.basicConfig(filename=root+arqlog, level=logging.INFO, format=formato)
    return logging.info(mensagem)


def msg(title, message, timer=1000):
    """

    :param title: Titulo do popup.
    :param message: Mensagem do corpo do popup.
    :param timer: Tempo para fechar o popup
    :return: Retorna uma mensagem para o Usuario.
    """
    eu = " - By: Yasser Ibrahim."
    root = Tk()
    root.withdraw()

    try:
        root.after(timer, root.destroy)
        return messagebox.showinfo(title=title+eu, message=message, master=root)
    except TclError:
        pass


def listarPastas(hd, pastacam):
    """

    :param hd: Unidade de HD de origem. Onde e gravado os arquivos de imagem originais.
    :param pastacam: Pasta a qual deseja encontrar dentro do HD
    :return: Retorna um Dicionario com o caminho Raiz e uma lista dos arquivos de video necessarios.
    """
    # Cria dicionario vazio
    dictarqivospastas = dict()
    # lista todos os diretorios e arquivos
    for root, dirs, files in os.walk(hd):
        # Verifica se existe a pasta desejada e se a lista de arquivos nao esta vazia.
        if pastacam in root and len(files) > 0:
            # Cria o dicionario
            dictarqivospastas[root] = files
    # Retorna o dicionario com o root e a lista de arquivos de video
    return dictarqivospastas


def criarArqLog(pasta, arquivo):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    arq = open(pasta+arquivo, "a")
    arq.close()


def verificarEspacoHD(hdbackup):
    total, usado, livre, percent = disk_usage(hdbackup)

    if percent >= 98:
        log('C:\\log_backup\\', 'info_script.log', 'O HD está cheio, hora de trocar.')
        while True:
            if messagebox.askyesno('Já trocou o HD.', """O HD de backup está cheio, Se você ja trocou o HD Clique em 
            Sim para continuar. Lembre de manter a mesma letra para o HD De backup."""):
                break
    else:
        msg('Porcentagem do HD.', f"O HD de Backup está com: {percent}% da capacidade total.", timer=500)


def unidadeDisk(arqivolog):
    with open(f'C:\\log_backup\\{arqivolog}', 'r') as txt:
        texto = txt.read()
        if texto == "":
            with open('C:\\log_backup\\arqivoLog', 'a') as txt2:
                if messagebox.askyesno("Escolha o HD de Origem.",
                                       "Para Continuar escolha o HD onde é gravado as imagens."):
                    unidade = filedialog.askdirectory()
                    txt2.write(unidade)
        else:
            unidade = texto
    return unidade


def criarPastas(dirs):
    if not os.path.exists(dirs):
        return os.makedirs(dirs)


def organizarData(arquivo):
    return {
        'ano': arquivo[0:4],
        'mes': 'Mes_' + arquivo[4:6],
        'dia': 'Dia_' + arquivo[6:8]
    }


def listarArqCopiados():
    with open('C:\\log_backup\\feitos.txt', 'r') as txt:
        lista = [x.strip() for x in txt.readlines()]
    return lista


def salvarLogArqCopiado(arquivo):
    with open('C:\\log_backup\\feitos.txt', 'a') as txt:
        txt.write(arquivo)
    return msg('Salvo no log', 'Log atualizado.', timer=200)


def organizaListaImgs(diskgravacao, arq):
    listaImgInternas = list()
    listaImgExternas = list()
    for key, value in listarPastas(diskgravacao, arq[0]).items():
        for img in value:
            if os.path.join(key, img) not in listarArqCopiados():
                listaImgInternas.append(os.path.join(key, img))
    for key, value in listarPastas(diskgravacao, arq[1]).items():
        for img in value:
            if os.path.join(key, img) not in listarArqCopiados():
                listaImgInternas.append(os.path.join(key, img))
    return {"Internas": listaImgInternas, "Externas":listaImgExternas}


def copiarArquivos(diskBackup, arquivos):
    for arquivo in arquivos:
        # Usar separarPastas[-3] = Cameras Internas/Externas e separarPastas[-2] = numero da camera, separarPastas[-1] = arquivos de video
        separarPastas = arquivo.split("\\")
        # Organizando os arquivos de video por data
        date = organizarData(separarPastas[-1])
        # Juntando os tudo para formar o caminnho para criar as pastas e copiar os arquivos de videos
        caminBackup = os.path.join(diskBackup, separarPastas[-3], date['ano'], date['mes'], date['dia'],
                                   'Cam_' + separarPastas[-2])
        criarPastas(caminBackup)
        # Verificando se o arquivo não existe na lista de arquivos copiados anteriormente
        if arquivo not in listarArqCopiados():
            verificarEspacoHD(diskBackup)
            try:
                # Copiando o arquivo com os metadados
                shutil.copy2(arquivo, os.path.join(caminBackup, separarPastas[-1]))
            except FileNotFoundError:
                msg("Arquivo não encontrado.",
                    f"O arquivo: {arquivo} não foi encontrado. Indo para o próximo.",
                    timer=1000)
                continue
            except PermissionError:
                msg("Sem permissão.",
                    f"Não tenho permissão para copiar este arquivo. Indo para o próximo.",
                    timer=1000)
                continue
            else:
                msg("Arquivo copiado.", "Indo para a próxima...", timer=500)
                salvarLogArqCopiado(arquivo + "\n")
