# HANDOFF — GTA 6 CLIPS BR (repositório `cortes-de-live`)

> Documento de passagem entre sessões do Claude Code. Escrito em 20/11/2026 a partir da inspeção real
> do repositório, do disco e dos arquivos gerados. O que não pôde ser confirmado em arquivo está marcado
> como **[informado pelo usuário]** ou **[não verificado]**.
>
> Branch de trabalho: `claude/eloquent-goldberg-xxyfad` (último commit verificado: `c7b3f0a`).
> Este arquivo e o `SESSION_START.md` **ainda não foram commitados** (o usuário pediu para não commitar sem autorização).

---

## A. Identidade do projeto

| Item | Valor |
|---|---|
| Canal | **GTA 6 CLIPS BR** [informado pelo usuário] |
| Objetivo | Transformar lives longas de GTA 6 (Twitch) em Shorts verticais em PT-BR para YouTube Shorts, TikTok e Instagram Reels, aproveitando o pico de interesse no lançamento do GTA 6 [informado pelo usuário] |
| Meta de volume | ~2 a 3 Shorts por dia, **priorizando qualidade, retenção e potencial viral**; o usuário não quer cortes sem graça escolhidos só para aumentar a quantidade [informado pelo usuário] |
| Ferramenta de edição | HyperFrames (HTML → vídeo), versão do CLI 0.9.69, com gerador próprio em Python (`scripts/build_clip.py`) |

### Identidade visual (verificada no código de `scripts/build_clip.py` e nos MP4 finais)

- **Quadro:** 1080×1920. Fundo = o próprio vídeo, borrado e escurecido (placa 360×640 com `gblur sigma=14`, mais uma camada preta a 50%).
- **Janela principal:** faixa horizontal no meio da tela.
  - Lives sem webcam (Poofesure): 1080×1215 em y=460, recorte 8:9 do gameplay.
  - Lives com webcam (Bisteconee, Alanzoka): 1080×900 em y=430, montada com **painéis** (veja os layouts abaixo).
- **Layouts de painel** (`scripts/specs/alan_common.py`):
  - `G(x)`: gameplay 8:9 (recorte 1296×1080 com x≤194, para que a webcam original da live nunca apareça duplicada) e a **webcam num inset com borda amarela** no canto superior direito (414×261 em x=650, y=16).
  - `GLOW(x,y)`: só a faixa de baixo do gameplay, usada para esconder nudez de NPC na parte de cima do quadro.
  - `R(gx,gy)`: modo reação, com a **webcam grande em cima** (1080×561) e uma faixa de gameplay embaixo.
  - Posição da webcam na live do Alanzoka (1080p): `CAM = [1490, 274, 416, 262]`. É preciso medir de novo em cada live nova.
- **Cores:** amarelo `#FFD400` para palavras-chave, selos, barra de progresso e moldura da webcam; texto branco com contorno preto.
- **Fontes:** Archivo Black (gancho, título, legendas, selos) e Inter (crédito, etiquetas), ambas no pacote do HyperFrames.
- **Topo:** o **gancho** aparece grande por 0–2,05 s e depois vira **barra de título** fixa, com a linha de crédito embaixo, por exemplo `alanzoka • live de GTA 6 na Twitch`.
- **Barra de progresso** amarela de 8 px logo abaixo da janela principal.
- **Selos** grandes amarelos nos picos ("FOGO!", "8 PESSOAS!", "SEM BALA!", "NERFADO", "COMPRAR?!", "DECOLOU!").
- **Etiquetas de capítulo** amarelas para saltos no tempo ("11 HORAS DEPOIS…", "2H36 DE LIVE").
- **Movimento:** punch-in de 1,14→1 nos primeiros 2 s; punch-ins de ênfase de 1,06–1,10 nas falas fortes; flash branco curto (opacidade 0,38) em cada corte seco. Os efeitos são moderados, como o usuário pediu: "dinâmica, sem exagerar".

### Padrão editorial

