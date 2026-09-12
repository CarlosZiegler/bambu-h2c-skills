# Pesquisa: comunidade e experimentos FDM

Consulta: **12 de setembro de 2026**. Nove fontes primárias: relatos, experimentos e orientação oficial. Participantes do fórum não foram verificados como especialistas. Resultados em outra impressora não validam o perfil H2C. Números abaixo descrevem condições publicadas, não receitas universais.

## Suportes e pontes

### C1 — Mesmo material e remoção

[Using same material for supports as the primary material — Bambu Forum](https://forum.bambulab.com/t/using-same-material-for-supports-as-the-primary-material/32491), outubro de 2023 a junho de 2024.

Usuários relatam PLA aderido aos próprios suportes na X1C, com diferenças entre filamentos e danos mesmo usando árvores. Um participante publicou separação Z de 0,22 mm com bico de 0,4 mm e camada de 0,20 mm. **Aplicação:** calibrar separação/interface para aquele material; árvores não garantem acabamento. O valor citado é anedótico. Não transportar distância zero de interface destacável para PLA sobre PLA.

### C2 — PLA/PETG tem duas possíveis falhas

[PLA as support for PETG — Bambu Forum, H2 Series](https://forum.bambulab.com/t/pla-as-support-for-petg/172107), maio a julho de 2025.

O autor informa PLA Basic como suporte de PETG HF, hotend de 0,4 mm e remoção difícil; depois relata melhora parcial. Outro usuário informa que Bambu PETG-HF não adere à interface de Creality PLA. **Aplicação:** testar marca, variante e direção da combinação; a interface precisa permanecer aderida durante a deposição. Não há ensaio controlado. “H2 Series” não confirma H2C. Manter identidade/temperaturas reais do material; não copiar o truque de classificá-lo como outro filamento.

### C3 — Remover facilmente não comprova resistência

[Support Filament → PETG for PLA and PLA for PETG and more — Bambu Forum](https://forum.bambulab.com/t/support-filament-petg-for-pla-and-pla-for-petg-and-more/5942), fevereiro a março de 2023.

Há sucesso relatado usando PLA como separador de PETG, mas também peças rompendo nas camadas de troca. Participantes atribuem o problema à contaminação e relatam ajustes de purga; os volumes divergem. Outro perdeu peças desprendidas da interface pela ventilação. **Aplicação:** verificar integridade após trocas, além da remoção. Identificar quais materiais compartilham hotend na H2C. Não importar volumes, desligamento de torre ou G-code desse tópico antigo de outra arquitetura.

### C4 — Cada ponte precisa de revisão

[Bridge flow testing — Bambu Forum, H2 Series](https://forum.bambulab.com/t/bridge-flow-testing/254508), junho a agosto de 2026.

O autor mostra uma ponte satisfatória e outra cedendo acima do infill no mesmo objeto, usando PLA e ventilador em 100%. Identifica camadas 26 e 36 e espaçamento diferente das trajetórias; não publica solução confirmada. **Aplicação:** revisar pontes externas e fechamento sobre infill separadamente: direção, vão, ancoragem e cobertura. O fluxo 1,5 citado não é recomendação. Aumentar fluxo ou ventilação não foi validado.

## Ensaios e dimensionamento

### E1 — Camada fina não substitui orientação

[Layer height and strength — CNC Kitchen](https://www.cnckitchen.com/blog/the-influence-of-layer-height-on-the-strength-of-fdm-3d-prints), 28 de setembro de 2019.

Ganchos Prusament PLA, Prusa MK2.5, bico de aço de 0,4 mm, três perímetros e camadas de 0,05–0,40 mm foram ensaiados em pé/deitados, também comparando massa. Camadas finíssimas não melhoraram continuamente a resistência; os ganchos em pé ficaram mais fracos. **Aplicação:** orientar pela carga e escolher camada por detalhe, união e tempo. 0,15 mm não constitui lei universal; equipamento experimental, sem validação de cargas críticas.

### E2 — Reforçar onde a carga passa

[Gradient Infill for 3D Prints — CNC Kitchen](https://www.cnckitchen.com/blog/gradient-infill-for-3d-prints), 10 de janeiro de 2020.

Barras em flexão e ganchos receberam infill gradiente por pós-processamento de G-code Cura, em Prusa i3. A comparação por massa/tempo favoreceu a rigidez das barras; nos ganchos não houve ganho significativo sobre aumentar infill convencional. **Aplicação:** posicionar nervuras, espessamentos e reforços de fixação pelo caminho da carga. Reforço local mal colocado também desperdiça material. Não importar o pós-processador ou seus multiplicadores para Bambu; rigidez e resistência são propriedades diferentes.

### E3 — Mais temperatura não melhora sempre

[Extrusion temperature and layer adhesion — CNC Kitchen](https://www.cnckitchen.com/blog/the-influence-of-extrusion-temperature-on-layer-adhesion), 19 de dezembro de 2020.

PLA/PETG dasFilament, Prusa MK3: quatro corpos verticais por temperatura, referências horizontais e segunda série com massa ajustada a aproximadamente ±1%. A adesão inicialmente melhorou e depois caiu nos extremos quentes; aparência e resistência tiveram ótimos diferentes. A causa da queda não foi confirmada. **Aplicação:** avaliar acabamento e união entre camadas, registrando fluxo/velocidade e filamento. Não copiar extremos fora das faixas do fabricante nem tratar esses resultados como perfil Bambu.

### E4 — Ventilação depende do defeito

[Transparent FDM 3D Prints are Clearly Stronger! — CNC Kitchen](https://www.cnckitchen.com/blog/transparent-fdm-3d-prints-are-clearly-stronger), 10 de setembro de 2022.

PETG transparente dasFilament recebeu parâmetros lentos para transparência e ensaios de tração/impacto. Após defeitos sem ventilação, uma série com 30% apresentou menos problemas e melhor resultado estrutural. **Aplicação:** evitar tanto “fan zero sempre fortalece” como “fan máximo resolve pontes”; considerar material, geometria e tempo por camada. A porcentagem daquele equipamento não equivale à vazão da H2C. Não transferir sobre-extrusão ou perfil de transparência para peças comuns.

### D1 — Perímetros e infill cumprem funções diferentes

[Infill — Prusa Knowledge Base](https://help.prusa3d.com/article/infill_42), consultada em setembro de 2026; data editorial não confirmada.

A orientação oficial destaca perímetros para resistência, infill para apoiar camadas superiores e contribuir à compressão; 100% pode prejudicar aparência. **Aplicação:** diferenciar carcaça decorativa, parede funcional e região de parafuso/carga. Conferir espessura, perímetros e cobertura superior efetivamente fatiados antes de aumentar tudo. É orientação qualitativa de fabricante, não ensaio independente nem dimensionamento da peça: suas porcentagens para modelos comuns não substituem carga, orientação e material.

## Inferências para integrar às skills

- Rebaixo inferior apenas ornamental: considerar base plana, detalhe em outra face ou pés separados. Preservar funções/encaixes; se o vão for necessário, comparar orientação, divisão e suporte. Inferência de projeto; não teste da Mini Fábrica.
- Revisar suporte real: cobertura, ancoragem, acesso de remoção, separações e interface/material.
- Calibrar com seção que preserve vão, altura suspensa, orientação e contato. Registrar antes/depois e critério de aceitação; isolar variáveis quando procurando a causa.
- Separar revisão digital de impressão fisicamente aprovada. Nenhuma fonte aqui valida o conjunto do usuário.
