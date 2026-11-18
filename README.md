# cortes-de-live

Projeto de cortes automáticos de lives: uma live longa entra, 3 clipes verticais (1080×1920, 30–60 s, legendas em PT-BR) saem, prontos para TikTok, Reels e Shorts. Feito com [HyperFrames](https://hyperframes.heygen.com).

## Estrutura

```
cortes-de-live/
├── input/          ← a live original (MP4). Não vai para o git.
├── work/           ← análise: áudio, transcrição, picos de energia, quadros, moments.json
├── template/       ← projeto HyperFrames base 1080×1920 (legendas, transições, layout)
├── clips/
│   ├── clip-01/    ← um projeto HyperFrames por corte, copiado do template
│   ├── clip-02/
│   └── clip-03/
├── output/         ← MP4 finais: corte-01.mp4, corte-02.mp4, corte-03.mp4
├── scripts/        ← etapas do pipeline (ingest.sh, …)
└── config.json     ← idioma, duração, formato, estilo das legendas
```

## Pipeline

1. **Ingest**: `scripts/ingest.sh input/live.mp4` extrai o áudio, mede a energia segundo a segundo, detecta silêncios e gera um quadro a cada 10 s.
2. **Transcrição**: `hyperframes transcribe` com o modelo multilíngue e `--language pt`, com tempo de cada palavra. Nunca o modelo `.en`, que traduziria para inglês.
3. **Escolha dos 3 momentos**: a transcrição inteira é lida e cruzada com os picos de energia (risadas, gritos, reações). Cada candidato recebe nota por gancho nos primeiros 2 s, ideia completa, emoção e se funciona sem contexto. Os cortes começam e terminam em pausas naturais. O resultado fica em `work/moments.json`, para você revisar antes de renderizar.
4. **Reenquadramento 9:16**: o rosto é detectado ao longo do trecho e o corte 9:16 o acompanha com movimento suave, sem tremer.
5. **Montagem**: cada `clips/clip-0N/` recebe o trecho de vídeo, as legendas (grupos de 3–5 palavras, palavra ativa destacada, palavras-chave em cor) e entradas, punch-ins e transições discretas.
6. **Revisão**: `hyperframes check` e snapshots de cada clipe. Você aprova a prévia e então o render gera `output/corte-0N.mp4` (H.264, AAC, 30 fps).

## Como enviar a live

Esta sessão roda num container na nuvem, então o arquivo precisa chegar até ele. Em ordem de preferência:

1. **Link de download (recomendado)**: suba o MP4 para o Google Drive (ou Dropbox), compartilhe como "Qualquer pessoa com o link" e cole o link aqui. Na primeira vez, aparece um pedido para liberar o domínio de download na rede desta sessão. É só aprovar.
2. **Pasta do seu computador**: abra o app Claude no computador onde está o arquivo, ative o Remote Control (Configurações → Claude Code → Remote Control) e compartilhe a pasta. Eu peço acesso por aqui e você aprova.
3. **Arquivo pequeno (< 100 MB, para teste)**: envie pelo GitHub (Add file → Upload files) para `input/` no branch de trabalho.

Dica: um MP4 em 1080p ou mais, com o rosto visível e o áudio da voz limpo, gera os melhores cortes. Se a live for muito longa (mais de 3 h), diga em que parte estão os melhores momentos e isso acelera a análise.