- Falas **originais**, sem inventar nem distorcer. Lives em inglês ganham tradução natural para PT-BR; lives em português são legendadas **literalmente**, com os palavrões mantidos (decisão do usuário).
- Cada corte precisa fazer sentido para quem não viu a live.
- Histórias em vários trechos levam etiquetas de tempo para deixar a narrativa clara.
- Gancho nos 2 primeiros segundos; o quadro 0 já mostra rosto, ação ou o texto do gancho.
- **Proibido:** nudez (inclusive de NPC), maus-tratos a animais. Esses trechos são excluídos ou recortados.

### Estratégia de crescimento [informado pelo usuário]

Aproveitar o momento de alta do GTA 6, publicando 2 a 3 Shorts por dia com seleção criteriosa de momentos virais (reações genuínas, situações inesperadas, frases memoráveis).

---

## B. Fluxo de trabalho (o que foi efetivamente feito nas rodadas)

1. **Receber a URL** da live (Twitch VOD).
2. **Verificar acesso, duração e qualidade:** `yt-dlp -J <url>` (título, canal, duração, formatos e host da CDN). Liberar o host da CDN na rede, se preciso. Confirmar com o usuário antes de analisar.
3. **Baixar para análise:**
   - Live curta (<5 h): 1080p60 completa (`yt-dlp -f 1080p60 --downloader native -N 8 --remux-video mp4`).
   - Live muito longa (Alanzoka, 15 h): **cópia 360p** para análise (`-f 360p`). Os trechos aprovados são baixados depois em 1080p60, direto dos segmentos HLS (`scripts/hls_segments.py`).
4. **Transcrição completa com timestamps:**
   - Áudio mono a 16 kHz.
   - Lives ≤5 h: `scripts/transcribe_full.py`. Lives longas: `scripts/transcribe_chunked.py`, que faz blocos de 30 min e retoma de onde parou.
   - Modelo `small` do faster-whisper, com `--language` correto (`pt` para PT, `en` para EN). O modelo `.en` nunca deve ser usado para PT.
   - Saída: `transcript.json` e `transcript.json.partial.txt`.
5. **Revisar amostras visuais:** 1 quadro a cada 10 s (`ffmpeg fps=1/10`) e folhas de contato (sheets). O resultado mapeia onde há GTA, onde há webcam, as pausas e os riscos de nudez.
6. **Encontrar e classificar candidatos:**
   - Ler a transcrição inteira (`scripts/reactions.py` filtra as reações do streamer bloco a bloco).
   - Cruzar com os quadros e confirmar a janela exata com `scripts/win.py` / `scripts/window.py` / `scripts/words.py`.
   - Picos de volume só servem como pista ("não selecionar só porque o áudio é alto", pedido do usuário).
7. **Apresentar candidatos** com nº, início/fim, duração, resumo, melhor frase, nota de viralização 0–10, título/gancho e justificativa, do mais ao menos promissor. Salvar em `analysis/candidatos-<streamer>.md` e **aguardar a escolha**.
8. **Gerar previews** para cada corte aprovado:
   1. Baixar as janelas em 1080p60 e normalizar para 30 fps `.mov` (`setpts=PTS-STARTPTS,fps=30`).
   2. Separar a voz com Demucs `htdemucs`.
   3. Re-transcrever a **voz isolada** com o modelo `medium`, palavra por palavra (`scripts/transcribe_windows.py` ou `scripts/transcribe_clip.py`).
   4. Escrever a spec (`scripts/specs/*.py` → `clips/.../spec.json`) e montar com `python3 scripts/build_clip.py <spec> --media`.
   5. Rodar `hyperframes check --json`, snapshots e `scripts/qa_sync.py`.
   6. Renderizar com `--quality draft` em `output/previews/...`.
9. **Aguardar a aprovação** do usuário.
10. **Renderizar os finais:** `hyperframes render --quality delivery`, um por vez, em segundo plano.
11. **QA completo de cada MP4:**
    - ffprobe: codec, perfil, resolução, fps, nº de quadros, duração.
    - Decodificação inteira (`ffmpeg -v error -f null`), que deve dar 0 erros.
    - Fast start (`moov` antes de `mdat`).
    - Loudness EBU R128 (`ebur128=peak=true`) e `astats`.
    - Folha de quadros do arquivo final.
12. **Organizar e entregar:** os finais vão em `output/<streamer>/corte-NN-<slug>.mp4` e são enviados ao usuário. Avisar que o container é temporário e que `output/` não vai para o git.

