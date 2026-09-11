---
name: blender-print-ready
description: Use when creating, adjusting, checking or exporting a Blender model for FDM printing on the Bambu Lab H2C — scene in mm, precise modeling, booleans, sculpt cleanup, FDM design rules, mesh hygiene, multi-color, STL/3MF export.
---

# Blender → modelo pronto para impressão FDM (Bambu Lab H2C)

Papel do agente: transformar qualquer modelo Blender em um sólido **manifold, em milímetros, com espessuras imprimíveis e sem overhangs escondidos**, e entregar STL/3MF que o Bambu Studio abre sem "Fix model". Fluxo obrigatório: **1 Setup da cena → 2 Modelar com regras FDM → 3 Higiene de malha → 4 Verificação (script) → 5 Export → 6 Conferir dimensões**. Nunca pule a etapa 4.

## 0. Ferramentas disponíveis
- Blender via MCP (computador do usuário): `mcp__remote-devices__Blender__execute_blender_code` (roda bpy — ferramenta principal), `get_objects_summary` / `get_object_detail_summary` (inventário da cena), `render_viewport_to_path` ou `get_screenshot_of_area_as_image` (conferir visualmente), `search_manual_docs` / `search_api_docs` / `get_python_api_docs` (dúvidas de API — consulte antes de chutar nomes de operadores).
- Extensões (Blender 4.2+): **3D Print Toolbox** (`bl_ext.blender_org.print3d_toolbox`) — instalar com `bpy.ops.extensions.package_install(repo_index=0, pkg_id="print3d_toolbox")`; **3MF Import/Export** (`threemf-io`) para multi-cor; opcionais: Bool Tool, MeasureIt, Precision Drawing Tools (PDT), CAD Sketcher, Mesh Repair Tools.
- Regra: sempre trabalhe em uma cópia (`obj.copy()` + `obj.data.copy()`) antes de aplicar modifiers destrutivamente, e salve o .blend antes de operações em massa.

## 1. Setup da cena (conceito básico mais ignorado)
STL/OBJ não têm unidade; o slicer assume **1 unidade = 1 mm**. O Blender nasce com 1 BU = 1 m, então o cubo padrão (2 m) vira 2 mm no Bambu Studio. Configure:
```python
import bpy
sc = bpy.context.scene
sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 0.001; sc.unit_settings.length_unit = 'MILLIMETERS'
for a in bpy.context.screen.areas:
    if a.type == 'VIEW_3D':
        for s in a.spaces:
            if s.type == 'VIEW_3D':
                s.overlay.grid_scale = 0.001; s.clip_start = 0.01; s.clip_end = 5000
                s.overlay.show_face_orientation = True   # azul = fora, vermelho = dentro
```
- Grid: linha fina = 1 mm, grossa = 10 mm. Clip start 0,01 / end 5000 evita geometria sumindo.
- Volume de referência da H2C: cubo com dimensões 325×320×320 mm (bico esquerdo) ou 300×320×325 mm (modo dual/Vortek), `display_type='BOUNDS'`, `hide_select=True`. Tudo que sair disso precisa ser cortado.
- Campos aceitam expressões: `12mm`, `24/2`, `0.5in`. Antes de qualquer export: `Ctrl+A → Scale` (ou `transform_apply(scale=True, rotation=True)`) — Scale deve ler 1.000 no N-panel.

## 2. Modelagem precisa (peças funcionais)
- Dimensões absolutas: N-panel → Item → Dimensions; em Edit Mode, Item → Median mostra coordenadas de vértices. Snapping (`Shift+Tab`) para Vertex/Edge/Face/Increment.
- Extrude `E`, Inset `I`, Bevel `Ctrl+B` + digitar valor em mm; ajuste fino em F9 (Adjust Last Operation).
- **Mirror**: ativar *Clipping* antes de puxar vértices até o eixo; *Merge* com distância 0,001 mm; *Bisect* para cortar e espelhar metade.
- **Array**: usar *Constant Offset* em mm (não Relative); *Merge* quando as cópias se tocam.
- **Boolean** (a maior fonte de malha quebrada):
  - Solver **Exact** por padrão (suporta geometria sobreposta); *Fast* só em cortes simples e rápidos. *Self Intersection* se o cutter se auto-intersecta; *Hole Tolerant* só se o Exact der erro.
  - Cutters em uma coleção "Cutters" com `display_type='WIRE'` e excluídos do render; Operand Type = Collection para vários cutters.
  - Nunca deixe faces **coplanares** entre operandos: desloque o cutter 0,01 mm além da superfície. Coplanar = resultado non-manifold.
  - Ordem típica de modifiers: Mirror/Array → Boolean → Bevel. Aplique de cima para baixo só no fim, numa cópia.
  - Só malhas manifold como operandos garantem resultado manifold — limpe antes de cortar.
