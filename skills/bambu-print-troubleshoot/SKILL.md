---
name: bambu-print-troubleshoot
description: Use when a Bambu Lab H2C print fails, shows an HMS code, or has quality defects — adhesion, warping, stringing, spaghetti, clogs, layer shifts, elephant foot, purge/color bleed, dimensional errors — to diagnose and fix one variable at a time.
---

# Diagnóstico de falhas — Bambu Lab H2C

Método: **1) coletar evidência** (status MCP, código HMS, foto da câmera, filamento/placa/perfil/processo usados, em que altura falhou) → **2) classificar** (adesão · extrusão/material · geometria/suporte · mecânica · configuração dual/Vortek) → **3) aplicar UMA correção por vez** → **4) reimprimir um teste pequeno** (mesma região do problema) antes da peça inteira → **5) registrar** parâmetro, valor antigo → novo. Nunca mude cinco coisas de uma vez; nunca cancele um print sem confirmação do usuário (pausar é permitido).

## Códigos HMS
Formato 4 blocos: módulo–parte–nível–ID. Nível 0001 erro (para), 0002 aviso, 0003 info. **Sempre** consultar o código exato em https://wiki.bambulab.com/en/hms/home antes de agir. Detecção por IA na série H2 (https://wiki.bambulab.com/en/h2/manual/intelligent-detection):
- 0300-8003 espaguete (nozzle cam) · 0C00-803F acúmulo no bico · 0C00-8040 extrusão em ar / sem extrusão
- 0500-806E objeto estranho na placa · 0C00-0300-0002-000C tipo/posição da placa · 0500-8053 hotend ≠ perfil
- 0C00-0300-0002-000x inspeção de 1ª camada (ex.: -0005 timeout)

## Sintoma → causa provável → correção (em ordem de probabilidade)
- **Não adere / descola / warping**: placa suja ou tipo errado no slicer; mesa fria; base pequena; correntes de ar; contração (ABS/ASA/PC). → Lavar placa (detergente + água morna, não IPA); conferir placa no slicer; +5–10 °C mesa; brim Auto/Painted; chanfro nas arestas; porta fechada + câmara para ABS/ASA; **cola** se PEI lisa + PETG; Cool Plate/SuperTack para PLA difícil.
- **Espaguete** (0300-8003): adesão falhou, suporte caiu, peça tombou, colisão do bico. → Corrigir adesão; suportes Tree Hybrid/Strong com base maior ou Normal Grid; brim; reorientar para mais base; reduzir velocidade em peças altas; manter detecção ligada.
- **Stringing / bolinhas / superfície áspera / estalos / bolhas**: filamento **úmido** (causa nº 1); temperatura alta; retração. → Secar (PLA 55 °C 8 h, PETG 70, ABS/ASA 75–85, TPU 65–75); rodar Flow Dynamics; −5 °C; retraction test (0,2–0,4 mm limpa a torre); TPU um objeto por plate, sem AMS.
- **Elephant foot / 1ª camada esmagada**: compensação 0; mesa quente demais. → Elephant foot compensation 0,10–0,20 mm (calibrar com cubo 25×25×10), −5–10 °C na 1ª camada, chanfro 45° na base.
- **Layer shift**: colisão com peça/suporte/warping levantado, placa mal encaixada, velocidade alta em peça alta, sujeira nos trilhos. → Placa encaixada até o fim; Z-hop Auto/Slope; reduzir outer wall/travel em peças altas; checar detritos e correias; evitar arestas que levantam.
- **Entupimento / underextrusion / extrusão em ar** (0C00-8040): PLA com câmara quente/porta fechada; filamento de suporte com temp incompatível; filamento úmido; hotend errado no rack; max volumetric speed alto demais em preset genérico. → Porta aberta para PLA; suporte compatível (Support for PLA vs PETG); secar; conferir hotend ID; calibrar Max Flowrate (−5–10 %); cold pull / trocar hotend Vortek.
- **Paredes finas ausentes / gaps entre paredes**: modelo < 2 perímetros; Arachne mal interpretando; flow baixo. → Redesenhar ≥ 0,9 mm (blender-print-ready); testar Classic wall generator; Flow Rate fine.
- **Furos/dimensões erradas**: sem Precise wall; sem hole compensation; flow alto; contração. → Precise wall ON; wall order outer/inner; XY hole/contour compensation (+0,1–0,2); calibrar Flow Rate; shrinkage no perfil do filamento.
- **Topo com buracos/pillowing**: poucas top shells sobre infill esparso. → Top shells ≥ 5; infill 20 %+ ou gradiente; ironing só se plano.
- **Seam feio / zits**: posição automática ruim; seam gap; PA errado. → Seam pintado; Aligned/Back; scarf seam em cascas curvas; rodar Flow Dynamics.
- **Overhang caído / superfície suportada ruim / pontes cedendo**: > 45° sem suporte; top Z distance errado; bridge flow/speed. → Suporte (0,2 mm mesmo filamento; **0 mm com filamento de interface no outro bico**); reorientar; ↓ overhang speed; ↑ bridge flow, ↓ bridge speed; mais cooling em PLA.
- **Purga excessiva / manchas de cor / cor suja**: trocas dentro do mesmo bico; flush baixo escuro→claro; prime tower off. → Grouping *Filament-saving*; uma cor/suporte por bico; prime tower ON + flush into support/infill/object; ↑ flush volume escuro→claro; purge mode H2C.
- **Hotend mismatch (0500-8053) / posição Vortek**: perfil diz 0,4 mas a posição tem 0,6. → Corrigir config do rack no perfil ou trocar o hotend; nunca ignorar.
- **Falha na inspeção de 1ª camada**: ver a foto; normalmente adesão, nivelamento, bico sujo, placa errada. → Limpar placa e bico; bed leveling ON; conferir placa; repetir.
- **Fatiamento estranho (infill faltando, paredes duplas, "redundant paths")**: cascas sobrepostas/faces internas do Blender. → Voltar ao modelo (Boolean Union, deletar faces internas) ou Mesh Boolean no Studio; Fix model como último recurso.
- **Peça fraca / quebra em camadas**: orientação errada, poucas walls, filamento úmido, temp baixa. → Reorientar carga no XY; 3–4 walls; secar; +5–10 °C; câmara fechada para ABS/ASA.
- **Timelapse/LAN print não inicia**: sem pendrive na H2 / LAN mode sem access code. → Inserir pendrive; conferir IP e access code; Developer Mode para MCP.