Regras do usuário que valem em todo o fluxo: nada de pular etapas; **nada de render final sem aprovação explícita**; nada de reaproveitar arquivos ou trechos de lives anteriores; **nada de apagar os brutos** sem autorização; nada de commit sem autorização (regra desta etapa de handoff).

---

## C. Padrões técnicos de edição (verificados no código e nos MP4)

| Parâmetro | Valor |
|---|---|
| Proporção / resolução | 9:16, **1080×1920** |
| FPS | **30** (as fontes 60 fps são normalizadas para 30 fps antes da montagem) |
| Render final | `node <skills>/hyperframes/scripts/plugin-cli.mjs render --quality delivery --skill=hyperframes -o <out.mp4>` |
| Render de prévia | `--quality draft --quiet` em `output/previews/...` |
| Vídeo final (medido) | H.264 **High**, yuv420p, cerca de 6–14 Mb/s, fast start ativado |
| Áudio final (medido) | **AAC-LC estéreo 48 kHz**, cerca de −14 LUFS integrado (entre −13,7 e −15,2 nos finais), pico verdadeiro ≈ −1,5 dBFS |
| Cadeia de áudio (`build_clip.py`) | trechos cortados do stem com fade de 20–30 ms → `highpass` (60/80 Hz) → `lowpass` (14–15 kHz) → [`afftdn`, só nos clipes de fonte única] → `acompressor threshold=-20dB ratio=3` → `loudnorm I=-14 TP=-1.5 LRA=9` → 48 kHz |
| Música protegida | Separação com **Demucs htdemucs**. Usar **só o stem `vocals`** quando há rádio ou trilha. A música nunca é substituída por outra. |
| Efeitos do jogo | `source(name, sfx=dB)` mistura `drums+other+bass` de −4 a −6 dB **somente** quando a janela não tem base musical. Para decidir, rodar `scripts/stem_levels.py` (baixo ativo ≈0% = sem música). |
| Legendas | PT-BR, Archivo Black em CAIXA ALTA, branco com contorno preto de 10 px; **palavras-chave em `#FFD400`**; a palavra ativa "pula" (escala 1,08, ou 1,15 se for palavra-chave); grupos curtos de uma frase; um grupo por vez |
| Sincronia | Início de cada palavra vindo da transcrição da **voz isolada** (`align_words`, por ordem); override manual com `"wt"` na spec; grupo entra 0,15 s antes (`CAPTION_LEAD`). QA (`qa_sync.py`): toda fala precisa ter legenda e a defasagem média deve ficar entre −0,1 e −0,35 s. |
| Posição das legendas | Bloco de 660 px em x=120, base em y=1240 (clipes 1–3) ou y=1170 (Alanzoka; `captionBottom` na spec). Fica sempre dentro da área segura do TikTok/Reels/Shorts e à esquerda da coluna de botões do TikTok. |
| Áreas seguras (HyperFrames) | Shorts: faixa livre y 288–1248, x 48–888. TikTok: equivale a y 240–1260, x 120–960 em 1080p. Por isso os ganchos do Alanzoka ficam em `top: 290`. |
| Gancho | Até 2 linhas, 64–84 px; cai para a barra de título aos 2,05 s; título de 44–54 px |
| Ritmo | Cortes secos removem silêncio ou enrolação; mudança de plano a cada 2–4 s, sem perder o contexto |
| Duração | Rodadas anteriores: 30–60 s (finais de 31 a 56 s). **Próxima rodada: preferir 25–45 s** [pedido do usuário] |
| Fundo borrado | Embutido no `bg*.mp4` via ffmpeg (`gblur`). **Não usar** o `media-treatment` blur do HyperFrames: em CPU sem GPU custa cerca de 12 s por quadro. |

---

## D. Histórico das rodadas

### D1. Poofesure — VOD 2932209040
- **URL:** https://www.twitch.tv/videos/2932209040 · título "GTA VI" · canal poofesure · 3 h 47 min 41 s · fala **inglês**, sem webcam.
- **Bruto:** `input/live-2932209040.mp4` (8,6 GB, 1080p60).
- **Análise:** `analysis/candidatos.md` (10 candidatos) · transcrição em `work/transcript_full.json`.
- **Aprovados pelo usuário:** candidatos #1, #3 e #5. Os palavrões foram mantidos na tradução PT-BR.

