---
name: bambu-h2c-slice-print
description: Use when operating Bambu Studio for the Bambu Lab H2C — importing/fixing/arranging models, cut/split/boolean/text/paint tools, process and filament settings for quality, supports, dual-nozzle/Vortek grouping, calibration, AMS mapping, plates, first print, CLI slicing and MCP control.
---

# Bambu Studio + H2C — do modelo ao print com qualidade

Fluxo obrigatório: **modelo aprovado (skill blender-print-ready) → importar e preparar no Studio → perfil impressora/filamento/processo corretos → ajustes de qualidade → suportes/pintura → fatiar e revisar preview → checklist → enviar → acompanhar 1ª camada**. Nunca envie sem revisar o preview. Nunca cancele um print sem confirmação do usuário.

## 1. A máquina (H2C) — o que muda em relação a uma impressora comum
- Toolhead dual: **bico esquerdo fixo** + **bico direito trocado automaticamente** entre 6 hotends no rack **Vortek** (aquecimento por indução, ~8 s). 7 hotends no total → até **7 materiais sem purga**; até 24 com AMS e purga mínima. Impressão sequencial (um bico por vez).
- Volume ≈ 325×320×320 mm (só bico esquerdo) / ≈ 300×320×325 mm em modo dual-Vortek (a área direita encolhe por causa do rack). Hotend 350 °C, mesa 120 °C, câmara aquecida 65 °C. Placas 350×320 mm.
- Hotends: 0,4 aço endurecido padrão; 0,2/0,6/0,8 e high-flow como hotends Vortek extras. O Studio precisa da **configuração real do rack** (qual diâmetro/tipo em cada posição) — a impressora confere o hotend ID e recusa perfil errado (HMS 0500-8053).
- Regras fixas de atribuição: **TPU só no bico direito** (alimentação externa; nunca AMS para ≤ 95A); PPA-CF/PPS-CF só no esquerdo; peças > 320 mm de altura → bico direito.
- Slicer: **Bambu Studio ≥ 2.4** tem perfis nativos H2C. OrcaSlicer: suporte H2C nas nightlies desde jul/2026, mas estimativa de tempo multi-bico errada e remapeamento filamento→Vortek instável → prefira Bambu Studio.

## 2. Importar e preparar o modelo no Studio
- Formatos: `.3mf .stl .step/.stp .obj .amf`. STEP é tesselado (linear/angle deflection: menor = mais suave, mais triângulos). OBJ abre diálogo de cores (OK). STL com várias cascas entra como **um objeto**.
- Vários arquivos de uma vez → pergunta "Load these files as a single object with multiple parts?": **Yes** para multi-cor/multi-material (partes mantêm posição), **No** para peças independentes.
- **Fix model** (clique direito → Fix Model, ou o ícone de aviso na lista): repara non-manifold/bordas abertas em certo grau; no Windows usa Netfabb. Se o aviso aparecer, o certo é voltar ao Blender e corrigir — Fix model é remendo, pode fechar buracos errado.
- **Simplify model** (clique direito): decimate com preview; use quando > ~1 M triângulos.
- **Lay on Face** (F): escolhe a face de apoio. **Auto Orient**: minimiza overhang/área suportada — confira, pontes enganam o algoritmo. **Arrange** (A / Shift+A): espaçamento, auto-rotate, uma cor por plate opcional.
- **Cut** (C): planar ou dovetail (encaixe rabo-de-andorinha com tolerância), conectores Plug/Dowel/Snap para peças maiores que o volume ou para eliminar suportes.
- **Split to Objects** (cada casca vira objeto, cai na mesa) vs **Split to Parts** (cascas continuam agrupadas, mantêm posição — use para atribuir cor por parte). Partes podem flutuar em Z; objetos precisam tocar a mesa.
- **Mesh Boolean** (Union/Intersection/Subtraction, dois objetos por vez): resolve objetos sobrepostos que geram "redundant paths". **Negative Part**: subtração só no fatiamento (não exporta STL). **Modifier**: região com parâmetros próprios (infill, velocidade, walls) — precedência Global < Object < Part < Modifier.
- **Text**: fonte, tamanho mm, Thickness (relevo) / Embedded Depth (gravado), modo Surround para superfícies curvas; operação Part ou Cut. Mais confiável que texto booleano no Blender.
- **Measure**: ponto/linha/superfície/círculo; use para conferir dimensões críticas importadas (bate com o Blender?).
- **Variable layer height**: Adaptive (slider detalhe↔velocidade) em topos curvos; faixa do 0,4 é 0,08–0,28 mm.
- **Pintura**: Support painting (enforcer verde/blocker; Fill para faces inteiras), Seam painting (habilitar na aba Seam), Color painting (1–9 escolhe filamento, Shift+LMB apaga, Fill com detecção de arestas, Height range para faixas).

