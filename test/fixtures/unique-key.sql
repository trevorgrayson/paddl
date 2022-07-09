CREATE TABLE `account` (
  `id` char(32) NOT NULL,
  `dave_user_id` bigint(20) NOT NULL,
  `extra_cash_account_id` char(32) DEFAULT NULL,
  `status` enum('ACTIVE','PENDING') NOT NULL DEFAULT 'PENDING',
  `created` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `updated` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `deleted` datetime(3) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_dave_user_id_unique` (`dave_user_id`),
  KEY `account_dave_user_id_index` (`dave_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
