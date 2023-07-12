import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

data = pd.read_json(path_or_buf="./export_data/records.json")
data_df = pd.DataFrame(data)
data_df = data_df.dropna(subset=['f1', 'f2', 'f3', 'f4', 'f5', 'f6'])
data_df = data_df[['id', 'name', 'brewery_name','area', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6']]

def find_similar_sake(sake_id):
    # target:
    target_sake = data_df.query(f"id=={sake_id}")

    if target_sake[['f1', 'f2', 'f3', 'f4', 'f5', 'f6']].size:
        target_score = target_sake[['f1', 'f2', 'f3', 'f4', 'f5', 'f6']].values
        all_score = data_df[['f1', 'f2', 'f3', 'f4', 'f5', 'f6']].values
        similarities = cosine_similarity(target_score.reshape(1, -1), all_score)

        # [0:1] 是 target 自己
        top_indexes = np.argsort(similarities[0])[::-1][1:2]
        top_similar_data = data_df.iloc[top_indexes].to_dict(orient='records')
        return top_similar_data
    else:
        return None

recommendations = {}
for sid in data_df['id']:
    recommendations[sid] = find_similar_sake(sid)
export_json = pd.DataFrame(recommendations).to_json(path_or_buf="./export_data/recommendations.json", force_ascii=False)
