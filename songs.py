import yt_dlp
import os
import threading
from concurrent.futures import ThreadPoolExecutor

# =================================================================
# !!! AÇÃO OBRIGATÓRIA ANTES DE EXECUTAR !!!
# =================================================================
# 1. LOCALIZAR O EXECUTÁVEL FFmpeg no seu sistema (ffmpeg ou ffmpeg.exe)
# 2. SUBSTITUIR O VALOR ABAIXO PELO CAMINHO CORRETO DO EXECUTÁVEL!

# ATENÇÃO: O SEU CAMINHO FOI CORRIGIDO PARA INCLUIR O EXECUTÁVEL.
# Se o seu ffmpeg.exe estiver na pasta bin do seu download, use esta forma:

# FFMPEG_CAMINHO = r"C:\Users\seu.usuario\Downloads\ffmpeg-8.0.tar.xz" 


# Se você tiver movido o ffmpeg.exe para a raiz da pasta, ajuste:
# FFMPEG_CAMINHO = r"C:\Users\suporte\Downloads\ffmpeg-8.0\ffmpeg.exe" 

# O 'r' antes das aspas (r"...") resolve o erro 'unicodeescape'!

# =================================================================
# LINKS PARA BAIXAR
# =================================================================
LINKS_PARA_BAIXAR = [
    "https://youtu.be/pB-5XG-DbAA?si=RVUUC_p1lVtS9xGz",
    "https://youtu.be/lSD_L-xic9o?si=GsQoYipLOKeUTuwy",
]

# =================================================================
# OPÇÕES DE DOWNLOAD
# =================================================================
DIRETORIO_SAIDA = 'Musicas_YouTube'
DOWNLOADS_SIMULTANEOS = 5 

# --- Funções Auxiliares para Feedback de Progresso ---

class Logger:
    def debug(self, msg):
        pass
    def warning(self, msg):
        print(f"[{threading.current_thread().name}] [AVISO] {msg}")
    def error(self, msg):
        # Captura e exibe erros de forma clara
        print(f"[{threading.current_thread().name}] [ERRO YT-DLP] {msg}")
def hook(d):
    thread_name = threading.current_thread().name
    
    if d['status'] == 'downloading':
        # Usa os valores numéricos de bytes, ignorando a string colorida
        if 'total_bytes' in d and 'downloaded_bytes' in d:
            
            total = d['total_bytes']
            baixado = d['downloaded_bytes']
            porcentagem = (baixado / total) * 100
            
            # Imprime uma atualização a cada 10%
            if int(porcentagem) % 10 == 0 and int(porcentagem) >= 1:
                 print(f"[{thread_name}] Baixando: {int(porcentagem)}%")
                 
    elif d['status'] == 'finished':
        print(f"\n[{thread_name}] Download concluído. Iniciando a CONVERSÃO para MP3...")
        
    elif d['status'] == 'error':
        print(f"\n[{thread_name}] Erro durante o download.")


# --- Função de Download (Núcleo da Thread) ---

def processar_link(link, diretorio_saida, ffmpeg_path):
    """Função que será executada por cada thread individualmente."""
    if not link:
        return 
        
    thread_name = threading.current_thread().name
    print("\n" + "=" * 60)
    print(f"[{thread_name}] 🟡 INICIANDO DOWNLOAD: {link}")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(diretorio_saida, '%(title)s.%(ext)s'),
        
        # *** GARANTIA DE CONVERSÃO: Passando o caminho do FFmpeg ***
        'ffmpeg_location': ffmpeg_path, 
        
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # Qualidade 192kbps
        }],
        'logger': Logger(),
        'progress_hooks': [hook],
        'verbose': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print(f"\n[{thread_name}] ✅ SUCESSO! Arquivo MP3 criado na pasta de saída.")

    except Exception as e:
        print(f"\n[{thread_name}] ❌ ERRO FATAL! Falha ao baixar/converter {link}. Detalhes: {e}")


def baixar_e_converter_mp3_paralelo(links, diretorio_saida, max_workers, ffmpeg_path):
    
    # Validação do FFmpeg
    if not ffmpeg_path or not os.path.exists(ffmpeg_path):
        print("\n" + "!"*60)
        print("!!! ERRO CRÍTICO: FFmpeg não encontrado no caminho fornecido. !!!")
        print("!!! O download VAI FALHAR na conversão para MP3 (deixará um .webm). !!!")
        print(f"Caminho Verificado: {ffmpeg_path}")
        print("!!! Por favor, ajuste a variável FFMPEG_CAMINHO no topo do script. !!!")
        print("!"*60 + "\n")
        
    # Cria o diretório de saída
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)

    links_validos = [link for link in links if link]
    if not links_validos:
        print("A lista de links está vazia. Nada para baixar.")
        return

    print("\n" + "#" * 60)
    print(f"Iniciando {len(links_validos)} downloads com {max_workers} processos simultâneos.")
    print("#" * 60 + "\n")

    # Inicia o pool de threads
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix='MUSICA') as executor:
        executor.map(
            processar_link, 
            links_validos, 
            [diretorio_saida] * len(links_validos), 
            [ffmpeg_path] * len(links_validos)
        )

    print("\n" + "=" * 60)
    print("Processo de download de TODOS os links finalizado!")
    print(f"Os arquivos estão na pasta: {os.path.abspath(diretorio_saida)}")
    print("=" * 60)


# --- Execução Principal ---

if __name__ == "__main__":
    
    if FFMPEG_CAMINHO == None or FFMPEG_CAMINHO == "":
         print("\n*** Aviso: O caminho do FFMPEG não foi definido. O script pode falhar na conversão para MP3. ***\n")

    baixar_e_converter_mp3_paralelo(
        links=LINKS_PARA_BAIXAR, 
        diretorio_saida=DIRETORIO_SAIDA,
        max_workers=DOWNLOADS_SIMULTANEOS,
        ffmpeg_path=FFMPEG_CAMINHO
    )