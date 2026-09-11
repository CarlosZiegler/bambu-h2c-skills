# bambu-h2c-skills

Skills para agentes Claude (Claude Code, Cowork, Agent SDK) cobrindo o fluxo completo **Blender → Bambu Studio → Bambu Lab H2C**, com foco em qualidade de impressão e prevenção de erros. Conteúdo baseado na wiki oficial da Bambu Lab, no manual do Blender 4.2 e em guias de design para FDM (Prusa, Rahix, Hydra Research).

| Skill | Quando o agente usa | Cobre |
|---|---|---|
| [`blender-print-ready`](skills/blender-print-ready/SKILL.md) | Criar, ajustar, verificar ou exportar um modelo no Blender para impressão | Cena em mm, modelagem precisa (booleans, solidify, bevel, screw, bisect), sculpt → print, regras de design FDM com números, higiene de malha, script de verificação com critérios de aprovação, multi-cor, export STL/3MF, tabela de erros |
| [`bambu-h2c-slice-print`](skills/bambu-h2c-slice-print/SKILL.md) | Operar o Bambu Studio e enviar/monitorar prints na H2C | Particularidades da H2C (Vortek, dual nozzle), todas as ferramentas de preparação do Studio, abas de processo explicadas, suportes, agrupamento de filamentos, placas/filamentos/secagem, calibrações, checklist pré-print, MCP e CLI headless |
| [`bambu-print-troubleshoot`](skills/bambu-print-troubleshoot/SKILL.md) | Um print falhou, apareceu código HMS ou há defeito de qualidade | Códigos HMS da série H2, tabela sintoma → causa → correção, rotina do agente (pausar, foto, uma correção por vez) |

## Instalação

### Claude Code (como plugin)
```bash
/plugin marketplace add <seu-usuario>/bambu-h2c-skills
/plugin install bambu-h2c-skills@bambu-h2c-skills
```

### Claude Code (skills soltas, sem plugin)
Copie as pastas de `skills/` para `~/.claude/skills/` (global) ou `.claude/skills/` (por projeto).

### Cowork / claude.ai
Abra cada `SKILL.md`, copie o conteúdo e salve como skill pessoal, ou peça ao Claude para propor as skills a partir deste repositório.

## Ferramentas que as skills assumem
- **Blender MCP** conectado (ex.: [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) ou a integração Blender do Claude desktop) — a skill roda `bpy` via `execute_blender_code`.
- **Bambu Studio ≥ 2.4** com perfil H2C.
- Opcional: **MCP da impressora** — [DMontgomery40/bambu-printer-mcp](https://github.com/DMontgomery40/bambu-printer-mcp) (`BAMBU_MODEL=h2c`, LAN + Developer Mode). Projeto comunitário, não oficial da Bambu Lab: leia o código antes de instalar.

## Regras de segurança embutidas
- O agente nunca exporta um modelo sem passar no script de verificação (manifold, mm, espessuras).
- O agente nunca envia um print sem revisar o preview e o checklist.
- O agente pode **pausar** um print sozinho, mas **cancelar** só com confirmação do usuário.
- Uma correção por vez; teste pequeno antes de reimprimir a peça inteira.

## Limitações conhecidas
- A wiki da Bambu não documenta os valores padrão de walls/infill por preset nem a opção "Precise wall"; nesses pontos as skills usam recomendações da comunidade.
- Suporte à H2C no OrcaSlicer ainda é instável (jul/2026); as skills assumem Bambu Studio.

## Contribuindo
PRs bem-vindos — especialmente medições reais (tolerâncias, contração, perfis) feitas na H2C. Mantenha os links para a fonte oficial em cada regra nova.

## Licença
MIT
