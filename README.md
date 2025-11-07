# 🎶 Sistema de Automação de Downloads de Músicas
- Um script Python eficiente que utiliza a biblioteca yt-dlp para baixar o áudio de vídeos do YouTube e convertê-lo automaticamente para o formato MP3, aproveitando a execução paralela (multithreading) para processar vários downloads simultaneamente.

# ⚙️ Pré-requisitos
Para executar este script, você precisará dos seguintes softwares instalados:

- *Python 3*: Recomenda-se a versão mais recente.

- *yt-dlp*: A ferramenta de linha de comando para download de vídeos.

- *FFmpeg*: A biblioteca essencial para a conversão de áudio para MP3.

# 📝 Instalação das Dependências Python
Instale a biblioteca yt-dlp via pip (Baixe no Terminal)
- pip install yt-dlp

# 🚨 Configuração do FFmpeg (Obrigatório)
O FFmpeg é crucial para que a conversão para MP3 funcione. Você deve baixá-lo separadamente e garantir que o caminho do executável (ffmpeg ou ffmpeg.exe) esteja corretamente definido no script.

# 🚀 Como Configurar e Executar
Siga estas etapas para colocar o script em funcionamento:

## 1. Definir o Caminho do FFmpeg

Localize onde o executável do FFmpeg (ffmpeg.exe no Windows ou ffmpeg em Linux/macOS) está no seu sistema e substitua o valor da variável FFMPEG_CAMINHO no topo do script:

## AÇÃO OBRIGATÓRIA ANTES DE EXECUTAR!

**SUBSTITUA PELO CAMINHO CORRETO DO SEU EXECUTÁVEL FFmpeg.**

** FFMPEG_CAMINHO = r"C:\Caminho\Para\O\Seu\ffmpeg.exe"**

**Use 'r' antes da string (r"...") para evitar problemas com caracteres de escape.**

*Nota: Se o caminho estiver incorreto, o script fará o download, mas falhará na conversão para MP3, deixando o arquivo no formato .webm.*

## 2. Adicionar os Links de Download

Insira os URLs dos vídeos do YouTube que deseja baixar na variável LINKS_PARA_BAIXAR: (Coloque sempre dentro dos colchetes)

**LINKS_PARA_BAIXAR = [
    "https:youtu.be/seu-primeiro-link",
    "https:youtu.be/seu-segundo-link",
    # Adicione mais links aqui
]**

## 3. Ajustar as Opções de Download
Você pode personalizar o nome da pasta de saída e o nível de paralelismo:

**DIRETORIO_SAIDA = 'Musicas_YouTube'** (Nome da pasta de destino.)
**DOWNLOADS_SIMULTANEOS = 5**           (Número de arquivos baixados ao mesmo tempo.)

## 4. Executar o Script
Com todas as variáveis configuradas, execute o script a partir do seu terminal:

- **python nome_da_pasta.py**

O console exibirá o progresso de cada thread (download) em tempo real, informando quando o arquivo for concluído e convertido, apenas aguare, que uma pasta ao lado na parte da pasta, apareça com as músicas.

🛠️ Detalhes da Implementação
O script utiliza recursos avançados do Python para um gerenciamento de download robusto:

| Recurso | Descrição |
| -------- | ----- |
| yt-dlp    |Biblioteca principal para a extração do áudio e processamento.    |
| ThreadPoolExecutor      | Gerencia um pool de threads para executar a função processar_link de forma paralela, garantindo o download simultâneo.   |  
| ffmeg_location   | Opção crucial do yt-dlp que recebe o caminho do FFmpeg para realizar a conversão do áudio (post-processamento) para MP3.   | 
| Logger e hock       | Funções auxiliares para monitorar o progresso do download de forma clara no console, atribuindo mensagens a cada thread em execução.    | 
| preferredcodec      | Define o codec final como mp3 e a qualidade em 192kbps.   |


### Idealizador e Criador

[Calebe Ferreira](https://www.linkedin.com/in/c-spellmank)
