class TestDatabaseHandlers:
    """
    Mix-in class, to be used in a subclass that also inherits ReferenceTestCase
    """
    def test_connection(self):
        elements = self.dbh.resolve_table('elements')
        self.assertTrue(self.dbh.check_table_exists(elements))
        self.assertFalse(self.dbh.check_table_exists('does_not_exist'))

    def test_handler_simple_ops(self):
        elements = self.dbh.resolve_table('elements')
        names = self.dbh.get_database_column_names(elements)
        if '_rowindex' in names:
            names.remove('_rowindex')  # hidden field, ignore it
        self.assertEqual(names,
                         ['Z', 'Name', 'Symbol', 'Period', 'Group',
                          'ChemicalSeries', 'AtomicWeight', 'Etymology',
                          'RelativeAtomicMass', 'MeltingPointC',
                          'MeltingPointKelvin', 'BoilingPointC',
                          'BoilingPointF', 'Density', 'Description', 'Colour'])
        self.assertEqual(self.dbh.get_database_column_type(elements, 'Z'),
                         'int')
        self.assertEqual(self.dbh.get_database_column_type(elements, 'Name'),
                         'string')
        self.assertEqual(self.dbh.get_database_column_type(elements,
                                                           'Density'),
                         'real')
        self.assertEqual(self.dbh.get_database_nrows(elements), 118)
        self.assertEqual(self.dbh.get_database_nnull(elements, 'Colour'), 85)
        self.assertEqual(self.dbh.get_database_nnonnull(elements, 'Colour'),
                         33)

    def test_handler_unique_values(self):
        elements = self.dbh.resolve_table('elements')
        self.assertEqual(self.dbh.get_database_unique_values(elements,
                                                             'ChemicalSeries'),
                         ['Actinoid', 'Alkali metal', 'Alkaline earth metal',
                          'Halogen', 'Lanthanoid', 'Metalloid', 'Noble gas',
                          'Nonmetal', 'Poor metal', 'Transition metal'])


