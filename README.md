# bambu-h2c-skills

Skills para **Codex e Claude** no fluxo **Blender → Bambu Studio → Bambu Lab H2C**, com foco em modelagem, apoio real, fatiamento e diagnóstico baseado em evidência.

Uma malha pode ser fechada, tocar a mesa e ainda começar uma plataforma no ar. As skills verificam geometria **e** camadas críticas, preservam os arquivos originais e distinguem validação digital de teste físico.

| Skill | Quando usar |
|---|---|
| [`blender-print-ready`](skills/blender-print-ready/SKILL.md) | Criar/ajustar peças, unidades, folgas, montagem, orientação e exportação sem destruir a cena original |
| [`fdm-print-preflight`](skills/fdm-print-preflight/SKILL.md) | Antes da entrega, ou após mudar geometria/orientação/suporte: contato real, faces inferiores elevadas, camadas críticas e arquivo final reaberto |
| [`bambu-h2c-slice-print`](skills/bambu-h2c-slice-print/SKILL.md) | Preparar e conferir o projeto H2C, suporte por objeto, plates por cor e mapeamento; operar a impressão quando autorizado |
| [`bambu-print-troubleshoot`](skills/bambu-print-troubleshoot/SKILL.md) | Diagnosticar falhas, espaguete, cantilever ou HMS, distinguindo falta de apoio de adesão/material/mecânica |

## Instalação

Instale as **quatro pastas juntas**, como diretórios irmãos: elas compartilham o preflight e referências. As skills não presumem que um MCP esteja conectado nem instalam ferramentas ou iniciam uma impressão por conta própria.

### Codex

Peça ao Codex para instalar as quatro skills deste repositório, ou copie as pastas de `skills/` para `~/.codex/skills/`. Preserve/compare uma instalação existente antes de substituí-la. Cada pasta contém `SKILL.md`; o preflight também contém `scripts/`, `references/` e metadados de interface. As skills ficam disponíveis em um próximo turno após a instalação.

Exemplo: “Use $fdm-print-preflight para conferir este projeto antes de entregar os arquivos de impressão.”

### Claude Code (plugin)

```text
/plugin marketplace add CarlosZiegler/bambu-h2c-skills
/plugin install bambu-h2c-skills@bambu-h2c-skills
```

### Claude Code (pastas de skills)

Copie as quatro pastas de `skills/` para `~/.claude/skills/` ou `.claude/skills/` no projeto. Inclua referências e scripts; copiar apenas o texto do `SKILL.md` perde a checagem executável e os links locais.

## Check executável de STL

Python 3.10+; sem Blender, rede ou dependências externas para este helper:

```bash
python3 skills/fdm-print-preflight/scripts/audit_stl.py pecas/*.stl \
  --output preflight-geometria.json
```

- Analisa todos os STLs informados, na orientação de impressão e assumindo coordenadas em mm; `--unit-scale` e `--bed-z` permitem convenção explícita diferente.
- Não modifica STLs. Detecta bordas abertas, winding inconsistente, cascas/volumes problemáticos, falta de contato plano e faces inferiores elevadas, inclusive plataformas sobre pés.
- Saída `0`: triagem sem achados, ainda requer revisão do slice. `2`: geometria bloqueada ou apoio precisa de revisão. `1`: entrada/leitura inválida. Consulte o JSON para o motivo.
- É uma triagem conservadora: chanfros/curvas autoportantes também podem pedir revisão. Não mede espessura, auto-interseção, contenção exata de cascas, estabilidade, resistência ou capacidade de ponte. Não lê transformações/configurações de 3MF nem comprova que o suporte foi gerado no lugar correto.

O [guia de suporte](skills/fdm-print-preflight/references/support-and-slice-review.md) explica como fechar achados com evidência do slicer. O [modelo de relatório](skills/fdm-print-preflight/references/preflight-report.md) registra decisões, arquivos e checks pendentes.

## Validação do repositório

```bash
python3 -m pip install -r tests/requirements.txt
python3 -m unittest discover -s tests -v
```

Os testes geram modelos pequenos: base fechada sobre quatro pés, vão de 0,25 mm, overhang alto, objeto suspenso, casca invertida, faces duplicadas/degeneradas e STLs truncados. Conferem também preservação dos arquivos, códigos de saída e integridade dos links/empacotamento das skills. Não enviam nada à impressora. O CI roda esses testes em cada push/PR.

A revisão que motivou as mudanças está em [docs/review-2026-09-12.md](docs/review-2026-09-12.md).

## Limites e operação

- Use perfil, firmware, bico, material e placa reais. Limites de máquina e valores de suporte não são universais; confira documentação oficial/perfil instalado.
- Zero warnings, malha manifold e saída bem-sucedida do slicer não bastam: revise a primeira camada e cada transição crítica, depois reabra a entrega.
- Modelar/corrigir/fatiar não autoriza enviar, retomar ou cancelar um print. Autorizações explícitas da sessão são preservadas.
- Nenhuma skill garante aderência ou sucesso físico. Registre separadamente “modelo conferido”, “slice conferido” e “teste físico concluído”.

## Contribuindo

PRs bem-vindos. Inclua evidência para regras novas, identifique números de perfil como exemplos e adicione regressões quando um caso puder ser testado. Não publique fotos, credenciais ou arquivos privados de projetos sem autorização.

## Licença

MIT
