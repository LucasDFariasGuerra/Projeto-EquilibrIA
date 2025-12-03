<img width="217" height="216" alt="image" src="https://github.com/user-attachments/assets/e2b617a9-3116-4d76-b55d-aace90563ef2" />

## Sobre o App
O Equilibr.IA tem capacidade de balancear o bem-estar físico com o mental, alinhadamente as limitações de cada indivíduo. 
Calculando as taxas iniciais de uma pessoa e baseada nas suas vontades propor fichas de treino e dietas.

Inicialmente o projeto será realizado no terminal utilizando Python.

Decidimos criar esse aplicativo tendo em vista que atualmente na sociedade brasileira 52% dos brasileiros raramente ou nunca praticam atividades físicas. Entre os que fazem atividades físicas, 22% se exercitam diariamente, 13% pelo menos três vezes por semana e 8% pelo menos duas vezes semanais.
## First Release (V1)
Este projeto foi desenvolvido com o objetivo de auxiliar no acompanhamento de saúde, nutrição e treino de forma prática e acessível. A primeira release do aplicativo apresenta quatro funcionalidades principais.

● A primeira consiste em um cadastro simplificado, permitindo o registro de dados básicos como idade, peso, altura, sexo e objetivo corporal, com possibilidade de criação, consulta, atualização e exclusão das informações.

● A segunda funcionalidade é responsável pelos cálculos essenciais, incluindo a geração automática do Índice de Massa Corporal (IMC) e da Taxa Metabólica Basal (TMB), utilizando a fórmula de Harris-Benedict.

● Na terceira funcionalidade, o aplicativo oferece sugestões de alimentação balanceada, com base em macronutrientes, para auxiliar o usuário a alcançar uma nutrição ideal de acordo com suas necessidades.

● Por fim, a quarta funcionalidade trata do plano de treino simples, que gera rotinas de exercícios adaptadas ao nível físico do usuário, podendo ser iniciante, intermediário ou avançado.

Esta é apenas a primeira versão do aplicativo. Futuras atualizações incluirão novas funcionalidades e melhorias para oferecer uma experiência mais completa e eficiente.

## Second Release (V2).
Nesta segunda release, o código sofreu uma refatoração robusta para integrar inteligência generativa e funcionalidades de segurança avançada. O foco saiu de algoritmos estáticos para consultas dinâmicas e personalizadas.

1. Personal Trainer e Nutricionista com IA (suggestions.py)
A maior inovação desta versão. O sistema foi integrado à API do Google Gemini (IA Generativa).

 ● Dietas Dinâmicas: Ao invés de frases prontas, o módulo suggestions.py envia os dados do usuário (TMB, Peso, Objetivo) para a IA, que retorna um cardápio único e calculado especificamente para aquele momento.

 ● Treinos Personalizados: A IA analisa a idade e o nível de treino (iniciante/avançado) para escrever uma rotina de exercícios detalhada.

2. Persistência de Dados (database.py):
 ● Sistema de salvamento local em JSON para manter os dados dos usuários seguros entre as execuções.


4. Recuperação de Conta via E-mail (user_manager.py)
A segurança foi aprimorada com a implementação de protocolos SMTP.

 ● Esqueci Minha Senha: Agora é possível solicitar a recuperação de senha. O sistema envia automaticamente um e-mail com um código de verificação para o endereço cadastrado, permitindo a redefinição segura da senha.

 ● Backup Codes: Geração de códigos de emergência no momento do cadastro.

4. Dashboard de Evolução e Hidratação (interface.py)
A interface foi expandida para permitir o acompanhamento diário:

 ● Monitoramento de Água: O usuário pode registrar o consumo de água ao longo do dia e o sistema compara com a meta diária (calculada baseada no peso: 35ml/kg).

 ● Histórico de Peso: O sistema agora armazena um histórico de pesagens, exibindo uma tabela de evolução que mostra a variação de peso ao longo do tempo, alertando caso o usuário fique muito tempo sem se pesar.

