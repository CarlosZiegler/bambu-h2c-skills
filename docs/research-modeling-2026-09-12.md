# Pesquisa de modelagem e camadas — 2026-09-12

Complementa as notas de [materiais/H2C](research-h2c-materials-2026-09-12.md) e [comunidade/ensaios](research-community-2026-09-12.md). Os critérios aplicados estão nas referências instaláveis de [modelagem](../skills/blender-print-ready/references/design-for-fdm.md) e [suporte/processo](../skills/bambu-h2c-slice-print/references/support-and-process-tuning.md).

## Fontes primárias consultadas

| Fonte | Evidência que mudou a orientação |
|---|---|
| [Blender Solidify, manual 4.5](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html) | Espessura afetada pela escala local e por limitações do offset; medir a malha avaliada após modifiers |
| [3D Print Toolbox, manual 4.1](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html) | Separar checks de malha/espessura das ações de reparo; manual histórico, operadores precisam ser descobertos na instalação |
| [Extensão atual 3D Print Toolbox](https://extensions.blender.org/add-ons/print3d-toolbox/) | Changelog 1.4.1, 05/08/2026, registra comportamento de exportação STL no Blender 5.2; conferir viewport/render e arquivo reimportado |
| [Prusa: modelagem para impressão](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) | Orientação, divisão, chanfro inferior, material e tolerância entram durante o desenho |
| [Prusa: camadas e perímetros](https://help.prusa3d.com/article/layers-and-perimeters_1748) | Separar resolução XY/Z e espessura sólida em mm; fechamento sobre infill merece revisão própria |
| [Prusa: Arachne](https://help.prusa3d.com/article/arachne-perimeter-generator_352769) | Linha variável pode preservar ou alterar detalhes; não impor múltiplo exato do diâmetro do bico como lei de modelagem |
| [Bambu: camada variável](https://wiki.bambulab.com/en/software/bambu-studio/adaptive-layer-height) | Compatibilidade com suporte e torre depende da configuração; revisar restrições na versão instalada |
| [Bambu: suporte](https://wiki.bambulab.com/en/software/bambu-studio/support) e [pintura](https://wiki.bambulab.com/en/software/bambu-studio/support-painting) | Escolher estratégia por região, conferir pintura/automático e separar corpo, interface e gaps |
| [Bambu: PLA/PETG para suporte](https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support) | Guia limitado a produtos Bambu específicos; preservar marca, direção da combinação e perfil H2C |
| [Prusa: infill patterns](https://help.prusa3d.com/article/infill-patterns_177130) | Cruzamentos no preenchimento podem gerar colisão; considerar padrão e cobertura superior, não só porcentagem |
| [Prusa: elephant foot](https://help.prusa3d.com/article/elephant-foot-compensation_114487) | Compensação inicial difere de ajuste global de dimensões/folgas |
| [Bambu Studio #4387](https://github.com/bambulab/BambuStudio/issues/4387) | Relato de 2024 e resposta técnica de 2025 sobre detalhes Arachne; motiva inspeção, não afirma defeito em toda versão atual |

## Decisões de integração

A preferência por uma base plana quando o rebaixo seria apenas ornamental é uma **inferência de projeto para o uso solicitado**, não uma ordem de eliminar todos os rebaixos. Preservar função, encaixes e aparência continua sendo requisito. A dimensão da parede acompanha função, orientação, material e trajetórias efetivas; reforço localizado é uma alternativa a avaliar, não promessa de resistência.

Não foi criado um preset único “anti-espaguete”. As skills passam a conduzir decisões antes da exportação, a escolher ajustes pela evidência e a registrar o contexto de testes para reutilização futura. Nenhuma configuração da impressora foi alterada nesta pesquisa.

Páginas Blender/Bambu que retornaram 402 no leitor de pesquisa foram acessadas nas mesmas URLs oficiais por HTTP direto e lidas como texto. Nenhum conteúdo pago ou autenticado foi contornado. Datas editoriais ausentes não foram inferidas a partir da data de consulta.
