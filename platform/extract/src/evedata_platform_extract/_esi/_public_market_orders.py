import asyncio
from datetime import (
    UTC,
    datetime,
)
from email.utils import parsedate_to_datetime
from pathlib import Path

import polars as pl
from aiohttp import ClientSession
from rich.console import Console

from evedata_platform_core import EVEDATA_USER_AGENT

_BASE_URL = "https://esi.evetech.net/markets"
MARKET_REGION_IDS = [
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
HUB_STATION_IDS = [
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


async def fetch_region_orders(
    session: ClientSession, region_id: int
) -> tuple[int, pl.LazyFrame]:
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
        return 1, first_page.with_columns(
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

    return total_pages, pl.concat(frames).with_columns(
        pl.lit(last_modified).alias("last_modified"),
        pl.lit(region_id).alias("region_id"),
    )


async def fetch_all_region_orders(session: ClientSession) -> tuple[int, pl.LazyFrame]:
    tasks = [fetch_region_orders(session, region_id) for region_id in MARKET_REGION_IDS]
    frames: list[pl.LazyFrame] = []
    total_pages = 0
    for task in asyncio.as_completed(tasks):
        pages, df = await task
        total_pages += pages
        frames.append(df)
    return total_pages, pl.concat(frames).sort(["region_id", "type_id", "order_id"])


def create_order_depth_aggregation(
    lazy_frame: pl.LazyFrame, group_by_cols: list[str]
) -> pl.LazyFrame:
    """Create full order depth aggregation for given grouping columns.

    This aggregation provides complete order book depth with all price levels
    and their cumulative volumes for full order book reconstruction.
    """
    # First aggregate to get volume and order count per price level
    depth_agg = lazy_frame.group_by([*group_by_cols, "price", "is_buy_order"]).agg(
        [
            pl.col("volume_remain").sum().alias("volume"),
            pl.col("order_id").count().alias("order_count"),
            pl.col("timestamp").first().alias("timestamp"),
        ]
    )

    # Now group by location/type and create the depth arrays
    return (
        depth_agg.group_by(group_by_cols)
        .agg(
            [
                # Full buy side depth - all price levels with volumes
                pl.when(pl.col("is_buy_order"))
                .then(
                    pl.struct(
                        [
                            pl.col("price").round(2),
                            pl.col("volume"),
                            pl.col("order_count"),
                        ]
                    )
                )
                .sort_by("price", descending=True)
                .drop_nulls()
                .alias("buy_depth"),
                # Full sell side depth - all price levels with volumes
                pl.when(~pl.col("is_buy_order"))
                .then(
                    pl.struct(
                        [
                            pl.col("price").round(2),
                            pl.col("volume"),
                            pl.col("order_count"),
                        ]
                    )
                )
                .sort_by("price")
                .drop_nulls()
                .alias("sell_depth"),
                # Summary metrics
                pl.col("volume")
                .filter(pl.col("is_buy_order"))
                .sum()
                .alias("total_buy_volume"),
                pl.col("volume")
                .filter(~pl.col("is_buy_order"))
                .sum()
                .alias("total_sell_volume"),
                pl.col("order_count")
                .filter(pl.col("is_buy_order"))
                .sum()
                .alias("total_buy_orders"),
                pl.col("order_count")
                .filter(~pl.col("is_buy_order"))
                .sum()
                .alias("total_sell_orders"),
                # Best prices
                pl.col("price")
                .filter(pl.col("is_buy_order"))
                .max()
                .round(2)
                .alias("best_buy_price"),
                pl.col("price")
                .filter(~pl.col("is_buy_order"))
                .min()
                .round(2)
                .alias("best_sell_price"),
                # Unique price levels
                pl.col("price")
                .filter(pl.col("is_buy_order"))
                .n_unique()
                .alias("buy_price_levels"),
                pl.col("price")
                .filter(~pl.col("is_buy_order"))
                .n_unique()
                .alias("sell_price_levels"),
                # Timestamp
                pl.col("timestamp").first().alias("timestamp"),
            ]
        )
        .with_columns(
            [
                # Calculate spread
                pl.when(
                    pl.col("best_buy_price").is_not_null()
                    & pl.col("best_sell_price").is_not_null()
                )
                .then(
                    pl.max_horizontal(
                        pl.col("best_sell_price") - pl.col("best_buy_price"),
                        pl.lit(0),
                    ).round(2)
                )
                .otherwise(None)
                .alias("spread"),
                # Mid price
                pl.when(
                    pl.col("best_buy_price").is_not_null()
                    & pl.col("best_sell_price").is_not_null()
                )
                .then(
                    ((pl.col("best_buy_price") + pl.col("best_sell_price")) / 2).round(
                        2
                    )
                )
                .otherwise(None)
                .alias("mid_price"),
                # Volume imbalance
                pl.when(
                    (pl.col("total_buy_volume") > 0) & (pl.col("total_sell_volume") > 0)
                )
                .then(
                    (
                        pl.col("total_buy_volume")
                        / (pl.col("total_buy_volume") + pl.col("total_sell_volume"))
                    ).round(4)
                )
                .otherwise(None)
                .alias("volume_imbalance_ratio"),
            ]
        )
    )


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


async def extract_public_market_orders(  # noqa: PLR0915
    output_dir: str | None = None, stdout: Console | None = None
) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    """Extract public market orders and create aggregations.

    Args:
        output_dir: Optional output directory. If None, saves to current directory.
        stdout: Optional Console for output. If None, creates a new Console.

    Returns:
        Tuple of (raw_orders, market_indicators, order_depth) DataFrames
    """
    stdout = stdout or Console()
    timestamp = datetime.now(UTC)
    timestamp_str = timestamp.strftime("%Y%m%d%H%M%S")

    # Determine output directory
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
    else:
        out_path = Path.cwd()

    async with ClientSession(headers={"User-Agent": EVEDATA_USER_AGENT}) as session:
        total_pages, lazy_orders = await fetch_all_region_orders(session)
        lazy_orders = lazy_orders.with_columns(pl.lit(timestamp).alias("timestamp"))

        # Regional aggregation - group by region_id and type_id
        # Note: We include all orders except station-limited ones. This can result
        # in "crossed markets" where buy_price > sell_price due to range
        # limitations. For example, a buy order with range=3 at station A might
        # offer 3.0 ISK while a region-wide sell order at station B (10+ jumps away)
        # offers 2.0 ISK. These crossed markets represent real arbitrage
        # opportunities and market inefficiencies, not data errors. Station-limited
        # orders are excluded as they don't participate in the broader regional
        # market.
        regional_orders = lazy_orders.filter(pl.col("range") != "station")
        regional_agg = (
            create_market_indicators_aggregation(
                regional_orders, ["region_id", "type_id"]
            )
            .rename({"region_id": "location_id"})
            .with_columns(pl.lit("region").alias("location_type"))
        )

        # Station aggregation - group by location_id and type_id for all stations
        station_agg = create_market_indicators_aggregation(
            lazy_orders,
            ["location_id", "type_id"],
        ).with_columns(
            [
                pl.lit("station").alias("location_type"),
                pl.col("location_id").is_in(HUB_STATION_IDS).alias("is_hub"),
            ]
        )

        # Combine regional and station aggregations
        regional_agg = regional_agg.with_columns(pl.lit(False).alias("is_hub"))  # noqa: FBT003
        combined_agg = pl.concat([regional_agg, station_agg], how="vertical_relaxed")

        # Collect aggregated data and sort
        aggregated = await combined_agg.collect_async()
        aggregated = aggregated.sort(["location_type", "location_id", "type_id"])

        # Write market indicators with zstd compression
        indicators_filename = out_path / f"market_indicators_5m_{timestamp_str}.parquet"
        aggregated.write_parquet(
            indicators_filename,
            compression="zstd",
            compression_level=3,
        )

        stdout.print(f"\nMarket indicators saved to: {indicators_filename}")
        stdout.print(aggregated.describe())
        stdout.print(f"Total aggregated rows: {len(aggregated)}")
        regional_count = aggregated.filter(pl.col("location_type") == "region").height
        station_count = aggregated.filter(pl.col("location_type") == "station").height
        hub_count = aggregated.filter(pl.col("is_hub")).height
        stdout.print(f"Regional rows: {regional_count}")
        stdout.print(f"Station rows: {station_count}")
        stdout.print(f"  - Hub stations: {hub_count}")

        # Create order depth aggregations
        stdout.print("\n[bold]Creating order depth aggregations...[/bold]")

        # Regional depth - excluding station-only orders
        regional_depth = (
            create_order_depth_aggregation(regional_orders, ["region_id", "type_id"])
            .rename({"region_id": "location_id"})
            .with_columns(pl.lit("region").alias("location_type"))
        )

        # Station depth - all orders at each station
        station_depth = create_order_depth_aggregation(
            lazy_orders, ["location_id", "type_id"]
        ).with_columns(
            [
                pl.lit("station").alias("location_type"),
                pl.col("location_id").is_in(HUB_STATION_IDS).alias("is_hub"),
            ]
        )

        # Combine depth aggregations
        regional_depth = regional_depth.with_columns(pl.lit(False).alias("is_hub"))  # noqa: FBT003
        combined_depth = pl.concat(
            [regional_depth, station_depth], how="vertical_relaxed"
        )

        # Collect and sort depth data
        depth_data = await combined_depth.collect_async()
        depth_data = depth_data.sort(["location_type", "location_id", "type_id"])

        # Write order depth data
        depth_filename = out_path / f"market_order_depth_{timestamp_str}.parquet"
        depth_data.write_parquet(
            depth_filename,
            compression="zstd",
            compression_level=3,
        )

        stdout.print(f"\nOrder depth saved to: {depth_filename}")
        stdout.print(f"Total depth rows: {len(depth_data)}")
        regional_depth_count = depth_data.filter(
            pl.col("location_type") == "region"
        ).height
        station_depth_count = depth_data.filter(
            pl.col("location_type") == "station"
        ).height
        hub_depth_count = depth_data.filter(pl.col("is_hub")).height
        stdout.print(f"Regional depth rows: {regional_depth_count}")
        stdout.print(f"Station depth rows: {station_depth_count}")
        stdout.print(f"  - Hub stations: {hub_depth_count}")

        # Sample depth statistics
        sample = depth_data.head(5)
        if len(sample) > 0:
            stdout.print("\n[bold]Sample order depth data:[/bold]")
            for row in sample.iter_rows(named=True):
                buy_depth_count = len(row["buy_depth"]) if row["buy_depth"] else 0
                sell_depth_count = len(row["sell_depth"]) if row["sell_depth"] else 0
                stdout.print(
                    f"Location {row['location_id']}, Type {row['type_id']}: "
                    f"{buy_depth_count} buy levels, {sell_depth_count} sell levels"
                )

        # Collect and save raw orders
        orders = await lazy_orders.collect_async()
        orders = orders.sort(["region_id", "type_id", "order_id"])
        orders_filename = out_path / f"market_orders_{timestamp_str}.parquet"
        orders.write_parquet(
            orders_filename,
            compression="zstd",
            compression_level=3,
        )
        stdout.print(f"\nRaw orders saved to: {orders_filename}")
        stdout.print(f"Total pages fetched: {total_pages}")
        stdout.print(orders.describe())

        return orders, aggregated, depth_data


if __name__ == "__main__":
    import uvloop

    async def main():
        await extract_public_market_orders()

    uvloop.run(main())
