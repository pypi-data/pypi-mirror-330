from pathlib import Path
import duckdb
import polars as pl
from rich import print
from core_pro.ultilities import make_dir, upload_to_datahub, create_batch_index
from datetime import date
import sys

sys.path.extend([str(Path.home() / 'PycharmProjects/model_train')])
from src.model_train.pipeline_infer import InferenceTextClassification
from classification.cx_item_reviews.prod.config import (
    path_model,
    api_endpoint,
    ingestion_token,
    path
)

# path
file_raw = sorted([*path.glob(f'deploy/raw/*')])

# path export
path_export_inference = path / f'deploy/inference/{date.today()}'
make_dir(path_export_inference)
path_export = path / f'deploy/inference/export_{date.today()}'
make_dir(path_export)

# init model
infer = InferenceTextClassification(
    path_model=str(path_model),
    col='comment',
    torch_compile=True,
    fp16=True
)

for f in file_raw:
    print(f'=== START {f.name} ===')
    # data
    query = f"""
    select * exclude(comment_stats)
    , cast(unnest(comment_stats, recursive := true)::json as STRUCT(comment_id bigint, comment VARCHAR, rating_star int, create_date date)) comment_stats
    from read_parquet('{f}')
    """
    df = (
        duckdb.sql(query).pl()
        .unnest('comment_stats')
    )
    print(f'Data Shape: {df.shape}, Total Items: {df['item_id'].n_unique():,.0f}')

    # inference
    col = ['comment_id', 'comment']
    file_export = path_export_inference / f'{f.stem}.parquet'
    if not file_export.exists():
        ds_pred = infer.run(data=df[col])
        ds_pred_post = (
            ds_pred
            .to_polars()
            .explode(['labels', 'score'])
            .pivot(index=col, on='labels', values='score', aggregate_function='sum')
         )

        ds_pred_post.write_parquet(file_export)
    else:
        ds_pred_post = pl.read_parquet(file_export)

    df_export = (
        df.join(ds_pred_post.drop(['comment']), how='left', on='comment_id', coalesce=True)
        .select(df.columns + infer.id2label)
    )
    print(f'Data merge Inference shape: {df_export.shape}')

    # a = df_export.filter(item_id=15485771904)
    # b = df_export.filter(comment_id=25467692158)

    # export
    file_csv = path_export / f'pred_{f.stem}.csv'
    df_export.write_csv(file_csv)
    print(f'=== DONE {f.name} ===\n')
    # break

# up to data hub
# file_csv = [*path_export.glob('pred_*')]
# df_csv = pl.concat([pl.read_csv(f) for f in file_csv])
#
# file_csv_all = path_export / 'concat_all.csv'
# df_csv.write_csv(file_csv_all)
# upload_to_datahub(file_csv_all, api_endpoint, ingestion_token)