| Corte | Trechos (relógio do VOD) | Final | Duração | Tamanho |
|---|---|---|---|---|
| 01 Roubar um avião | 2:03:05.9–2:04:07.2 (3 trechos) | `output/corte-01-aviao.mp4` | 46,20 s | 58,9 MB |
| 02 Seguro × Boeing | 2:20:04.9–2:21:22.3 (4 trechos) + inserção de 2:05:45 | `output/corte-02-seguro.mp4` | 43,20 s | 58,0 MB |
| 03 Lançamento (contagem) | 0:16:03.5–0:17:04.0 (4 trechos) | `output/corte-03-lancamento.mp4` | 37,80 s | 37,2 MB |

- **Status:** finais renderizados em delivery e verificados nesta sessão (1080×1920, 30 fps, 0 erros de decodificação). Prévias em `output/previews/preview-clip-0{1,2,3}-*.mp4`. Projetos em `clips/clip-01-aviao`, `clips/clip-02-seguro`, `clips/clip-03-lancamento`.
- **Publicação:** [não verificado / não informado pelo usuário].

### D2. Bisteconee — VOD 2932201544
- **URL:** https://www.twitch.tv/videos/2932201544 · título "TAMO VOLTANDO A ATIVA" · canal bisteconee · 4 h 46 min 10 s · **português**, com webcam.
- **Bruto:** `input/live-2932201544.mp4` (13,1 GB, 1080p60).
- **Análise:** `analysis/candidatos-bisteconee.md` (1 escolhido + 3 reservas) · transcrição em `work/b2/transcript.json`.
- **Aprovado:** a contagem regressiva ("esperou o GTA 6 e o PS5 pediu para comprar"). A re-transcrição da voz isolada mostrou que ele **tinha comprado** (estava no perfil errado), e o gancho foi corrigido.

| Corte | Trechos | Final | Duração | Tamanho |
|---|---|---|---|---|
| 04 Contagem / "pediu pra COMPRAR?!" | 0:31:54.3–0:33:38.7 (11 trechos) | `output/corte-04-contagem.mp4` | 51,87 s | 48,8 MB |

- **Status:** final em delivery, verificado. Prévia em `output/previews/preview-clip-04-contagem.mp4`. Projeto em `clips/clip-04-contagem` (spec gerada por `scripts/specs/clip04_contagem.py`).
- **Observação:** este final está em `output/` (raiz) e não em `output/bisteconee/`. Não foi movido, por regra.
- **Publicação:** [não verificado].
- **Tentativa abandonada:** a live do YouTube de LipaoGamer (`lfqmnrTEu_4`) foi bloqueada pela verificação anti-bot do YouTube neste servidor. O usuário desistiu dela.

### D3. Alanzoka — VOD 2932200023 (anterior)
- **URL:** https://www.twitch.tv/videos/2932200023 · título "VICE CITY BABYYYYYYYYYYY" · canal alanzoka · 15 h 25 min 41 s · **português**, webcam no canto superior direito.
- **Bruto de análise:** `input/alanzoka-2932200023-360p.mp4` (4,5 GB, 360p30). Os trechos aprovados foram baixados em 1080p60 para `work/alan/src/` (`c1a…c7b`, com `.mp4`, `.mov`, `.wav` e `.start`).
- **Análise:** `analysis/candidatos-alanzoka.md` (12 candidatos) · transcrição em `work/alan/transcript.json` (11.015 trechos) · notas em `work/alan/notas.md`.
- **Aprovados para produção:** #1–#6. O **#3 (festa errada)** foi **descartado** depois da prévia (nudez de NPC fora do quadro exigiu um recorte baixo) e **substituído pelo #7 (culpa do controle)**, aprovado e finalizado.

