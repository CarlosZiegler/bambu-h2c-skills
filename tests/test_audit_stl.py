import hashlib
from contextlib import redirect_stderr
import importlib.util
import io
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/fdm-print-preflight/scripts/audit_stl.py'
spec = importlib.util.spec_from_file_location('audit_stl', SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def voxel_surface(cells):
    """Closed, consistently oriented fixtures, with internal faces removed."""
    quads = [
        ((-1, 0, 0), ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0))),
        ((1, 0, 0), ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1))),
        ((0, -1, 0), ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1))),
        ((0, 1, 0), ((0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0))),
        ((0, 0, -1), ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0))),
        ((0, 0, 1), ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1))),
    ]
    triangles = []
    for cell in sorted(cells):
        for normal, corners in quads:
            if tuple(a + b for a, b in zip(cell, normal)) not in cells:
                p = [tuple(a + b for a, b in zip(cell, corner)) for corner in corners]
                triangles.extend(((p[0], p[1], p[2]), (p[0], p[2], p[3])))
    return triangles


def transform(triangles, scale=(1, 1, 1), offset=(0, 0, 0)):
    return [tuple(tuple(v*s + o for v, s, o in zip(p, scale, offset)) for p in t) for t in triangles]


def feet_base():
    cells = {(x, y, 2) for x in range(6) for y in range(4)}
    cells.update((x, y, z) for x in (0, 5) for y in (0, 3) for z in range(2))
    return voxel_surface(cells)


def write_binary(path, triangles, header=b'STL fixture'):
    data = header.ljust(80, b' ')[:80] + struct.pack('<I', len(triangles))
    for t in triangles:
        data += struct.pack('<12fH', 0, 0, 0, *(v for p in t for v in p), 0)
    path.write_bytes(data)


