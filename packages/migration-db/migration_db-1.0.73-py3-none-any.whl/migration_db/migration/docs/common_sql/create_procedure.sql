/*
-- 根据_separator拆分字符串，返回pos处的值
DROP FUNCTION IF EXISTS SPLIT_STR;
CREATE FUNCTION SPLIT_STR(
  x VARCHAR(255),
  _separator VARCHAR(12),
  pos INT
)
RETURNS VARCHAR(255)
RETURN REPLACE(SUBSTRING(SUBSTRING_INDEX(x, _separator, pos), LENGTH(SUBSTRING_INDEX(x, _separator, pos - 1)) + 1), _separator, '');

DROP FUNCTION IF EXISTS COUNT_STR_SEPARATOR;
CREATE FUNCTION COUNT_STR_SEPARATOR(
  x VARCHAR(255),
  _separator VARCHAR(12)
)
RETURNS INT
RETURN LENGTH(x) - LENGTH(REPLACE(x, _separator, ""));
*/


DROP PROCEDURE IF EXISTS REPLACE_STR;
DELIMITER //
CREATE PROCEDURE REPLACE_STR(
		IN `table_name` VARCHAR(200),
		IN `field_name` VARCHAR(200),
		IN `pre_value` VARCHAR(20),
		IN `cur_value` VARCHAR(20),
		IN `_separator` VARCHAR(20),
		IN `pos` INT)
BEGIN
    DECLARE cnt INT DEFAULT 0;
    DECLARE i INT DEFAULT 0;
    DECLARE fieldValue VARCHAR(200);
    DECLARE splitFieldValue VARCHAR(200);
    DECLARE countFieldValueSeparator INT;
	SET @queryStmt = CONCAT("SELECT COUNT(1) INTO @cnt FROM ", table_name);
	PREPARE stmt FROM @queryStmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	SET cnt = @cnt;
    WHILE i<= cnt DO
		SET @stmtStr = CONCAT("SELECT ", field_name, " INTO @fieldValue FROM ", table_name, " LIMIT ", i, ",1");
		PREPARE stmt FROM @stmtStr;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
		SET fieldValue = @fieldValue;
--        SET splitFieldValue = SPLIT_STR(fieldValue, _separator, pos);
--        SET countFieldValueSeparator = COUNT_STR_SEPARATOR(fieldValue, _separator);
        SET splitFieldValue = REPLACE(SUBSTRING(SUBSTRING_INDEX(fieldValue, _separator, pos), LENGTH(SUBSTRING_INDEX(fieldValue, _separator, pos - 1)) + 1), _separator, '');
        SET countFieldValueSeparator = LENGTH(fieldValue) - LENGTH(REPLACE(fieldValue, _separator, ""));
		IF splitFieldValue = pre_value THEN
			SET @newFieldValue = CONCAT(SUBSTRING_INDEX(fieldValue, _separator, pos - 1), "-", cur_value, "-", SUBSTRING_INDEX(fieldValue, _separator, -(countFieldValueSeparator + 1 -pos)));
			SET @stmtStr = CONCAT("UPDATE ", table_name, " SET ", field_name, "='", @newFieldValue, "' WHERE ", field_name, "='", fieldValue, "';");
			PREPARE stmt FROM @stmtStr;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		END IF;
        SET i = i + 1;
    END WHILE;
END;
//
DELIMITER ;


DROP PROCEDURE IF EXISTS ReplaceValuesByJson;
DELIMITER //
CREATE PROCEDURE `ReplaceValuesByJson`(
    IN input_str TEXT,
    IN json_mapping JSON,
    IN separator_ CHAR(1),
    OUT result_str TEXT
    )
BEGIN
    -- 计算 input_str 中的逗号数量，并存储在变量中
    DECLARE num_values INT;
    DECLARE temp_result TEXT;
    SET num_values = CHAR_LENGTH(input_str) - CHAR_LENGTH(REPLACE(input_str, separator_, '')) + 1;
    -- 递归生成数字序列的CTE
    WITH RECURSIVE numbers AS (
        SELECT 1 AS n
        UNION ALL
        SELECT n + 1 FROM numbers
        WHERE n <= num_values
    )
    -- 将 JSON 映射转换为表格格式
    , json_mapped_values AS (
        SELECT `key` AS new_value, `val` AS old_value
        FROM JSON_TABLE(json_mapping, '$[*]' COLUMNS(
            `key` VARCHAR(255) PATH "$.new_value",
            `val` INT  PATH "$.old_value"
        )) AS j
    )
    -- 使用递归CTE生成拆分后的结果并执行替换
    SELECT GROUP_CONCAT(COALESCE(mapped_values.new_value, split_values.val) SEPARATOR "_") AS mapped_values INTO temp_result
    FROM (SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(input_str, separator_, numbers.n), separator_, -1) AS val FROM numbers WHERE numbers.n <= num_values) AS split_values
    LEFT JOIN json_mapped_values AS mapped_values ON split_values.val COLLATE utf8mb4_general_ci = mapped_values.old_value COLLATE utf8mb4_general_ci;
    SET result_str = REPLACE(temp_result, '_', separator_);
END;
//
DELIMITER ;


DROP PROCEDURE IF EXISTS REPLACE_STR_BY_MAPPING;
DELIMITER //
CREATE PROCEDURE `REPLACE_STR_BY_MAPPING`(
		IN `table_name` VARCHAR(200),
		IN `field_name` VARCHAR(200),
		IN `_separator` VARCHAR(20),
		IN `json_mapping` JSON,
		IN `primary_key` VARCHAR(200)
		)
BEGIN
    DECLARE cnt INT DEFAULT 0;
    DECLARE i INT DEFAULT 0;
    DECLARE fieldValue text;
    DECLARE newFieldValue text;
    DECLARE primaryKeyValue text;
    DECLARE key_val VARCHAR(255);
    DECLARE key_str VARCHAR(255);
    DECLARE val_str VARCHAR(255);
    DECLARE case_stmt TEXT DEFAULT '';
    DECLARE mappingFieldValue TEXT DEFAULT '{}';
    IF primary_key IS NULL THEN
        SET primary_key = "id";
    END IF;
    -- 查询记录条数
	SET @queryStmt = CONCAT("SELECT COUNT(1) INTO @cnt FROM ", table_name);
	PREPARE stmt FROM @queryStmt;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	SET cnt = @cnt;
	-- 循环修改数据
  	my_loop: WHILE i<= cnt DO
		SET @stmtStr = CONCAT("SELECT ", field_name, ", ", primary_key, " INTO @fieldValue, @primaryKeyValue", " FROM ", table_name, " LIMIT ", i, ",1");
		PREPARE stmt FROM @stmtStr;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
        SET @queryMapping = JSON_UNQUOTE(JSON_EXTRACT(mappingFieldValue, CONCAT('$."', @fieldValue, '"')));
        IF @queryMapping IS NOT NULL THEN
            SET @newFieldValue = @queryMapping;
        ELSE
            CALL ReplaceValuesByJson(@fieldValue, json_mapping, _separator, @newFieldValue);
            SET mappingFieldValue = JSON_SET(mappingFieldValue, CONCAT('$."', @fieldValue, '"'), @newFieldValue);
        END IF;
	    -- 执行修改数据SQL
	    IF @newFieldValue != @fieldValue THEN
            SET @stmtStr = CONCAT("UPDATE ", table_name, " SET ", field_name, "='", @newFieldValue, "' WHERE ", primary_key, "='", @primaryKeyValue, "';");
            PREPARE stmt FROM @stmtStr;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
        END IF;
	    SET i = i + 1;
  	END WHILE;
END;
//
DELIMITER ;