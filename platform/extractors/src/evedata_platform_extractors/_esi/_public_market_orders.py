import asyncio
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime

import polars as pl
from aiohttp import ClientSession

from evedata_platform_core import EVEDATA_USER_AGENT

_BASE_URL = "https://esi.evetech.net/markets"
_MARKET_REGION_IDS = [
    10000054,  # Aridia
    10000069,  # Black Rise
    10000055,  # Branch
    10000007,  # Cache
    10000014,  # Catch
    10000051,  # Cloud Ring
    10000053,  # Cobalt Edge
    10000012,  # Curse
    10000035,  # Deklein
    10000060,  # Delve
    10000001,  # Derelik
    10000005,  # Detorid
    10000036,  # Devoid
    10000043,  # Domain
    10000039,  # Esoteria
    10000064,  # Essence
    10000027,  # Etherium Reach
    10000037,  # Everyshore
    10000046,  # Fade
    10000056,  # Feythabolis
    10000058,  # Fountain
    10000029,  # Geminate
    10000067,  # Genesis
    10000011,  # Great Wildlands
    10000030,  # Heimatar
    10000025,  # Immensea
    10000031,  # Impass
    10000009,  # Insmother
    10000052,  # Kador
    10000049,  # Khanid
    10000065,  # Kor-Azor
    10000016,  # Lonetrek
    10000013,  # Malpais
    10000042,  # Metropolis
    10000028,  # Molden Heath
    10000040,  # Oasa
    10000062,  # Omist
    10000021,  # Outer Passage
    10000057,  # Outer Ring
    10000059,  # Paragon Soul
    10000063,  # Period Basis
    10000066,  # Perrigen Falls
    10000048,  # Placid
    10000070,  # Pochven
    10000047,  # Providence
    10000023,  # Pure Blind
    10000050,  # Querious
    10000008,  # Scalding Pass
    10000032,  # Sinq Laison
    10000044,  # Solitude
    10000022,  # Stain
    10000041,  # Syndicate
    10000020,  # Tash-Murkon
    10000045,  # Tenal
    10000061,  # Tenerifis
    10000038,  # The Bleak Lands
    10000033,  # The Citadel
    10000002,  # The Forge
    10000034,  # The Kalevala Expanse
    10000018,  # The Spire
    10000010,  # Tribute
    10000003,  # Vale of the Silent
    10000015,  # Venal
    10000068,  # Verge Vendor
    10000006,  # Wicked Creek
    10001000,  # Yasna Zakh
]
_HUB_STATION_IDS = [
    60003760,  # Jita IV - Moon 4 - Caldari Navy Assembly Plant
    60008494,  # Amarr VIII (Oris) - Emperor Family Academy
    60011866,  # Dodixie IX - Moon 20 - Federation Navy Assembly Plant
    60004588,  # Rens VI - Moon 8 - Brutor Tribe Treasury
    60005686,  # Hek VIII - Moon 12 - Republic Military Assembly Plant
]

_RANGE_ENUM = pl.Enum(
    [
        "station",
        "region",
        "solarsystem",
        "1",
        "2",
        "3",
        "4",
        "5",
        "10",
        "20",
        "30",
        "40",
    ]
)
_SCHEMA = {
    "duration": pl.Int16,
    "is_buy_order": pl.Boolean,
    "issued": pl.Datetime(time_zone="UTC"),
    "location_id": pl.Int64,
    "min_volume": pl.Int64,
    "order_id": pl.Int64,
    "price": pl.Float64,
    "range": pl.String,  # Read as string, will convert to enum later
    "system_id": pl.Int32,
    "type_id": pl.Int32,
    "volume_remain": pl.Int64,
    "volume_total": pl.Int64,
}


async def fetch_dataframe(session: ClientSession, url: str) -> pl.DataFrame:
    async with session.get(url) as resp:
        resp.raise_for_status()
        df = pl.read_json(await resp.read(), schema=_SCHEMA)
        # Convert range column to enum
        return df.with_columns(pl.col("range").cast(_RANGE_ENUM))