- **Solidify** (dar espessura a cascas): modo *Complex* (garante saída manifold), *Even Thickness* ON, Offset −1 (para dentro) ou +1, Thickness ≥ 0,9 mm (2 perímetros) e de preferência 1,2–2 mm. Aplique escala antes: escala não uniforme dá parede desigual.
- **Bevel modifier**: Segments = 1 → chanfro; ≥ 4 → fillet. *Limit Method: Angle* (30°) para não chanfrar faces planas; *Clamp Overlap* ON; Weight/Vertex Group para arestas específicas.
- **Screw modifier** para roscas: perfil alinhado ao eixo, Angle 360°, Screw = passo (mm/volta), Iterations = voltas, Steps 32–64, Merge ON; depois Boolean Union no eixo. Roscas só ≥ M5 impressas; abaixo disso, furo a 90 % do diâmetro para macho ou insert térmico (98 %).
- **Bisect** (`Mesh → Bisect`): plano numérico + *Fill* + *Clear Inner/Outer* para partir peças grandes; adicione pinos de alinhamento Ø ≥ 1,8 mm e furos +0,2–0,3 mm.
- Texto: `Add → Text`, extrudar ≥ 0,5 mm de profundidade, traço ≥ 0,6 mm; converter para mesh (`object.convert(target='MESH')`), *Remesh* ou limpar antes do Boolean com o corpo. Alternativa mais confiável: usar a ferramenta Text do próprio Bambu Studio.

## 3. Orgânico / sculpt → impressão
- Dyntopo gera lascas non-manifold e auto-interseções: finalize sempre com **Voxel Remesh** (`Ctrl+R`, voxel 0,2–0,5 mm na cena em mm; produz malha manifold; ignora modifiers, aplique antes).
- Polycount: slicer engasga acima de ~1–2 M triângulos (MakerWorld alerta > 1 M). Alvo 200 k–1 M. **Decimate** *Collapse* (Ratio) ou *Planar* (Angle Limit) — ou "Simplify model" no Bambu Studio.
- Oco (economizar filamento): Solidify Complex, Offset −1, parede 1,2–2 mm; ou Toolbox → *Hollow* (OpenVDB). Furos de dreno Ø 3–4 mm. Para FDM, geralmente é melhor deixar sólido e usar infill baixo — só oque quando a peça é muito grande.
- Remesh modifier em modo Voxel exige espessura: coloque Solidify antes.

## 4. Regras de design FDM (bico 0,4 mm, linha 0,45 mm)
- **Paredes**: múltiplos da linha — 0,45 / 0,9 / 1,35 / 1,8 mm. Nada < 0,45 imprime; evite 0,45–0,9 (uma parede só). Mínimo prático **0,9 mm**; funcional 1,35–1,8 mm. Pinos/features ≥ 1,8 mm (4× linha); furos ≥ Ø 2 mm.
- **Overhang**: ≤ 45° sem suporte; 45–60° só com cooling bom (PLA); > 60° exige suporte → redesenhe. **Pontes** < 10–20 mm.
- **Furos horizontais**: gota (teardrop 90°) se < Ø 4 mm; maiores com teto plano 0,4 mm acima do círculo. Furos verticais saem menores: compensar +0,1 (PLA) a +0,2 mm (PETG/ABS), ou usar *hole compensation* no slicer.
- **Ajustes**: press-fit −0,1…−0,15 mm; deslizante +0,1; folga +0,2–0,3; dobradiças ≥ 0,3; print-in-place 0,3–0,5 mm. Precisão da máquina ±0,1–0,2 mm.
- **Arestas na mesa**: chanfro 45° de ~0,3–0,5 mm (esconde elephant foot); fillet virado para baixo vira overhang íngreme. Fillets só em arestas verticais.
- **Texto** em relevo ≥ 0,9 mm largo; gravado ≥ 0,6 mm traço, 0,5 mm fundo.
- **Snap-fit**: viga 1,5–2,5 mm, deflexão 2–5 % do comprimento, lead-in 30–45°. Living hinge 0,8–1 mm em TPU/PETG (PLA quebra).
- **Orientação**: camadas são o ponto fraco (~3× menos resistência em Z). Carga no plano XY; base plana grande; face bonita na lateral ou na PEI texturizada; minimize área suportada. Peça alta e estreita → prever brim.
- **Contração** (ajustar no perfil do filamento ou no modelo): ABS/ASA ~0,5–1 %, PLA ~0,2–0,4 %, Nylon/PP 1–2 %.
- Resistência vem de **paredes**, não de infill — desenhe pensando em 3–4 walls.

