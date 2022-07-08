from pytest import fixture
from paddl.langs.mysql import create_definition
from paddl import Column


class TestColumnDefinitions:
    @fixture
    def create_def(self):
        return """
          (
          `id` char(32) NOT NULL,
          `overdraft_id` char(32) NOT NULL,
          `amount` decimal(8,2) NOT NULL,
          `reason` text NOT NULL,
          `adjustment_source_id` int(11) NOT NULL DEFAULT '1',
          `created` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
          CONSTRAINT `adjustment_adjustment_source_id_foreign` FOREIGN KEY (`adjustment_source_id`) REFERENCES `adjustment_source` (`id`),
          CONSTRAINT `adjustment_overdraft_id_foreign` FOREIGN KEY (`overdraft_id`) REFERENCES `overdraft` (`id`)
          )
        """

    def test_col_defs(self, create_def):
        result = create_definition.parseString(create_def)
        assert result[0][0] == 'id'
        assert result[6][0] == 'CONSTRAINT'