## 3. Perfis: impressora, filamento, processo
- **Impressora**: H2C com o nozzle/rack correto. Trocou hotend físico → atualize o perfil antes de fatiar.
- **Filamento**: preferir presets Bambu para filamento Bambu; para terceiros, *Generic X* como base e criar preset próprio (Filament → Settings → Custom Filaments → Create New; nome "Marca Tipo @H2C"). Presets genéricos costumam ter *max volumetric speed* errado → calibrar (§6).
- **Processo** (0,4 mm): `0.20mm Standard` como base; `0.16 Optimal`/`0.12 Fine` para detalhe; `0.28 Draft` para protótipo. Layer entre 20–70 % do bico; 1ª camada 50 % (0,2). Salvar como preset próprio por tipo de peça ("Funcional 4 walls", "Figura 0.12").

## 4. Ajustes de qualidade (aba Process) — o que mexer e quando
**Quality**
- Layer height: 0,20 padrão; 0,12–0,16 fino; 0,28 rápido. **Precise Z height** ON para altura exata (ajusta as últimas 5 camadas).
- Line width: deixe padrão; se mudar, 0,75–1,5× bico. 1ª camada mais larga é proposital.
- **Seam**: Aligned (liso, seam numa linha), Back (fica atrás), Nearest (cantos vivos, esconde melhor), Random (dispersa). Seam gap 15 % do bico. **Scarf seam** (Contour) em cascas curvas/figuras para sumir a linha; pintar seam quando cair em face visível.
- **Wall order**: inner/outer (padrão, melhor para overhang); outer/inner para precisão dimensional/superfície; inner-outer-inner para os dois.
- **Precise wall** ON em peças dimensionais (encaixes). "Only one wall on top surfaces" ON (padrão). "Detect overhang walls" ON.
- **Wall generator**: Arachne (padrão; paredes finas variáveis, mantém texto fino) vs Classic (uma seam por camada, descarta features < 1 linha). Trocar para Classic se superfícies ficarem irregulares ou aparecerem segmentos flutuantes.
- **Ironing**: só topos planos (Top surfaces, Rectilinear); risco de creep térmico e descolamento — não usar por padrão.
- **Elephant foot compensation**: calibrar com cubo 25×25×10, brim off, compensação 0 → valor = média do desvio X/Y (típico 0,10–0,20 mm). Específico por placa.
- Bridges: ↑ bridge flow (linhas fundem), ↓ bridge speed; *Thick bridges* só em vãos longos.
- Slow down for overhangs ON (padrão). Smooth speed discontinuity ON.

**Strength**
- **Walls**: 2 decorativo, **3–4 funcional**. Top/bottom shells ≥ 4–5 (topo liso sobre infill esparso). Resistência = paredes, não infill.
- Infill: 15 % Gyroid/Cubic (isotrópico) geral; 30–40 % carga; Grid raspa o bico em alta velocidade; 100 % só Rectilinear/Aligned/Concentric etc. Infill/wall overlap 15 %.

**Speed**: presets são bons; reduza outer wall (≈ 100–150 mm/s) e overhang para acabamento; peças altas e finas → mais lentas (vibração).