## 5. Higiene de malha (conceitos)
- **Manifold** = toda aresta pertence a exatamente 2 faces, sem faces internas, sem sobreposição. Encontrar: Edit Mode → `Select → Select All by Trait → Non Manifold` (Wire, Boundaries, Multiple Faces, Non Contiguous). Também `Interior Faces`, `Loose Geometry`.
- **Join ≠ Union**: `Ctrl+J` mantém cascas sobrepostas e faces internas → slicer alterna dentro/fora, infill falta, Bambu acusa "redundant paths". Use Boolean Union (Exact) ou o Mesh Boolean do Studio.
- **Normais**: overlay Face Orientation azul fora / vermelho dentro. `Shift+N` (Recalculate Outside). Volume negativo no script = normais invertidas.
- **Limpeza padrão** (Edit Mode, tudo selecionado): Merge by Distance 0,001–0,01 mm → Delete Loose → Degenerate Dissolve → Fill Holes → Recalculate Outside. N-gons: `Ctrl+T` triangular antes de STL (o exportador triangula, mas n-gons côncavos podem sair errados).
- Cascas: `Mesh → Separate → By Loose Parts` para descobrir quantas há; cada cor/material = 1 casca fechada.

## 6. Script de verificação obrigatório (rodar via execute_blender_code)
```python
import bpy, bmesh, math
obj = bpy.context.active_object; assert obj and obj.type == 'MESH'
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); bpy.context.view_layer.objects.active = obj
for m in list(obj.modifiers): bpy.ops.object.modifier_apply(modifier=m.name)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.001)
bpy.ops.mesh.delete_loose()
bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.mesh.select_interior_faces(); bpy.ops.mesh.delete(type='FACE')
bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.dissolve_degenerate(threshold=0.0001)
bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')
bm = bmesh.new(); bm.from_mesh(obj.data)
nm_e = [e for e in bm.edges if not e.is_manifold]; nm_v = [v for v in bm.verts if not v.is_manifold]
vol = bm.calc_volume(signed=True); tris = sum(len(f.verts) - 2 for f in bm.faces); bm.free()
d = obj.dimensions
report = dict(nonmanifold_edges=len(nm_e), nonmanifold_verts=len(nm_v), volume_mm3=round(vol,1), triangles=tris,
              dims_mm=(round(d.x,2), round(d.y,2), round(d.z,2)), scale=tuple(round(s,3) for s in obj.scale))
print(report)
```
Depois, com o Toolbox ativo:
```python
prefs = bpy.context.preferences.addons["bl_ext.blender_org.print3d_toolbox"].preferences
prefs.thickness_min = 0.9; prefs.angle_overhang = math.radians(45); prefs.angle_sharp = math.radians(160)
bpy.ops.mesh.print3d_clean_non_manifold(threshold=0.001, sides=0)
bpy.ops.mesh.print3d_check_all()   # solid, intersect, shells, degenerate, nonplanar, thick, sharp, overhang
bpy.ops.mesh.print3d_info_volume()
```
**Critérios de aprovação** (todos): 0 arestas/vértices non-manifold · volume > 0 · 1 shell por objeto (ou Union antes) · nenhuma face < 0,9 mm em check_thick · triângulos < 1 M · dims dentro do volume da H2C · scale = (1,1,1) · overhangs > 45° listados e cada um justificado (suporte planejado ou redesenho). Se reprovar: corrija, rode de novo, só então exporte. Reporte o dicionário ao usuário.

## 7. Multi-cor / multi-material
- Um objeto **por cor**, cada um manifold fechado, **origem comum** (`origin_set` para o mesmo ponto) e faces em contato exato — sem sobreposição e sem coplanar-parcial; se precisar, sobreponha 0,01 mm e deixe o slicer unir.
- Export A (recomendado): 3MF via `bpy.ops.export_mesh.threemf(filepath=..., use_selection=True, global_scale=1.0)` — materiais viram slots de filamento; abre no Bambu Studio como um objeto com partes.
- Export B: um STL por cor com o mesmo origin; no Studio, importar todos → responder **"Yes"** em "Load these files as a single object with multiple parts?" → atribuir filamento por parte (teclas 1–9).
- Se o Studio achatar Z no 3MF (bug conhecido), use OBJ com *Colors* + *Triangulated Mesh* ou os STLs separados.