class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.cube = voxel_surface({(0, 0, 0)})

    def test_flat_cube_screen_is_not_print_approval(self):
        r = audit.audit_triangles(self.cube)
        self.assertEqual(r['status'], 'screen_pass')
        self.assertAlmostEqual(r['planar_bed_contact_area_mm2'], 1)
        self.assertAlmostEqual(r['shells'][0]['signed_volume_mm3'], 1)
        self.assertEqual(r['slice_review'], 'required')
        self.assertEqual(r['physical_print'], 'not_verified')

    def test_closed_base_on_feet_requires_review_at_two_mm(self):
        r = audit.audit_triangles(feet_base())
        self.assertEqual(r['nonmanifold_edges'], 0)
        self.assertEqual(len(r['shells']), 1)
        self.assertEqual(r['bounds_mm']['min'][2], 0)
        self.assertAlmostEqual(r['planar_bed_contact_area_mm2'], 4)
        self.assertEqual(r['status'], 'review_required')
        underside = r['horizontal_undersides_above_bed'][0]
        self.assertAlmostEqual(underside['z_min_mm'], 2)
        self.assertAlmostEqual(underside['area_mm2'], 20)

    def test_quarter_mm_recess_is_not_missed(self):
        r = audit.audit_triangles(transform(feet_base(), scale=(1, 1, 0.125)))
        self.assertEqual(r['status'], 'review_required')
        self.assertAlmostEqual(r['horizontal_undersides_above_bed'][0]['z_min_mm'], 0.25)

    def test_high_overhang_still_requires_review(self):
        r = audit.audit_triangles(transform(feet_base(), scale=(1, 1, 30)))
        self.assertAlmostEqual(r['horizontal_undersides_above_bed'][0]['z_min_mm'], 60)
        self.assertEqual(r['status'], 'review_required')

    def test_open_mesh_blocks(self):
        self.assertEqual(audit.audit_triangles(self.cube[:-1])['status'], 'blocked')

    def test_inverted_shell_blocks_even_if_total_volume_positive(self):
        small = transform(self.cube, scale=(0.1, 0.1, 0.1), offset=(3, 0, 0))
        r = audit.audit_triangles(self.cube + [tuple(reversed(t)) for t in small])
        self.assertGreater(sum(s['signed_volume_mm3'] for s in r['shells']), 0)
        self.assertIn('nonpositive_shell_volume', r['blocking_findings'])

    def test_disconnected_floating_shell_is_reported(self):
        r = audit.audit_triangles(self.cube + transform(self.cube, offset=(3, 0, 4)))
        self.assertEqual(len(r['shells']), 2)
        self.assertIn('multiple_shells_check_each', r['review_findings'])
        self.assertEqual(r['status'], 'review_required')

    def test_duplicate_and_degenerate_faces_block(self):
        for extra in [self.cube[0], ((0, 0, 0),) * 3]:
            with self.subTest(extra=extra):
                self.assertEqual(audit.audit_triangles(self.cube + [extra])['status'], 'blocked')

    def test_enclosed_void_is_reviewed_not_declared_invalid(self):
        cells = {(x, y, z) for x in range(3) for y in range(3) for z in range(3)}
        cells.remove((1, 1, 1))
        r = audit.audit_triangles(voxel_surface(cells))
        self.assertEqual(r['nonmanifold_edges'], 0)
        self.assertEqual(r['inconsistent_winding_edges'], 0)
        self.assertEqual(sorted(s['signed_volume_mm3'] for s in r['shells']), [-1, 27])
        self.assertEqual(r['status'], 'review_required')
        self.assertIn('negative_shell_verify_cavity_or_winding', r['review_findings'])
        self.assertIn('exact_shell_nesting', r['not_checked'])

    def test_wholly_inverted_object_is_blocked(self):
        r = audit.audit_triangles([tuple(reversed(t)) for t in self.cube])
        self.assertEqual(r['status'], 'blocked')
        self.assertIn('nonpositive_shell_volume', r['blocking_findings'])

    def test_above_and_below_bed(self):
        high = audit.audit_triangles(transform(self.cube, offset=(0, 0, 0.25)))
        low = audit.audit_triangles(transform(self.cube, offset=(0, 0, -0.25)))
        self.assertIn('whole_object_above_bed', high['review_findings'])
        self.assertIn('geometry_below_bed', low['blocking_findings'])

    def test_explicit_units_and_bed_reference(self):
        m = transform(self.cube, scale=(0.001,)*3, offset=(0, 0, 0.002))
        r = audit.audit_triangles(m, unit_scale=1000, bed_z=2)
        self.assertEqual(r['status'], 'screen_pass')
        self.assertEqual(r['dimensions_mm'], [1, 1, 1])

    def test_point_contact_does_not_pass(self):
        # Tetrahedron supported only at the origin; orient faces outward.
        verts = [(0, 0, 0), (-1, -1, 2), (1, -1, 2), (0, 1, 2)]
        triangles = [tuple(verts[i] for i in face) for face in [(0, 2, 1), (0, 1, 3), (0, 3, 2), (1, 2, 3)]]
        r = audit.audit_triangles(triangles)
        self.assertEqual(r['planar_bed_contact_area_mm2'], 0)
        self.assertNotEqual(r['status'], 'screen_pass')

    def test_nonfinite_data_and_invalid_parameters_rejected(self):
        for kwargs in [dict(unit_scale=0), dict(unit_scale=float('inf')), dict(z_tolerance=0), dict(bed_z=float('nan'))]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                audit.audit_triangles(self.cube, **kwargs)
        with self.assertRaises(ValueError):
            audit.audit_triangles([((float('nan'), 0, 0), (1, 0, 0), (1, 1, 0))])


class FileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.cube = voxel_surface({(0, 0, 0)})

    def test_binary_header_solid_still_binary_and_unchanged(self):
        path = self.folder / 'cube.stl'
        write_binary(path, self.cube, b'solid binary')
        before = path.read_bytes()
        triangles, digest = audit.read_stl(path)
        self.assertEqual(triangles, self.cube)
        self.assertEqual(digest, hashlib.sha256(before).hexdigest())
        self.assertEqual(path.read_bytes(), before)

    def test_ascii_and_malformed_input(self):
        path = self.folder / 'cube.stl'
        text = 'solid cube\n'
        for tri in self.cube:
            text += 'facet normal 0 0 0\nouter loop\n'
            text += ''.join('vertex %s %s %s\n' % p for p in tri)
            text += 'endloop\nendfacet\n'
        path.write_text(text + 'endsolid cube\n')
        self.assertEqual(audit.read_stl(path)[0], self.cube)
        for broken in [text, text.replace('endloop', 'bad'), 'solid\nvertex 1 2 3\nendsolid\n']:
            path.write_text(broken)
            with self.subTest(broken=broken[:20]), self.assertRaises(ValueError):
                audit.read_stl(path)

    def test_binary_truncation_rejected(self):
        path = self.folder / 'cube.stl'
        write_binary(path, self.cube)
        path.write_bytes(path.read_bytes()[:-1])
        with self.assertRaises(ValueError):
            audit.read_stl(path)

    def test_cli_all_parts_exit_codes_and_no_mutation(self):
        good, bad = self.folder / 'cube.stl', self.folder / 'base.stl'
        out = self.folder / 'report.json'
        write_binary(good, self.cube)
        write_binary(bad, feet_base())
        originals = [p.read_bytes() for p in (good, bad)]
        r = subprocess.run([sys.executable, str(SCRIPT), str(good), str(bad), '--output', str(out)], capture_output=True)
        self.assertEqual(r.returncode, 2, r.stderr)
        reports = json.loads(out.read_text())['files']
        self.assertEqual([r['status'] for r in reports], ['screen_pass', 'review_required'])
        self.assertEqual([p.read_bytes() for p in (good, bad)], originals)
        r = subprocess.run([sys.executable, str(SCRIPT), str(good)], capture_output=True)
        self.assertEqual(r.returncode, 0)
        r = subprocess.run([sys.executable, str(SCRIPT), str(good), str(self.folder / 'missing.stl')], capture_output=True)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(len(json.loads(r.stdout)['files']), 2)

    def test_output_cannot_overwrite_input_or_hardlink(self):
        path, alias = self.folder / 'cube.stl', self.folder / 'alias.json'
        write_binary(path, self.cube)
        alias.hardlink_to(path)
        before = path.read_bytes()
        for dest in [path, alias]:
            r = subprocess.run([sys.executable, str(SCRIPT), str(path), '--output', str(dest)], capture_output=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertEqual(path.read_bytes(), before)

    def test_extreme_coordinates_do_not_discard_other_file_reports(self):
        good, extreme = self.folder / 'cube.stl', self.folder / 'extreme.stl'
        write_binary(good, self.cube)
        for scale in (1e104, 1e200):
            text = 'solid extreme\n'
            for tri in transform(self.cube, scale=(scale,) * 3):
                text += 'facet normal 0 0 0\nouter loop\n'
                text += ''.join('vertex %s %s %s\n' % p for p in tri)
                text += 'endloop\nendfacet\n'
            extreme.write_text(text + 'endsolid extreme\n')
            before = extreme.read_bytes()
            with self.subTest(scale=scale):
                r = subprocess.run([sys.executable, str(SCRIPT), str(extreme), str(good)], capture_output=True)
                self.assertEqual(r.returncode, 1)
                self.assertEqual(r.stderr, b'')
                reports = json.loads(r.stdout)['files']
                self.assertEqual([p['status'] for p in reports], ['input_error', 'screen_pass'])
                self.assertEqual(extreme.read_bytes(), before)

    def test_report_path_replaced_by_symlink_during_audit_preserves_input(self):
        source, out = self.folder / 'cube.stl', self.folder / 'report.json'
        write_binary(source, self.cube)
        before = source.read_bytes()
        original_reader = audit.read_stl

        def swap_output(path):
            result = original_reader(path)
            out.symlink_to(source)
            return result

        with patch.object(audit, 'read_stl', side_effect=swap_output):
            self.assertEqual(audit.main([str(source), '--output', str(out)]), 0)
        self.assertEqual(source.read_bytes(), before)
        self.assertFalse(out.is_symlink())
        self.assertEqual(json.loads(out.read_text())['files'][0]['status'], 'screen_pass')

    def test_failed_report_replacement_keeps_previous_report_and_cleans_temp(self):
        source, out = self.folder / 'cube.stl', self.folder / 'report.json'
        write_binary(source, self.cube)
        before = source.read_bytes()
        out.write_text('previous report')
        entries = set(self.folder.iterdir())
        with patch('os.replace', side_effect=OSError('replacement failed')), redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(audit.main([str(source), '--output', str(out)]), 1)
        self.assertIn('Cannot write report', errors.getvalue())
        self.assertEqual(out.read_text(), 'previous report')
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(set(self.folder.iterdir()), entries)


if __name__ == '__main__':
    unittest.main()
