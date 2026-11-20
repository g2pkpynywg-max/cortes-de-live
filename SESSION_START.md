# SESSION START — GTA 6 CLIPS BR

**O que é:** pipeline que transforma lives de GTA 6 da Twitch em Shorts verticais em PT-BR (1080×1920, 30 fps, legendas com palavras-chave em amarelo, webcam do streamer em destaque, só a voz original, sem música protegida) para o canal **GTA 6 CLIPS BR**. A edição é feita com HyperFrames (`scripts/build_clip.py` + specs em `scripts/specs/`).

**Documento completo:** [`HANDOFF.md`](HANDOFF.md), na raiz. Leia **inteiro** antes de qualquer ação.

**Estado atual (20/11/2026):**
- 3 lives concluídas:
  - Poofesure 2932209040: 3 cortes.
  - Bisteconee 2932201544: 1 corte.
  - Alanzoka 2932200023: 6 cortes; o 03 foi descartado e trocado pelo 07.
- 10 finais aprovados e verificados em `output/` e `output/alanzoka/` (fora do git, só no container antigo).
- Não está confirmado que o usuário baixou os finais.
- Disco: cerca de 7 GB livres. Os brutos em `input/` **não podem ser apagados** sem autorização.
- Branch: `claude/eloquent-goldberg-xxyfad`. HANDOFF.md e SESSION_START.md ainda não foram commitados.

**Próxima tarefa:** analisar a nova live do Alanzoka, **https://www.twitch.tv/videos/2933657204**, e apresentar **10–15 candidatos** (preferência 25–45 s). **Não editar nem renderizar antes da aprovação do usuário.**

**Para começar:**
1. Ler `HANDOFF.md` (seções B, C, F e G).
2. Inspecionar o estado real: `git log --oneline | head`, `git status`, `df -h /home/user`, `ls input work output`.
3. Se o container for novo: `npx skills add heygen-com/hyperframes -g -y` e `pip install yt-dlp faster-whisper demucs`.
4. Se faltar espaço, pedir autorização ao usuário antes de apagar qualquer coisa.
5. `yt-dlp -J https://www.twitch.tv/videos/2933657204`: reportar título, canal, duração e qualidade, e confirmar com o usuário.
6. Análise completa (cópia 360p + `scripts/transcribe_chunked.py` em `pt` + quadros a cada 10 s) → `analysis/candidatos-alanzoka-2933657204.md` → aguardar a escolha.

**Regras do usuário:** não pular etapas; prévia antes de final; render final só com aprovação; não reaproveitar trechos de lives anteriores; sem nudez nem maus-tratos a animais; falas originais sem distorção; não apagar, mover ou sobrescrever arquivos finais ou brutos; não commitar sem autorização.