## 8. Export e conferência
```python
bpy.ops.wm.stl_export(filepath="/caminho/peca.stl", export_selected_objects=True, apply_modifiers=True,
                      global_scale=1.0, use_scene_unit=False, forward_axis='Y', up_axis='Z', ascii_format=False)
```
- Cena em mm (scale_length 0,001) → `global_scale=1.0`, `use_scene_unit=False`. Cena em metros → `global_scale=1000`. Nunca os dois. Binário sempre (menor, mais rápido).
- OBJ: `bpy.ops.wm.obj_export(filepath, export_selected_objects=True, apply_modifiers=True, forward_axis='Y', up_axis='Z', export_triangulated_mesh=True, export_materials=False)`.
- Conferir: reimportar o STL numa cena vazia e comparar `dimensions` com o relatório, ou abrir no Bambu Studio e ler a caixa de tamanho. Se der 1000× → unidades.
- Um arquivo por peça; nomes descritivos (`suporte_v3_PLA.stl`). Se a peça precisa de orientação específica, deixe o Z-up correto no Blender — o Studio importa como está.

## 9. Erros comuns: sintoma no slicer → causa → correção
- Modelo minúsculo/gigante → unidades ou escala não aplicada → scale_length 0,001, scene unit off, `Ctrl+A` Scale.
- Paredes faltando / "inside-out" → normais invertidas → Face Orientation, `Shift+N`, volume > 0.
- Camadas vazias, buracos, Studio pede "Fix model" → non-manifold/aberto → Select by Trait, Fill Holes, `print3d_clean_non_manifold`.
- Peça sólida onde devia ser oca / infill estranho → faces interiores ou cascas unidas por Join → Delete Interior Faces, Boolean Union.
- Fatiamento lento ou trava → > 1–2 M triângulos → Decimate/Remesh/Simplify.
- Casca fina some no preview → parede < 0,45 mm → Solidify ≥ 0,9 mm ou Arachne no slicer.
- Furo sai apertado → contração + seam → +0,1–0,2 mm ou hole compensation; gota em furos horizontais.
- Resultado do modifier não aparece → não aplicado → `apply_modifiers=True` ou aplicar antes.
- Partes multi-cor se sobrepõem no Studio → origens diferentes ou faces sobrepostas → origem comum, contato exato.

## Referências
- Unidades/STL: https://projects.blender.org/blender/blender/issues/71704 · https://www.katsbits.com/codex/3d-printing-units/
- Boolean: https://docs.blender.org/manual/en/4.2/modeling/modifiers/generate/booleans.html · Solidify: https://docs.blender.org/manual/en/4.2/modeling/modifiers/generate/solidify.html · Bevel: https://docs.blender.org/manual/en/4.2/modeling/modifiers/generate/bevel.html · Screw: https://docs.blender.org/manual/en/4.2/modeling/modifiers/generate/screw.html · Remesh: https://docs.blender.org/manual/en/4.2/sculpt_paint/sculpting/tool_settings/remesh.html
- Seleção/limpeza: https://docs.blender.org/manual/en/4.2/modeling/meshes/selecting/all_by_trait.html · https://docs.blender.org/manual/en/4.2/modeling/meshes/editing/mesh/cleanup.html · STL: https://docs.blender.org/manual/en/4.2/files/import_export/stl.html
- 3D Print Toolbox: https://extensions.blender.org/add-ons/print3d-toolbox/ · 3MF: https://extensions.blender.org/add-ons/threemf-io/ · Bool Tool: https://extensions.blender.org/add-ons/bool-tool/ · PDT: https://extensions.blender.org/add-ons/precision-drawing-tools-pdt/ · CAD Sketcher: https://hlorus.github.io/CAD_Sketcher/
- Regras FDM: https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135 · https://blog.rahix.de/design-for-3d-printing/ · https://www.hydraresearch3d.com/design-rules · Contração (Bambu): https://wiki.bambulab.com/en/knowledge-sharing/3d-prints-shrinkage · Snap-fit: https://help.makelab.com/help/article/snap-fit-and-living-hinge-design-for-3d-printing
- Multi-cor no Studio: https://wiki.bambulab.com/en/software/bambu-studio/split-to-objects-parts · https://wiki.bambulab.com/en/software/bambu-studio/multi-color-printing
