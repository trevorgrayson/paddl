from paddl import parse
from paddl.langs.mysql import DECIMAL
DDL = """
CREATE TABLE `starburst` (
  `id` char(32) NOT NULL,
  `backdraft_id` char(32) NOT NULL,
  `amount` decimal(13,2) NOT NULL,
  `starburst_status_id` int(11) NOT NULL,
  `created` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `updated` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `deleted` datetime(3) DEFAULT NULL,
  `starburst_method_loomis_id` varchar(50) NOT NULL,
  `starburst_method_type_id` int(11) NOT NULL DEFAULT '3',
  `express_fee` decimal(13,2) NOT NULL DEFAULT '0.00',
  `total_disbursed_amount` decimal(13,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `starburst_backdraft_id_index` (`backdraft_id`),
  KEY `starburst_starburst_status_id_foreign` (`starburst_status_id`),
  KEY `starburst_starburst_method_type_id_foreign` (`starburst_method_type_id`),
  CONSTRAINT `starburst_starburst_method_type_id_foreign` FOREIGN KEY (`starburst_method_type_id`) REFERENCES `starburst_method_type` (`id`),
  CONSTRAINT `starburst_starburst_status_id_foreign` FOREIGN KEY (`starburst_status_id`) REFERENCES `starburst_status` (`id`),
  CONSTRAINT `starburst_backdraft_id_foreign` FOREIGN KEY (`backdraft_id`) REFERENCES `backdraft` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

DECIMAL_COL = """`amount` decimal(8,2) NOT NULL"""
DECIMAL_DEF = """decimal(8,2)"""


class TestDefaultValues:

    def test_decimal(self):
        result = DECIMAL.parseString(DECIMAL_DEF)
        assert result[0] == 'DECIMAL'
        assert result[1] == '8'
        assert result[2] == '2'

    def test_defaults(self):
        result = parse(DDL)

