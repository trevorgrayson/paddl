CREATE TABLE `adjustment` (
  `id` char(32) NOT NULL,
  `overdraft_id` char(32) NOT NULL,
  `amount` decimal(8,2) NOT NULL,
  `reason` text NOT NULL,
  `adjustment_source_id` int(11) NOT NULL DEFAULT '1',
  `created` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT `adjustment_adjustment_source_id_foreign` FOREIGN KEY (`adjustment_source_id`) REFERENCES `adjustment_source` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
