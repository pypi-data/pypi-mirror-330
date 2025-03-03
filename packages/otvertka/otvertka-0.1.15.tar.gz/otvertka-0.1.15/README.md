# otvertka

![otvertka](./assets/logo.png)

Набор простых функций для работы с данными в ClickHouse.

## Установка

```bash
pip install otvertka
```

## Использование

```python
from otvertka import fetch_data, generate_ab_test_data, get_dates_tuples, get_table_info, handle_outliers

# Получить информацию о таблице
get_table_info('my_table')

# Выполнить SQL запрос
df = fetch_data('SELECT * FROM my_table LIMIT 10')

# Разбить временной интервал на периоды
dates = get_dates_tuples('2024-01-01', '2024-02-01', days_interval=7)

# Сгенерировать тестовые данные для A/B теста
df = generate_ab_test_data(
    groups=['control', 'test'],
    num_observations_per_group=10000,
    effect_size=0.05,
    base_retention_prob=0.3,
    base_impressions_mean=5,
    base_revenue_scale=1.0
)

# Обработать выбросы в данных
df = handle_outliers(
    df,
    target_column='revenue',
    threshold_quantile=0.995,
    handling_method='replace_threshold',
    outlier_type='upper',
    grouping_column='group'
)
```

## Требования

- Python 3.7+
- Необходимые переменные окружения:
  - `CH_USER` - пользователь ClickHouse
  - `CH_PASSWORD` - пароль ClickHouse
  - `CH_HOST` - хост ClickHouse (по умолчанию: localhost)
  - `CH_PORT` - порт ClickHouse (по умолчанию: 8123)

## Лицензия

MIT 