## Rotina do agente ao detectar erro
1. `get_printer_status` + `camera_snapshot` (MCP) → registrar código HMS, altura/camada, tempo decorrido.
2. Erro nível 0001 ou espaguete visível: **pausar** (`pause_print`) e reportar ao usuário com foto e diagnóstico provável; cancelar só com confirmação. Avisos 0002: reportar e seguir monitorando.
3. Buscar o código na wiki HMS; propor a correção mais provável desta tabela + teste pequeno de validação (cubo, torre, ou recorte da região problemática via Cut no Studio).
4. Após a correção, aplicar no perfil/modelo, salvar preset com nome novo e registrar o que mudou. Se dois prints seguidos falharem pelo mesmo motivo, parar e revisar o modelo (skill blender-print-ready) antes de mexer mais no slicer.

## Referências
- HMS: https://wiki.bambulab.com/en/hms/home · Intro HMS: https://wiki.bambulab.com/en/x1/troubleshooting/intro-hms · Detecção H2: https://wiki.bambulab.com/en/h2/manual/intelligent-detection
- Placas: https://wiki.bambulab.com/en/filament-acc/acc/plates · PEI texturizada: https://wiki.bambulab.com/en/general/textured-PEI-plate-not-working-as-expected · Secagem: https://wiki.bambulab.com/en/filament-acc/filament/dry-filament · Tabela de materiais: https://wiki.bambulab.com/en/general/filament-guide-material-table
- Elephant foot: https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot · Bridging: https://wiki.bambulab.com/en/filament-acc/filament/print-quality/bridging · Purga: https://wiki.bambulab.com/en/software/bambu-studio/reduce-wasting-during-filament-change · Contração: https://wiki.bambulab.com/en/knowledge-sharing/3d-prints-shrinkage · Calibrações: https://wiki.bambulab.com/en/bambu-studio/Calibration
