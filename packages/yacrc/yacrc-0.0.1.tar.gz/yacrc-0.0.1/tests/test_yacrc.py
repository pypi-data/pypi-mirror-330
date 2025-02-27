import unittest

from yacrc import CRC


class TestYACRC(unittest.TestCase):

    def test_catalog(self):
        """Compares built-in CRC model catalog to Greg Cook's catalog.

        The Greg Cook's catalog is downloaded from:

            https://reveng.sourceforge.io/crc-catalogue/all1.htm
        """

        try:
            from .catalog import get
            from requests import HTTPError
        except ModuleNotFoundError:
            self.skipTest('Catalog test requires requests module')

        try:
            catalog = get()
        except (ValueError, HTTPError) as e:
            self.fail(e)

        for model in CRC.catalog():

            p = model.parameters

            self.assertTrue(
                model.optimize,
                f'Expected optimized CRC model: {model}'
            )

            # These fields do not exist in the catalog
            del p['data']
            del p['reverse']
            del p['optimize']

            if model.name not in catalog:
                self.fail(f'Greg Cook\'s catalog does not have {model}')

            c = catalog[model.name]
            del catalog[model.name]

            self.assertEqual(
                p, c,
                f'CRC model parameters mismatch:\n{p}\n{c}'
            )

        remaining = '\n'.join([str(p) for p in catalog.values()])

        self.assertFalse(
            remaining,
            f'Missing CRC models in the built-in catalog:\n{remaining}'
        )

    def test_check_and_residue(self):
        """Validates check and residue parameters for each CRC model.

        These parameters are checked when the CRC model is created.
        However, for CRC models from the catalog, the validation is
        not performed to speed up loading the module.
        """

        for model in CRC.catalog():
            try:
                model._validate()
            except ValueError as e:
                self.fail(e)

    def test_verify(self):
        """TODO
        """

        for model in CRC.catalog():

            buffer = b'123456789'
            appended = model.append(buffer)

            self.assertTrue(
                model.verify(appended)
            )

    def test_optimized(self):
        """Tests optimized CRC calculation algorithm.
        """

        for model in CRC.catalog():

            self.assertTrue(model.optimize)

            buffer = b'123456789'

            crc_1 = model.crc(buffer)

            model.optimization(False)

            self.assertFalse(model.optimize)

            crc_2 = model.crc(buffer)

            self.assertEqual(crc_1, crc_2)

    def test_single_bit(self):
        """Tests single bit buffer.
        """

        for model in CRC.catalog():

            obj = model(data=1)

            appended = obj.append('1')

            self.assertTrue(obj.verify(appended))


if __name__ == '__main__':
    unittest.main()