async def fetch_region_orders(session: ClientSession, region_id: int) -> pl.LazyFrame:
    first_page: pl.LazyFrame
    last_modified: datetime | None
    total_pages: int
    async with session.get(f"{_BASE_URL}/{region_id}/orders/") as resp:
        resp.raise_for_status()
        first_page_df = pl.read_json(await resp.read(), schema=_SCHEMA)
        # Convert range column to enum
        first_page = first_page_df.with_columns(
            pl.col("range").cast(_RANGE_ENUM)
        ).lazy()

        last_modified = parsedate_to_datetime(resp.headers.get("last-modified"))
        total_pages = int(resp.headers.get("x-pages", "1"))

    if total_pages == 1:
        return first_page.with_columns(
            pl.lit(last_modified).alias("last_modified"),
            pl.lit(region_id).alias("region_id"),
        )

    page_urls = [
        f"{_BASE_URL}/{region_id}/orders/?page={page}"
        for page in range(2, total_pages + 1)
    ]
    tasks = [fetch_dataframe(session, url) for url in page_urls]
    frames = [first_page]
    async for df in asyncio.as_completed(tasks):
        frames.append((await df).lazy())  # noqa: PERF401

    return pl.concat(frames).with_columns(
        pl.lit(last_modified).alias("last_modified"),
        pl.lit(region_id).alias("region_id"),
    )


async def fetch_all_region_orders(session: ClientSession) -> pl.LazyFrame:
    tasks = [
        fetch_region_orders(session, region_id) for region_id in _MARKET_REGION_IDS
    ]
    frames: list[pl.LazyFrame] = []
    for df in asyncio.as_completed(tasks):
        frames.append(await df)  # noqa: PERF401
    return pl.concat(frames).sort(["region_id", "type_id", "order_id"])


def create_market_indicators_aggregation(
    lazy_frame: pl.LazyFrame, group_by_cols: list[str]
) -> pl.LazyFrame:
    """Create market indicators aggregation for given grouping columns."""
    return (
        lazy_frame.group_by(group_by_cols)
        .agg(
            [
                # Core prices
                pl.col("price").filter(pl.col("is_buy_order")).max().alias("buy_price"),
                pl.col("price")
                .filter(~pl.col("is_buy_order"))
                .min()
                .alias("sell_price"),
                # Weighted averages - Buy side
                (
                    (pl.col("price") * pl.col("volume_remain"))
                    .filter(pl.col("is_buy_order"))
                    .sum()
                    / pl.col("volume_remain").filter(pl.col("is_buy_order")).sum()
                ).alias("buy_weighted_avg"),
                # Weighted averages - Sell side
                (
                    (pl.col("price") * pl.col("volume_remain"))
                    .filter(~pl.col("is_buy_order"))
                    .sum()
                    / pl.col("volume_remain").filter(~pl.col("is_buy_order")).sum()
                ).alias("sell_weighted_avg"),
                # Percentiles - Buy side
                pl.col("price")
                .filter(pl.col("is_buy_order"))
                .quantile(0.05)
                .alias("buy_p5"),
                pl.col("price")
                .filter(pl.col("is_buy_order"))
                .quantile(0.50)
                .alias("buy_p50"),
                pl.col("price")
                .filter(pl.col("is_buy_order"))
                .quantile(0.90)
                .alias("buy_p90"),
                pl.col("price")
                .filter(pl.col("is_buy_order"))
                .quantile(0.95)
                .alias("buy_p95"),
                # Percentiles - Sell side
                pl.col("price")
                .filter(~pl.col("is_buy_order"))
                .quantile(0.05)
                .alias("sell_p5"),
                pl.col("price")
                .filter(~pl.col("is_buy_order"))
                .quantile(0.50)
                .alias("sell_p50"),
                pl.col("price")
                .filter(~pl.col("is_buy_order"))
                .quantile(0.90)
                .alias("sell_p90"),
                pl.col("price")
                .filter(~pl.col("is_buy_order"))
                .quantile(0.95)
                .alias("sell_p95"),
                # Volume metrics
                pl.col("volume_remain")
                .filter(pl.col("is_buy_order"))
                .sum()
                .alias("buy_volume"),
                pl.col("volume_remain")
                .filter(~pl.col("is_buy_order"))
                .sum()
                .alias("sell_volume"),
                # Order counts
                pl.col("order_id")
                .filter(pl.col("is_buy_order"))
                .count()
                .alias("buy_orders"),
                pl.col("order_id")
                .filter(~pl.col("is_buy_order"))
                .count()
                .alias("sell_orders"),
                # Timestamp
                pl.col("timestamp").first().alias("timestamp"),
            ]
        )
        .with_columns(
            [
                # Round price fields to 2 decimal places
                pl.col("buy_price").round(2),
                pl.col("sell_price").round(2),
                pl.col("buy_weighted_avg").round(2),
                pl.col("sell_weighted_avg").round(2),
                pl.col("buy_p5").round(2),
                pl.col("buy_p50").round(2),
                pl.col("buy_p90").round(2),
                pl.col("buy_p95").round(2),
                pl.col("sell_p5").round(2),
                pl.col("sell_p50").round(2),
                pl.col("sell_p90").round(2),
                pl.col("sell_p95").round(2),
                # Mid-price (only when both prices exist)
                pl.when(
                    pl.col("buy_price").is_not_null()
                    & pl.col("sell_price").is_not_null()
                )
                .then(((pl.col("buy_price") + pl.col("sell_price")) / 2).round(2))
                .otherwise(None)
                .alias("mid_price"),
                # Micro-price (only when both prices and volumes exist)
                pl.when(
                    pl.col("buy_price").is_not_null()
                    & pl.col("sell_price").is_not_null()
                    & (pl.col("buy_volume") > 0)
                    & (pl.col("sell_volume") > 0)
                )
                .then(
                    (
                        (
                            pl.col("buy_price") * pl.col("sell_volume")
                            + pl.col("sell_price") * pl.col("buy_volume")
                        )
                        / (pl.col("buy_volume") + pl.col("sell_volume"))
                    ).round(2)
                )
                .otherwise(None)
                .alias("micro_price"),
                # Spread absolute (only when both prices exist, must be >= 0)
                pl.when(
                    pl.col("buy_price").is_not_null()
                    & pl.col("sell_price").is_not_null()
                )
                .then(
                    pl.max_horizontal(
                        pl.col("sell_price") - pl.col("buy_price"),
                        pl.lit(0),  # Ensure non-negative
                    ).round(2)
                )
                .otherwise(None)
                .alias("spread_absolute"),
                # Spread percentage (only when both prices exist and mid_price > 0)
                pl.when(
                    pl.col("buy_price").is_not_null()
                    & pl.col("sell_price").is_not_null()
                    & ((pl.col("buy_price") + pl.col("sell_price")) / 2 > 0)
                )
                .then(
                    (
                        pl.max_horizontal(
                            pl.col("sell_price") - pl.col("buy_price"), pl.lit(0)
                        )
                        / ((pl.col("buy_price") + pl.col("sell_price")) / 2)
                        * 100
                    ).round(4)
                )
                .otherwise(None)
                .alias("spread_percentage"),
            ]
        )
    )