| Corte | Trechos (relógio do VOD) | Final | Duração | Tamanho |
|---|---|---|---|---|
| 01 Reformou a casa… tacaram fogo | 3:22:26 · 3:29:04–3:29:31 · 14:52:52 · 14:53:19 · 15:18:17 | `output/alanzoka/corte-01-casa.mp4` | 51,00 s | 67,7 MB |
| 02 Só queria comprar flor pra esposa | 5:08:40–5:11:15 (4 trechos) | `output/alanzoka/corte-02-flor.mp4` | 52,37 s | 89,8 MB |
| 03 Festa errada | 9:53:44–9:54:51 | **descartado** (só a prévia `output/previews/alanzoka/preview-03-festa.mp4`) | 47,0 s | — |
| 04 Viciado no TikTok dentro do GTA | 5:29:35–5:29:54 · 13:11:52–13:16:08 | `output/alanzoka/corte-04-celular.mp4` | 55,70 s | 74,9 MB |
| 05 "Eu não mato ninguém" (coletânea) | 2:36:03 · 4:01:03 · 10:50:38 · 10:50:55 · 12:25:39 · 13:52:58 · 13:53:16 · 13:54:07 | `output/alanzoka/corte-05-naomato.mp4` | 55,80 s | 77,2 MB |
| 06 Arma dos sonhos sem bala | 12:05:57–12:07:10 (5 trechos) | `output/alanzoka/corte-06-arma.mp4` | 31,10 s | 22,3 MB |
| 07 A culpa é SEMPRE do controle | 2:45:09–2:46:06 · 10:19:51–10:20:38 | `output/alanzoka/corte-07-controle.mp4` | 50,80 s | 65,6 MB |

- **Status:** os 6 finais em delivery passaram no QA (H.264 High, yuv420p, AAC 48 kHz, −13,8 a −15,2 LUFS, pico ≤ −1,4 dBFS, 0 erros, fast start) e foram enviados ao usuário. Prévias em `output/previews/alanzoka/`.
- **Download pelo usuário:** ele disse que vai "baixar e conferir todos os arquivos". **[não confirmado]**
- **Publicação:** [não verificado].
- **Candidatos não produzidos** (podem virar material depois): #8 zoou o jogo e pediu desculpa (11:13:50), #9 ladrão que rouba ladrão (9:08:44), #10 yoga (9:34:51), #11 moto sem gasolina (já usada em parte no 07), #12 "não vou olhar" (1:08:47, nudez na tela) e as menções honrosas listadas no arquivo de análise.

---

## E. Estratégia do canal

| Tema | Situação |
|---|---|
| Nome / identidade | GTA 6 CLIPS BR; cortes curtos de streamers jogando GTA 6, legendas PT-BR com amarelo [informado pelo usuário + visual verificado] |
| Monetização | **[não informado pelo usuário nesta sessão]** |
| Postagem | ~2–3 Shorts por dia; qualidade acima de volume [informado pelo usuário] |
| Desempenho (views, retenção, inscritos) | **Nenhum dado de desempenho foi informado nesta sessão.** [não verificado] |
| Aprendizados registrados | Só critérios editoriais, sem métricas: gancho visual no 1º segundo; o corte tem que fazer sentido sozinho; preparação seguida de virada (casa reformada → fogo); identificação do público (celular); recorrência engraçada (coletânea "não mato ninguém") |
| Direitos autorais / conteúdo reutilizado | Música licenciada do jogo (rádio) é removida via Demucs e nunca substituída. Créditos ao streamer em cada vídeo (linha "<canal> • live de GTA 6 na Twitch"). O conteúdo é de terceiros (streamers e Rockstar); não há registro de autorização formal dos streamers **[não verificado]**. Os alertas de sub e de chat da live às vezes aparecem no quadro. |
| Restrições de conteúdo | Sem nudez (há nudez de personagens no GTA 6: Mende, festas, personagem pelado); sem maus-tratos a animais (ex.: chute no cachorro do Bisteconee em 2:47) |

---

## F. Estado atual do ambiente (verificado em 20/11/2026)

