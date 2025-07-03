# Meteor Tracker ☄️

![Versão](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Licença](https://img.shields.io/badge/license-MIT-green)

Um programa de computador desenvolvido em Python para monitorar o céu noturno e capturar automaticamente a passagem de meteoros ou outros objetos luminosos.
![$RNBV7K7](https://github.com/user-attachments/assets/d6d32f40-7668-407b-ab61-0b04eb4836a0)

---

## 📖 Sobre o Projeto

O **Meteor Tracker** utiliza uma webcam conectada ao computador para vigiar o céu. Através do processamento de imagem em tempo real com OpenCV, o programa detecta mudanças bruscas de luminosidade e movimento, características da passagem de um meteoro.

Ao detectar um evento, ele automaticamente grava um clipe de vídeo da passagem completa e o salva em uma pasta pré-definida, criando um registro de todas as atividades celestes noturnas. A interface foi criada com CustomTkinter, seguindo um design minimalista e moderno.

PODE SER BAIXADO AQUI -> https://www.mediafire.com/file/7r40x1zgjog253w/meteor_tracker.exe/file

![image](https://github.com/user-attachments/assets/bda8a474-62c3-4af2-8684-c93daf7fb203)

---

## ✨ Funcionalidades Principais

-   **Detecção Automática:** Monitoramento contínuo do feed de vídeo para detecção de movimento e luminosidade.
-   **Gravação Automática de Clipes:** Salva automaticamente um vídeo do evento detectado, com alguns segundos de contexto antes e depois.
-   **Interface Gráfica Moderna:** Interface limpa e intuitiva com tema escuro.
-   **Feed da Câmera em Tempo Real:** Visualização ao vivo da imagem que está sendo monitorada.
-   **Configuração de Câmera Avançada:** Um menu de configurações que permite a seleção da câmera e do backend de captura (MSMF, DSHOW, VFW) para máxima compatibilidade.
-   **Log de Atividades Persistente:** Registra todos os eventos importantes (início/parada do rastreio, detecções, etc.) em um histórico que pode ser consultado a qualquer momento.

---

## 🛠️ Tecnologias Utilizadas

-   **Python 3**
-   **OpenCV (`opencv-python`)** - Para captura e processamento de vídeo.
-   **CustomTkinter** - Para a criação da interface gráfica moderna.
-   **Pillow** - Para manipulação de imagens e integração com a interface.

---

## 🚀 Como Começar

Siga estes passos para executar o projeto a partir do código-fonte.

### Pré-requisitos

-   Python 3.8 ou superior instalado.
-   Uma webcam conectada ao computador.

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/meteor-tracker.git](https://github.com/seu-usuario/meteor-tracker.git)
    cd meteor-tracker
    ```

2.  **Crie um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # No Windows
    # source venv/bin/activate  # No Linux/Mac
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Se você não tiver um arquivo `requirements.txt`, crie-o com o comando: `pip freeze > requirements.txt`)*

4.  **Adicione os Assets:**
    Certifique-se de que o arquivo `logo.png` (para a splash screen) esteja na pasta raiz do projeto.

### Uso

1.  Execute o programa:
    ```bash
    python meteor_tracker.py
    ```
2.  **Configurações:** Antes de iniciar, clique em "Configurações" para selecionar a câmera correta e a pasta onde os clipes serão salvos.
3.  **Iniciar:** Clique no botão "Iniciar" para começar o monitoramento.
4.  **Log:** Clique em "Log" para visualizar o histórico de todos os eventos da sessão.
5.  **Parar:** Clique em "Parar" para finalizar o monitoramento. Os clipes gravados estarão na pasta que você definiu.

---

## 🚨 Solução de Problemas (Troubleshooting)

-   **A Câmera não Abre:** Este foi o problema mais difícil de depurar. Se você enfrentar isso, siga os passos:
    1.  Vá em **Configurações** e tente selecionar outra câmera ou outro **Backend** (MSMF geralmente é o mais estável no Windows).
    2.  Feche todos os outros programas que possam estar usando a câmera (Zoom, Discord, OBS, etc.).
    3.  Verifique as permissões de câmera em **Configurações > Privacidade e segurança > Câmera** no Windows.
    4.  Execute o programa como **Administrador**.
    5.  Como último recurso, reinstale os drivers da sua webcam através do **Gerenciador de Dispositivos**.

-   **Antivírus Bloqueia o .exe:** É comum que antivírus sinalizem executáveis criados pelo PyInstaller como falsos positivos. Adicione uma exceção no seu antivírus para a pasta ou para o arquivo.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---
_Criado com 💙 por Maycon J. Deláqua