**Support**
- Tipos: Normal(auto) / Tree(auto) / manual. Estilos: Tree **Organic** (padrão) ou **Hybrid** (padrão com filamento de suporte ou adaptive layer); Normal Grid/Snug para overhangs planos grandes. Threshold 30° padrão (subir para 40–45° em PLA para menos suporte).
- **Top Z distance**: 0,2 mm com o mesmo filamento; **0 mm com filamento de suporte dedicado** (Support for PLA/PETG, PVA) usado **só na interface** ("support interface filament") — menos trocas, superfície perfeita. Interface ~3 camadas.
- Pintar enforcers/blockers em vez de deixar tudo automático. Remover suportes em até 2 h (ficam mais duros depois).
- Filamento de suporte deve suportar a temperatura do modelo (Support for PLA ≠ PETG) senão entope.

**Others**
- Brim: Auto (padrão — largo para PC/ABS/CF, estreito para TPU); Painted (orelhas) para cantos que levantam; No-brim em peças com base larga. Skirt para purgar.
- **Prime tower** ON (necessário para "flush into support/infill/object"); Prime volume ≠ Flushing volume. Flush escuro→claro precisa de muito mais volume que claro→escuro.

## 5. Dual nozzle e Vortek no Studio
- **Filament grouping** (automático ao fatiar; "Rearrange filament → Customize" para manual). Modos: *Filament-saving* (mínima purga), *Convenient* (usa posições atuais do AMS), *Custom*. Ordem de decisão: compatibilidade de material → limites de slot AMS → menor flush → cor.
- Regra de ouro: **suporte/interface no outro bico** — trocar de bico não purga; toda purga vem de trocas *dentro* do mesmo bico. Mesmo raciocínio para duas cores: uma por bico = zero purga.
- PLA↔PETG como suporte mútuo: validado só com Bambu PLA Basic + PETG HF; PLA como interface sob PETG é o recomendado; ambos secos; porta aberta.
- Purge mode H2C (prime tower vs chute) selecionável; com ≤ 7 materiais em hotends distintos, praticamente zero desperdício.
- Confira no preview a aba de filamentos: cada um mostra o bico atribuído. TPU no direito, CF no esquerdo. Altura > 320 mm força direito.

## 6. Filamentos, placas e calibração
- Temperaturas (presets Bambu, ajustar após calibração): PLA ~220 °C / mesa 35–55 °C, **porta e tampa abertas** (câmara quente amolece PLA → entupimento); PETG HF ~245 / 70 °C; ABS/ASA 250–270 / 90–100 °C, fechado + câmara ligada; PC/PA: câmara, cola; TPU só 0,4, direito, externo, um objeto por plate.
- **Placas**: PEI texturizada — sem cola para PLA/PETG/ABS; lavar com detergente + água morna (IPA só espalha gordura). PEI lisa — PLA sem cola; **PETG e outros exigem cola** senão arranca a PEI. Cool Plate SuperTack — PLA. Engineering — materiais técnicos. Cola bastão para ASA-CF/PA/PPA/PPS/PET-CF. Remover peça só com mesa ≤ 35 °C. Selecione a placa certa no slicer: a H2 lê o marcador da placa.
- **Secagem**: PLA 55 °C 8 h (AMS 2 Pro 45 °C 12 h); PETG 70 °C 8 h; PETG HF obrigatório 65 °C 8 h; ABS/ASA 75–85 °C; TPU 65–75 °C; PVA obrigatório. Só TPU duro (≥ 55D) via AMS. Sintomas de umidade: stringing, estalos, superfície áspera, camadas fracas.
- **Flow Dynamics (PA)**: rodar para filamento novo, bico trocado/gasto, ou após mudar temperatura/max flow. Auto na H2 (Calibration → Flow Dynamics → Auto). Não confiável com filamento úmido, transparente ou TPU.
- **Flow Rate**: só depois do PA e só se persistirem blobs/zits (flow alto) ou gaps (flow baixo). Coarse ±20 % em passos de 5, depois Fine −9…0 % em passos de 1; salvar em preset novo.
- Developer Mode (Preferences) libera: Temperature tower, PA Tower/Line/Pattern, Retraction test (torre limpa → 0,2–0,4 mm; stringing no topo = filamento úmido), **Max Flowrate** (valor = início + altura×passo, reduzir 5–10 %), VFA.
- Contração: medir peça de teste e ajustar *shrinkage* no perfil do filamento (`% = medido/projetado×100`).