### Estrutura de pastas
```
cortes-de-live/
├── HANDOFF.md, SESSION_START.md     ← NÃO commitados
├── README.md                         ← DESATUALIZADO (descreve o plano inicial; o fluxo real está neste HANDOFF)
├── config.json                       ← DESATUALIZADO (valores do plano inicial; o código real não lê este arquivo)
├── analysis/                         ← candidatos de cada live (no git)
├── scripts/                          ← pipeline (no git)
│   ├── build_clip.py                 ← gerador spec → projeto HyperFrames (+ mídia com --media)
│   ├── specs/                        ← geradores de spec por corte; alan_common.py = layouts/helpers
│   ├── ingest.sh, transcribe_full.py, transcribe_chunked.py, transcribe_clip.py, transcribe_windows.py
│   ├── hls_segments.py               ← baixa só os segmentos HLS de cada janela (Twitch)
│   ├── reactions.py, win.py, window.py, words.py, sheet.py, preview_sheet.py, stem_levels.py, qa_sync.py
├── template/                         ← projeto HyperFrames base (pouco usado)
├── clips/                            ← projetos HyperFrames (HTML no git; assets/ fora do git)
│   ├── clip-01-aviao, clip-02-seguro, clip-03-lancamento   (Poofesure)
│   ├── clip-04-contagem                                     (Bisteconee)
│   └── alan/clip-01-casa … clip-07-controle                 (Alanzoka; 03 descartado)
├── input/   (25 GB, fora do git)     ← brutos das 3 lives
├── work/    (10 GB, fora do git)     ← transcrições, stems, janelas 1080p, folhas de quadros
└── output/  (872 MB, fora do git)    ← finais e prévias
```

### Arquivos importantes fora do git (SÓ existem neste container)
- **Finais (11):** `output/corte-01-aviao.mp4`, `output/corte-02-seguro.mp4`, `output/corte-03-lancamento.mp4`, `output/corte-04-contagem.mp4`, `output/alanzoka/corte-0{1,2,4,5,6,7}-*.mp4`.
- **Prévias (11):** `output/previews/*.mp4`, `output/previews/alanzoka/*.mp4`.
- **Brutos:** `input/live-2932209040.mp4` (8,6 GB), `input/live-2932201544.mp4` (13,1 GB), `input/alanzoka-2932200023-360p.mp4` (4,5 GB). **O usuário proibiu apagar** até conferir os downloads.
- **Transcrições:** `work/transcript_full.json` (Poofesure), `work/b2/transcript.json` (Bisteconee), `work/alan/transcript.json` e `work/alan/transcript.json.chunks/` (Alanzoka).
- **Janelas 1080p e stems do Alanzoka:** `work/alan/src/` (cerca de 2,5 GB) e `work/alan/stems/htdemucs/` (16 janelas).
- **Arquivos temporários grandes:** `work/alan/audio.wav` (1,8 GB), `work/audio.wav`, `work/b2/audio.wav`, e folhas e snapshots em `work/**/sheets*`, `snap*`, `frames/`. Podem ser apagados para liberar espaço, **mas só com autorização do usuário**.
- `clips/**/assets/` (2,8 GB no total) guarda as cópias de mídia dos projetos; são regeneráveis com `build_clip.py --media`.

### Espaço em disco
- **7,0 GB livres** de 252 GB (90% usado). **Não cabe uma nova live em 1080p60** (a do Alanzoka teria 53 GB). Mesmo a cópia 360p de uma live longa (cerca de 4–5 GB), somada a transcrição e janelas, deixa pouca margem.
- Antes da próxima rodada, pedir ao usuário autorização para liberar espaço (brutos de `input/`, `work/*/audio.wav`, `clips/**/assets`), **depois** de ele confirmar o download dos finais.

### Dependências (instaladas neste container; numa sessão nova em container novo NÃO estarão lá)
- `ffmpeg 6.1.1`, `node v22.23.5`, `yt-dlp 2026.10.26` (pip), `faster-whisper 1.2.1` (pip), `demucs 4.1.0` (pip), Pillow, numpy.
- Modelos em `~/.cache/huggingface/hub`: `faster-whisper-small`, `faster-whisper-medium`, `HTDemucs`.
- Skills do HyperFrames: instaladas com `npx skills add heygen-com/hyperframes -g -y` em `~/.agents/skills`, com link em `/root/.claude/skills/`. O CLI roda via `node /root/.claude/skills/hyperframes/scripts/plugin-cli.mjs <cmd>` (versão 0.9.69). **Os scripts do repo apontam para esse caminho absoluto**; se ele mudar, ajustar.
- Reinstalar numa sessão nova: `npx skills add heygen-com/hyperframes -g -y` · `pip install yt-dlp faster-whisper demucs` · ao baixar modelos do HF, usar `HF_HUB_DISABLE_XET=1` se der erro.

