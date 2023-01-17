"""
Script Criado para organizar arquivos de video dentro de pastas especificas geradas  de um progrograma de CFTV.
"""

from lib import *


msg("Iniciando Script de organização.", "Aguarde uns instantes que já vou começar a organizar as coisas.", timer=3000)

# Cria os arquivos de log caso não exista.
criaTxt = lambda arq: criarArqLog('C:\\log_backup\\', arq)
[criaTxt(arq) for arq in ['hd_origem.txt', 'hd_backup.txt', 'feitos.txt']]

# Busca no log se existe a unidade salva, se não existir o script pergunta qual unidade é pra ser salva.
diskOrigem = logUnidadeHDs("hd_origem.txt")
diskBackup = logUnidadeHDs("hd_backup.txt")

# Cria uma biblioteca com todos os arquivos de video listados. 
listaOrganizada  = organizarListaImgs(diskOrigem, ['Cameras Internas', 'Cameras Externas'])

# Para todos os arquivos listados anteriomente realiza a cópia para o HD de backup.
for values in listaOrganizada.values():
    copiarArquivos(diskBackup, values)

msg("Acabou!", """A cópia dos arquivos acabaram! Pode ser que todos os arquivos existentas no HD de origem já 
foram copiados não se preocupe. Até amanhã!!!!""", timer=10000)
