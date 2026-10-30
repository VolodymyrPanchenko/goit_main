from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def load_csv(spark, path):
    """Завдання 1: завантаження CSV як окремого DataFrame"""
    return spark.read.csv(path, header=True, inferSchema=True)


def clean_data(df, name="DataFrame"):
    """Завдання 2: видалення рядків з пропущеними значеннями"""
    before = df.count()
    cleaned = df.dropna()
    after = cleaned.count()
    print(f"\nОчищення {name}:")
    print(f"  Було рядків: {before}")
    print(f"  Залишилось:  {after}")
    print(f"  Видалено:    {before - after}")
    return cleaned


def main():
    spark = (
        SparkSession.builder
        .appName("PurchaseAnalysis")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    try:
        # ---------- Завдання 1: завантаження ----------
        users_df = load_csv(spark, "./data/users.csv")
        purchases_df = load_csv(spark, "./data/purchases.csv")
        products_df = load_csv(spark, "./data/products.csv")

        print("=== Завдання 1: DataFrame після завантаження ===")
        print("users:")
        users_df.show(5, truncate=False)
        print("purchases:")
        purchases_df.show(5, truncate=False)
        print("products:")
        products_df.show(5, truncate=False)

        # ---------- Завдання 2: очищення ----------
        users_df = clean_data(users_df, "users")
        purchases_df = clean_data(purchases_df, "purchases")
        products_df = clean_data(products_df, "products")

        print("\n=== Завдання 2: DataFrame після очищення ===")
        users_df.show(5, truncate=False)
        purchases_df.show(5, truncate=False)
        products_df.show(5, truncate=False)

        # Спільний join для подальших розрахунків
        joined = (
            purchases_df
            .join(users_df, on="user_id", how="inner")
            .join(products_df, on="product_id", how="inner")
            .withColumn("total_price", F.col("quantity") * F.col("price"))
        )

        # ---------- Завдання 3: загальна сума покупок за категоріями (усі користувачі) ----------
        category_total_all = (
            joined
            .groupBy("category")
            .agg(F.round(F.sum("total_price"), 2).alias("total_sum"))
            .orderBy(F.desc("total_sum"))
        )

        print("\n=== Завдання 3: Загальна сума покупок за кожною категорією ===")
        category_total_all.show(truncate=False)

        # ---------- Завдання 4: сума покупок за категоріями для віку 18–25 ----------
        age_filtered = joined.filter(F.col("age").between(18, 25))

        category_total_18_25 = (
            age_filtered
            .groupBy("category")
            .agg(F.round(F.sum("total_price"), 2).alias("total_sum"))
            .orderBy(F.desc("total_sum"))
        )

        print("\n=== Завдання 4: Сума покупок за категоріями (вік 18–25) ===")
        category_total_18_25.show(truncate=False)

        # ---------- Завдання 5: частка (%) кожної категорії від загальних витрат 18–25 ----------
        # Один раз рахуємо загальну суму і використовуємо lit (без Window-попереджень)
        grand_total = category_total_18_25.agg(F.sum("total_sum")).collect()[0][0]

        category_share_18_25 = (
            category_total_18_25
            .withColumn(
                "percentage",
                F.round(F.col("total_sum") / F.lit(grand_total) * 100, 2)
            )
            .orderBy(F.desc("percentage"))
        )

        print("\n=== Завдання 5: Частка (%) витрат за категоріями (вік 18–25) ===")
        category_share_18_25.show(truncate=False)

        # ---------- Завдання 6: топ-3 категорії з найвищим відсотком ----------
        top3 = category_share_18_25.limit(3)

        print("\n=== Завдання 6: Топ-3 категорії з найвищим % витрат (вік 18–25) ===")
        top3.show(truncate=False)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