### Rede (ambiente cloud "cortes-de-live", pessoal)
Hosts liberados [verificado na sessão]: `www.twitch.tv`, `gql.twitch.tv`, `usher.ttvnw.net`, `d1m7jfoe9zdc1j.cloudfront.net`, `huggingface.co`, `cdn-lfs.huggingface.co`, `cdn-lfs.hf.co`, `cas-bridge.xethub.hf.co`, `us.aws.cdn.hf.co`, `cas-server.xethub.hf.co`, `www.youtube.com`. Uma VOD nova pode vir de outra CDN da Twitch; nesse caso, pedir para liberar o host que aparece em `yt-dlp -J`.

### Problemas técnicos conhecidos
1. **Blur WebGL do HyperFrames** (`media-treatment`) é inviável em CPU (cerca de 12 s por quadro). Use o blur embutido via ffmpeg (já é o padrão).
2. **Transcrição de lives longas:** `transcribe_full.py` trava no VAD em lives de mais de 10 h (array de 3,5 GB). Use `transcribe_chunked.py` (blocos de 30 min). Leva cerca de 2,3 h para 15 h de live, com 4 CPUs.
3. **Demucs** leva cerca de 1–3× o tempo real por janela. Rode em segundo plano e não junte com render.
4. **Whisper small** erra nomes e trechos rápidos. Por isso cada corte é re-transcrito com `medium` a partir da voz isolada antes de legendar. `qa_sync.py` usa `small` só como checagem.
5. **YouTube** bloqueia downloads neste servidor (verificação anti-bot). Só Twitch funciona.
6. **Chat da Twitch** (API GQL com Client-ID do site) foi bloqueado pelo classificador de permissões. O chat não é usado.
7. **Segmentos `-muted` da Twitch** (áudio removido por DMCA): `hls_segments.py` lista os que aparecem em cada janela. Evite falas que caiam neles.
8. Render delivery: cerca de 3–6 min por clipe de 50 s. Prévia draft: cerca de 2,5–4 min.
9. `hyperframes check` sempre emite 2 avisos benignos com layouts de painel: `composition_file_too_large` e `duplicate_media_discovery_risk`.
10. **README.md e config.json estão desatualizados**: não refletem o fluxo real. Este HANDOFF é a fonte de verdade.

---

## G. Próxima tarefa

**Nova live do Alanzoka: https://www.twitch.tv/videos/2933657204** [informado pelo usuário; ainda não acessada nem verificada]

A próxima sessão deve:
1. Ler este `HANDOFF.md` inteiro.
2. Inspecionar o estado real: `git log`, `git status`, `ls input work output clips`, `df -h`. Conferir se o container é o mesmo (os arquivos de `output/` existem?) ou se é novo, e nesse caso reinstalar as dependências da seção F.
3. Verificar o armazenamento. Se não houver espaço, **pedir autorização** ao usuário para liberar (ele precisa confirmar antes que já baixou os finais).
4. Confirmar acesso, título, canal, duração, formatos e host da CDN do novo VOD (`yt-dlp -J`) e reportar ao usuário.
5. Analisar a live **inteira**: cópia 360p, `transcribe_chunked.py` em `pt`, quadros a cada 10 s e folhas de contato, mapa de webcam, pausas e riscos (nudez, animais).
6. Encontrar **10–15 candidatos**, sem repetir momentos da live 2932200023.
7. Priorizar cortes de **25–45 s**, sem sacrificar o contexto.
8. Apresentar os candidatos (nº, início/fim, duração, resumo, melhor frase, nota 0–10, título/gancho, justificativa), do mais ao menos promissor, salvar em `analysis/candidatos-alanzoka-2933657204.md` e **aguardar a aprovação**.
9. **Não editar nem renderizar antes da aprovação.**

Na produção (depois da aprovação), seguir as seções B e C, gravar em `output/alanzoka-2933657204/` (sugestão) e manter a numeração e os nomes `corte-NN-<slug>.mp4`.
