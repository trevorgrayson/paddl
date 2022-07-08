CREATE TABLE `adjustment` (
  `id` char(32) NOT NULL,
  `overdraft_id` char(32) NOT NULL,
  `amount` decimal(8,2) NOT NULL,
  `reason` text NOT NULL,
  `adjustment_source_id` int(11) NOT NULL DEFAULT '1',
  `created` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY `adjustment_overdraft_id_index` (`overdraft_id`),
  KEY `adjustment_adjustment_source_id_foreign` (`adjustment_source_id`),
  CONSTRAINT `adjustment_adjustment_source_id_foreign` FOREIGN KEY (`adjustment_source_id`) REFERENCES `adjustment_source` (`id`),
  CONSTRAINT `adjustment_overdraft_id_foreign` FOREIGN KEY (`overdraft_id`) REFERENCES `overdraft` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