## 7. Checklist pré-print (obrigatório, reportar item a item)
1. Modelo passou no blender-print-ready (manifold, mm, paredes ≥ 0,9 mm); Studio não pediu Fix model.
2. Perfil H2C com rack Vortek real; hotend por posição confere.
3. Filamentos: preset correto, seco, slot AMS/bico batem com o slice; TPU externo no direito.
4. Placa correta no slicer e limpa; cola se PEI lisa + PETG/ABS.
5. Preview: suportes onde precisa (e só lá), overhangs justificados, seam em face escondida, brim em peça alta/estreita, prime tower dentro do volume, tempo e gramas plausíveis.
6. Porta: aberta para PLA/PETG; fechada + câmara para ABS/ASA/PC/PA.
7. Print options no envio: Bed leveling ON, Flow Dynamics Auto, Nozzle offset Auto (padrões da H2), AI detection ON, timelapse só se houver pendrive.
8. Mapeamento AMS (diálogo de envio): tipo → cor; spool externo nunca mapeia sozinho — mapear manualmente.
9. Enviar e **acompanhar a 1ª camada** pela câmera; só considerar "ok" após ~5 camadas.

## 8. Enviar e controlar por agente
- **MCP** (comunitário, não oficial — auditar antes de instalar): https://github.com/DMontgomery40/bambu-printer-mcp — `npx @rowbotik/bambu-printer-mcp`; env `PRINTER_HOST`, `BAMBU_SERIAL`, `BAMBU_TOKEN` (LAN access code; Developer Mode ligado na impressora), `BAMBU_MODEL=h2c` (nunca fallback h2d; exige Studio ≥ 2.4), `SLICER_PATH` para fatiar. Tools: `get_printer_status`, `print_3mf`, `pause_print`/`resume_print`/`cancel_print`, `camera_snapshot` (RTSP na H2), `get_printer_filaments`, `resolve_3mf_ams_slots`, `slice_stl`/`slice_with_template`, `scale_stl`/`rotate_stl`/`lay_flat`, `set_ams_drying`, `upload_file`/`list_printer_files`.
- Alternativas: https://github.com/tobiasbischoff/bambu-cli (Go, AGENTS.md), https://github.com/griches/bambu-mcp, https://github.com/greghesp/ha-bambulab (pybambu, referência MQTT), protocolo: https://github.com/Doridian/OpenBambuAPI.
- Studio por Wi-Fi/LAN: Slice plate → Print plate → diálogo com impressora, calibrações e mapeamento AMS. LAN mode = IP + access code; sem pendrive não há timelapse nem envio para storage.
- **CLI headless** (Bambu Studio e Orca compartilham):
```bash
bambu-studio --load-settings "machine.json;process.json" --load-filaments "f1.json;f2.json" \
  --arrange 1 --orient 1 --slice 0 --allow-newer-file --export-3mf out.gcode.3mf --outputdir ./out --debug 2 model.stl
```
  Gotchas: presets de sistema não são referenciáveis por nome — exportar JSON (ou copiar de `resources/profiles/BBL/`) e resolver `inherits`; `printer_model` do 3MF = machine JSON; JSON de Orca ≠ Bambu Studio; números como string (`"raft_layers": "2"`); settings por extrusora são vetores (`--retraction-length=a,b`); um `--load-filaments` por slot; `--export-slicedata` para inspecionar. Docs: https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage · https://www.orcaslicer.com/wiki/cli/cli_mode
- Rotina do agente: `get_printer_status` (IDLE, placa detectada, AMS carregado) → `print_3mf` → `camera_snapshot` após a 1ª camada e a cada poucos minutos → se HMS/erro: skill bambu-print-troubleshoot. Pausar sozinho é permitido; cancelar só com confirmação.

