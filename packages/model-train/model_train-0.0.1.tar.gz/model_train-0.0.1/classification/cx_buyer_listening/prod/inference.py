from pathlib import Path
import polars as pl
from rich import print
from core_pro.ultilities import make_dir, create_batch_index, update_df
from datetime import date
import duckdb
import sys

sys.path.extend([str(Path.home() / 'PycharmProjects/model_train')])
from src.model_train.pipeline_infer import InferenceTextClassification
from classification.cx_buyer_listening.prod.config import (
    path,
    sh
)

f = [*path.glob('*cleaned.parquet')][0]

# path export
path_export_inference = path / f'inference/{date.today()}'
make_dir(path_export_inference)

# init model
path_model = 'kevinkhang2909/buyer_listening'
infer = InferenceTextClassification(
    path_model=str(path_model),
    pretrain_name=str(path_model),
    col='text_clean',
    torch_compile=True,
    fp16=True,
    mode='multi_classes'
)

print(f'=== START {f.name} ===')
# data
df = pl.read_parquet(f)
print(f'Data Shape: {df.shape}, Total Items: {df['text'].n_unique()}')

# batching
col = ['index', 'text', 'text_clean', 'l1', 'l2']
batches = create_batch_index(df.shape[0], n_size=100_000)
for i, v in batches.items():
    file_export = path_export_inference / f'{f.stem}_{i}.parquet'
    if file_export.exists():
        print(f'Batch Done: {file_export.stem}')
        continue

    # infer
    print(f'Start Batch {i}/{len(batches)}: {file_export.stem}')
    ds_pred = infer.run(data=df[col].filter(pl.col('index').is_in(v)))

    # post process
    ds_pred_post = (
        ds_pred
        .to_polars()
        .with_columns(
            pl.col('labels').str.split(' >> ').list[i].alias(v)
            for i, v in enumerate(['l1_pred', 'l2_pred'])
        )
        .with_columns(
            (pl.col(i) == pl.col(f'{i}_pred')).alias(f'check_{i}')
            for i in ['l1', 'l2']
        )
    )

    # export
    ds_pred_post.write_parquet(path_export_inference / f'{f.stem}_{i}.parquet')
    break

query = f"""select * exclude(labels) from read_parquet('{path_export_inference}/*.parquet')"""
tmp = duckdb.sql(query).pl()
print(f'Data Inference shape: {tmp.shape}')

update_df(tmp.head(1000), 'sample', sh )
