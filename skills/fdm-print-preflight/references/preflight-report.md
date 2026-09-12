# Registro de preflight

Preencha com evidência, sem transformar campos vazios em aprovação. Guarde junto à entrega; resuma o essencial ao usuário. Use caminhos relativos/IDs de artefato em relatórios compartilhados, sem credenciais ou dados privados da impressora.

## Arquivos e configuração

- Origem e versão preservada:
- Arquivo final reaberto (nome, versão e hash ou identificação equivalente):
- Ferramentas/versões, perfil H2C, modo/bico/diâmetro, placa e processo:
- Materiais e atribuição efetiva por filamento/bico:
- Plates, cor/material e quantidade de peças por plate:

## Geometria — uma linha por peça

| ID / peça / plate | Dimensões e orientação | Montagem / tolerância | Malha e espessuras | Contato real / mínimo Z | Regiões inferiores e alturas | Decisão e evidência |
|---|---|---|---|---|---|---|
| Preencher | mm e face de apoio | cola/encaixe/etc. | checks executados e não verificados | área plana, estabilidade | inclusive pés/rebaixos/ilhas | reorientação/redesenho/suporte/ponte |

## Fatiamento — uma linha por região crítica

| Peça / região / Z | Parâmetros efetivos por objeto | Antes / início / depois | Apoio localizado / interface | Avisos e resolução | Evidência |
|---|---|---|---|---|---|
| Preencher | suporte, pontes, blockers, filamento | camadas/alturas inspecionadas | onde chega e separação | ausência não é aprovação | captura/trajectórias/medição |

- Primeira camada de todas as peças conferida:
- Letras, paredes, encaixes e partes pequenas presentes no preview:
- Espaço de brim/suporte/torre e colisões conferidos:
- Estimativa de tempo/material e diferença em relação à versão anterior:
- 3MF reaberto como projeto e configurações preservadas:
- Plates alterados refatiados; demais comparados com a versão preservada:
- Suporte removível, acesso e instrução de montagem:

## Estado final

- Modelagem e exportação: concluídas / pendentes.
- Geometria: verificada nos checks listados / achados abertos / checks não executados.
- Fatiamento e camadas críticas: conferidos / pendentes.
- Impressão física: não testada / em teste autorizado / concluída com evidência.
- Limites e próximo teste necessário:

Somente evidência do teste físico permite registrar “impressão física concluída”. Aprovação visual, `screen_pass` do helper ou sucesso do slice não substituem esse teste.