if __name__ == "__main__":
    import uvloop
    from rich import print as rprint

    async def main():
        timestamp = datetime.now(UTC)
        # Format timestamp for filenames: YYYYMMDDHHmmss
        timestamp_str = timestamp.strftime("%Y%m%d%H%M%S")

        async with ClientSession(headers={"User-Agent": EVEDATA_USER_AGENT}) as session:
            lazy_orders = (await fetch_all_region_orders(session)).with_columns(
                pl.lit(timestamp).alias("timestamp")
            )

            # Regional aggregation - group by region_id and type_id
            regional_agg = (
                create_market_indicators_aggregation(
                    lazy_orders, ["region_id", "type_id"]
                )
                .rename({"region_id": "location_id"})
                .with_columns(pl.lit("region").alias("location_type"))
            )

            # Hub station aggregation - group by location_id and type_id
            hub_orders = lazy_orders.filter(
                pl.col("location_id").is_in(_HUB_STATION_IDS)
            )
            hub_agg = create_market_indicators_aggregation(
                hub_orders, ["location_id", "type_id"]
            ).with_columns(pl.lit("station").alias("location_type"))

            # Combine regional and hub aggregations
            combined_agg = pl.concat([regional_agg, hub_agg], how="vertical_relaxed")

            # Collect aggregated data and sort
            aggregated = await combined_agg.collect_async()
            aggregated = aggregated.sort(["location_type", "location_id", "type_id"])

            # Write with zstd compression for better compression ratio
            indicators_filename = f"market_indicators_5m_{timestamp_str}.parquet"
            aggregated.write_parquet(
                indicators_filename,
                compression="zstd",
                compression_level=3,  # Good balance of speed and compression
            )

            rprint(f"\nMarket indicators saved to: {indicators_filename}")
            rprint(aggregated.describe())
            rprint(f"Total aggregated rows: {len(aggregated)}")
            regional_count = aggregated.filter(
                pl.col("location_type") == "region"
            ).height
            hub_count = aggregated.filter(pl.col("location_type") == "station").height
            rprint(f"Regional rows: {regional_count}")
            rprint(f"Hub station rows: {hub_count}")

            # Also save raw orders with sorting and compression
            orders = await lazy_orders.collect_async()
            orders = orders.sort(["region_id", "type_id", "order_id"])
            orders_filename = f"market_orders_{timestamp_str}.parquet"
            orders.write_parquet(
                orders_filename,
                compression="zstd",
                compression_level=3,
            )
            rprint(f"\nRaw orders saved to: {orders_filename}")
            rprint(orders.describe())

    uvloop.run(main())