## 9. Publicar no MakerWorld (se for o caso)
Foto real do resultado; título descritivo ("4 cores, 0.16 mm, suportes fáceis"); perfil deve agregar valor (orientação, seam, suporte, parâmetros); variantes em plates nomeados; proibido: perfis sem suporte necessário, tempo enganoso, edições triviais, palavras "fast/best/official".

## Referências (wiki Bambu Lab)
- Quick start: https://wiki.bambulab.com/en/software/bambu-studio/studio-quick-start · Fix model: https://wiki.bambulab.com/en/software/bambu-studio/fix-model · Simplify: https://wiki.bambulab.com/en/software/bambu-studio/simplify-model · Auto orient: https://wiki.bambulab.com/en/software/bambu-studio/auto-orientation · Arrange: https://wiki.bambulab.com/en/software/bambu-studio/auto-arranging · Cut: https://wiki.bambulab.com/en/software/bambu-studio/cut-tool · Split: https://wiki.bambulab.com/en/software/bambu-studio/split-to-objects-parts · Boolean: https://wiki.bambulab.com/en/software/bambu-studio/mesh-boolean · Negative part: https://wiki.bambulab.com/en/software/bambu-studio/subtract-a-part · Modifier: https://wiki.bambulab.com/en/software/bambu-studio/modifier · Text: https://wiki.bambulab.com/en/software/bambu-studio/3d-text · Measure: https://wiki.bambulab.com/en/software/bambu-studio/measurement_tool · Support painting: https://wiki.bambulab.com/en/software/bambu-studio/support-painting · Color painting: https://wiki.bambulab.com/en/software/bambu-studio/color-painting-tool · Adaptive layer: https://wiki.bambulab.com/en/software/bambu-studio/adaptive-layer-height
- Layer height: https://wiki.bambulab.com/en/software/bambu-studio/layer-height · Line width: https://wiki.bambulab.com/en/software/bambu-studio/parameter/line-width · Seam: https://wiki.bambulab.com/en/software/bambu-studio/Seam · Quality advanced: https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings · Wall generator: https://wiki.bambulab.com/en/software/bambu-studio/wall-generator · Ironing: https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing · Elephant foot: https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot · Overhang slowdown: https://wiki.bambulab.com/en/software/bambu-studio/slow-down-for-overhang · Retraction: https://wiki.bambulab.com/en/software/bambu-studio/parameter/retraction · Fill patterns: https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns · Support: https://wiki.bambulab.com/en/software/bambu-studio/support · Brim: https://wiki.bambulab.com/en/software/bambu-studio/auto-brim · Prime tower: https://wiki.bambulab.com/en/software/bambu-studio/parameter/prime-tower · Purga: https://wiki.bambulab.com/en/software/bambu-studio/reduce-wasting-during-filament-change
- PA: https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa · Flow rate: https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate · Calibrações dev: https://wiki.bambulab.com/en/bambu-studio/Calibration · Criar filamento: https://wiki.bambulab.com/en/bambu-studio/create-filament · Tabela de materiais: https://wiki.bambulab.com/en/general/filament-guide-material-table · Placas: https://wiki.bambulab.com/en/filament-acc/acc/plates · Secagem AMS 2 Pro: https://wiki.bambulab.com/en/ams-2-pro/manual/drying-function
- H2: primeiro print https://wiki.bambulab.com/en/h2/manual/h2d-first-print · FAQ https://wiki.bambulab.com/en/h2/manual/h2d-faq · Dual-nozzle grouping https://wiki.bambulab.com/en/software/bambu-studio/manual/dual-nozzles-slicing-filament-grouping · Área dual https://wiki.bambulab.com/en/h2/manual/printable-range-for-dual-nozzles · Vortek FAQ https://wiki.bambulab.com/en/h2/manual/vortek-faq · Purge H2C https://wiki.bambulab.com/en/software/bambu-studio/h2c-purge-mode · PLA/PETG suporte mútuo https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support · AMS mapping https://wiki.bambulab.com/en/software/bambu-studio/filament-mapping-principle · MakerWorld perfis https://wiki.bambulab.com/en/makerworld/tutorials/print-profile-upload
