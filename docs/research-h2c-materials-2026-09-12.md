# Pesquisa oficial: H2C, materiais e configurações

Consulta: **12/09/2026**. Fontes primárias; ensaios de comunidade constam em outra nota. Não houve operação da impressora nem validação física. Valores publicados são condicionados ao produto, método e versão, não garantias de sucesso.

## Evidências e implicações

**Volume útil — evidência forte, versão explícita.** O manual H2C V1.0, jan/2026, pp.90–91, informa esquerda X0–325/Y0–320/Z320 mm; direita X25–330/Y0–320/Z325; região XY comum X25–325/Y0–320. Firmware prevalece se houver divergência. **Aplicação:** conferir o perfil atual e a posição de peça, suporte, interface e torre por hotend. Não assumir que toda a placa serve aos dois bicos nem um volume genérico único. [Manual H2C](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf).

**Compatibilidade — evidência forte, sujeita a firmware.** O guia H2C descreve TPU 85A/90A/95A HF à direita; flexíveis macios não fazem as trocas automáticas comuns do Vortek. PET/PPA/PPS-CF são restringidos à esquerda pelo percurso do filamento. PVA/PETG em hotends opostos é proibido; há alternativa descrita pela direita com AMS. **Aplicação:** decidir material, alimentação e hotend antes de desenhar multimateriais ou suporte solúvel; conferir a combinação atual. [H2C Filament Printing Guide](https://wiki.bambulab.com/en/h2c/h2c-filament-printing-guide).

**TPU for AMS — evidência forte para produto específico.** É **68D**, diferente de TPU 95A ou mais macio. A ficha V1.0 lista bicos 0,4/0,6/0,8 mm e secagem em ar forçado a 70 °C/8 h. **Aplicação:** não colocar qualquer TPU no AMS nem usar um perfil genérico. Escolher dureza e geometria pela flexibilidade pretendida; validar o encaixe com um cupom é recomendação de engenharia. [TDS TPU for AMS](https://store.bblcdn.eu/s8/default/0b83dc5419534babb4287686cb8c7375/Bambu_TPU_for_AMS_Technical_Data_Sheet.pdf).

**PLA/PETG HF — dados de laboratório, não dimensionamento final.** PLA Basic V3.0 apresenta módulo XY 2580 MPa/HDT 54 °C a 1,8 MPa; PETG HF V1.0, 1810 MPa/62 °C. “PETG sempre mais rígido” é falso. As fichas distinguem XY/Z e condições dos corpos de prova. **Aplicação:** escolher por carga, flexão, impacto, calor e orientação; não calcular capacidade de uma peça somente pelo nome do polímero. [TDS PLA Basic](https://store.bblcdn.com/s7/default/b189de92249a4b9ebed28b8ea1f080f0/Bambu_PLA_Basic_Technical_Data_Sheet.pdf), [TDS PETG HF](https://store.bblcdn.com/ce12d65176a94f1086e6aefa238e62e2.pdf).

**Versões divergentes — evidência direta.** Duas fichas PETG HF chamadas V1.0 diferem no resfriamento: “ligado” versus 0–60%. Ambas indicam secagem em ar forçado a 65 °C/8 h; mesa é outro método. **Aplicação:** registrar a fonte exata, conferir o preset H2C atual e não transformar percentuais ou limites aproximados de ponte em regra universal. [Segunda ficha PETG HF V1.0](https://store.bblcdn.com/s6/default/20423d7f839c4a66b9712508549c68b4/Bambu_PETG_HF_TDS.pdf).

**Calibração — conceitos fortes; interfaces variam por impressora.** Não confundir:

| Ajuste | Função | Evidência que justifica investigar |
|---|---|---|
| Flow ratio / Flow Rate | Multiplicador de extrusão | Excesso/lacunas persistentes |
| Flow Dynamics / K | Compensa atraso de pressão nas mudanças de velocidade | Defeitos em cantos/transições; troca de material/hotend/temperatura |
| Maximum volumetric speed | Limite de extrusão em mm³/s | Subextrusão ao aumentar velocidade/largura/altura |

Os guias ainda têm seções X1/A1/H2D: não transportar seus botões, Lidar ou limites de bico para H2C. Material úmido e bico obstruído distorcem calibrações. **Aplicação:** verificar a opção real, diagnosticar antes de calibrar e salvar resultados pela combinação utilizada. [Flow Rate Calibration](https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate), [Flow Dynamics Calibration](https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa).

**Fluxo volumétrico — evidência forte.** Aproximação: **Q = altura × largura × velocidade**. Exemplo didático: 0,20 × 0,45 × 200 = 18 mm³/s; a 300 mm/s, 27 mm³/s. Não são presets recomendados. Aumentar o limite no software não aumenta a capacidade física do hotend. **Aplicação:** começar pelo preset compatível, verificar a prévia de fluxo/velocidade e investigar subextrusão antes de elevar limites. [Volumetric speed](https://wiki.bambulab.com/en/knowledge-sharing/volumetric-speed).

**Secagem — evidência forte, dependente do equipamento.** O guia distingue mesa, ar forçado e AMS; AMS 2 Pro pode não secar completamente certos materiais. Há condições específicas para rotação, impressão simultânea e outros rolos sensíveis ao calor. **Aplicação:** registrar método/material, manter armazenamento seco e não afirmar “seco” por embalagem nova, dessecante ou leitura de umidade isolada. Não adotar temperatura/tempo universal. [Filament Drying Recommendations](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament).

**Placa — evidência forte, escopo Smooth PEI/High Temperature Plate.** O guia recomenda água/detergente, cola protetora para materiais além de PLA e resfriamento antes da remoção; calor excessivo pode causar pé de elefante/entupimento. **Aplicação:** identificar superfície e polímero; não estender a regra da Smooth PEI a todas as placas. Brim aumenta contato, mas não resolve uma plataforma suspensa. [Smooth PEI troubleshooting](https://wiki.bambulab.com/en/general/high-temperature-plate-not-working-as-expected).

**Preset — evidência forte sobre o arquivo, não sobre a instalação local.** O perfil público PETG HF/H2C usa herança, listas de parâmetros e resfriamento específico. **Aplicação:** preservar a herança; não selecionar arbitrariamente um elemento de uma lista nem importar `master` inteiro. Registrar versão e conferir parâmetros efetivos no 3MF salvo. [Perfil oficial PETG HF/H2C](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/filament/Bambu%20PETG%20HF%20%40BBL%20H2C.json).

## Integração sugerida nas skills

Estas são recomendações de engenharia inferidas das fontes:

- Identificar marca/formulação, uso, carga, calor e flexão antes de dimensionar. O rótulo “PLA Basic” isolado não comprova que seja Bambu.
- Separar espessura geométrica, paredes, largura de linha, camadas sólidas e infill; cada peça precisa de justificativa própria.
- Evitar suportes desnecessários pela orientação/geometria, preservando função; quando necessários, validar cobertura e material antes de afinar interface e velocidade.
- Registrar hipótese, ajuste e teste. Não usar calibração, cola ou infill como substitutos do apoio de uma camada.
- Agrupar mesma cor/material na mesma plate quando compatível; documentar exceções por suporte, temperatura, hotend ou alimentação.

## Limites de acesso e atualização

Datas de alteração das páginas Wiki não estavam claras; registra-se consulta, sem inventar publicação. TDS usa a versão do PDF; `master` é mutável. O leitor web retornou 402 em páginas públicas da Wiki, mas a leitura HTTP direta dessas mesmas páginas funcionou. A página comercial PETG HF retornou 403; os números finais vieram dos documentos acessíveis. Não há garantia física derivada desta pesquisa.