O projeto é modularizado para facilitar a manutenção e escalabilidade:

 ● main.py: O ponto de entrada. Gerencia o loop principal da aplicação e a navegação entre menus.

 ● suggestions.py: Módulo responsável pela conexão com a API google-generativeai. Contém os prompts de engenharia para gerar dietas e treinos.

 ● user_manager.py: Controla a lógica de negócios do usuário (login, cadastro, envio de e-mail e validação de senhas).

 ● health_calculator.py: Contém a matemática pura (fórmulas de TMB, IMC).

 ● database.py: Módulo que manipula o arquivo usuarios.json.

 ● interface.py: Cuida de toda a parte visual (prints, tabelas e menus coloridos).

 ● utils.py: Utilitários gerais como limpeza de tela, pausas e cores (Colorama).

 📚 Bibliotecas Externas Utilizadas
google-generativeai: Para inteligência artificial.

python-dotenv: Para gerenciamento de variáveis de ambiente (Chaves de API).

colorama: Para estilização do terminal.

smtplib (Nativa): Para envio de e-mails.

⚙️ Configuração (Environment)

Para que as funcionalidades de Dieta/Treino com IA e Recuperação de Senha funcionem, você precisa configurar o ambiente corretamente. Siga os passos abaixo.

1. Instalação das Bibliotecas
O projeto depende de bibliotecas externas para conectar com o Google Gemini, gerenciar variáveis de ambiente e colorir o terminal.

Abra o seu terminal na pasta do projeto.

Execute o seguinte comando para instalar tudo de uma vez:

pip install google-generativeai python-dotenv colorama

Nota: As bibliotecas smtplib, json, os, math, random e datetime já vêm instaladas por padrão no Python.

2. Gerando a API Key do Google (Gemini)
Para que o "Personal Trainer" e o "Nutricionista" funcionem, você precisa de uma chave gratuita do Google.

Acesse o Google AI Studio: https://aistudio.google.com/

Faça login com sua conta Google.

No menu esquerdo, clique em "Get API key" (Obter chave de API).

Clique no botão "Create API key".

Selecione um projeto existente ou crie um novo.

Copie o código gerado (começa geralmente com AIza...).

3. Gerando a Senha de App (Para envio de E-mail)
Para a recuperação de senha funcionar, o sistema usa o Gmail. Por segurança, o Google não aceita sua senha normal. Você precisa criar uma "Senha de App".

⚠️ Importante: Para isso funcionar, a "Verificação em duas etapas" da sua conta Google precisa estar ATIVADA.

Acesse as configurações da sua Conta Google: https://myaccount.google.com/

No menu esquerdo, clique em Segurança.

Na barra de busca no topo, digite "Senhas de app" (ou "App passwords") e clique na opção.

Dê um nome para o app (ex: EquilibrIA) e clique em Criar.

O Google vai gerar uma senha de 16 letras (ex: xyza bcde fghi jklm).

Copie essa senha. (Você usará ela sem os espaços).

4. Configurando o Arquivo .env
O sistema busca essas chaves em um arquivo oculto para não expor suas senhas na internet.

Na pasta raiz do projeto (a mesma onde está o main.py), crie um arquivo novo chamado .env (apenas .env, sem nome antes do ponto).

Abra esse arquivo com o Bloco de Notas ou VS Code.

Cole o conteúdo abaixo, substituindo pelos seus dados gerados nos passos anteriores:

Snippet de código

# Chave da Inteligência Artificial (Passo 2)
API_KEY="COLE_SUA_CHAVE_AIZA_AQUI"

# Configurações de E-mail (Passo 3)
EMAIL_REMETENTE="seu_email@gmail.com"
EMAIL_SENHA="cole sua senha de app aqui sem espaços"
Exemplo real de como deve ficar: EMAIL_SENHA="xyzabcdefghijklm" (tudo junto).








 
