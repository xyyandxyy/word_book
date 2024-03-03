import torch
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

# 加载预训练的BERT模型和tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# 要聚类的词汇列表
df = pd.read_excel('file.xlsx')
vocab_list = ["chicken", "beef", "food", "jail", "killer", "sucker", "murder"]  # 包含1000个词汇的列表

# 提取每个词汇的嵌入
embeddings = []
for word in vocab_list:
    # 添加特殊标记[CLS]和[SEP]以构造BERT输入
    marked_text = "[CLS] " + word + " [SEP]"
    # 使用tokenizer将文本转换为token ID
    tokenized_text = tokenizer.tokenize(marked_text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    # 将token ID转换为torch张量
    tokens_tensor = torch.tensor([indexed_tokens])
    # 使用BERT模型获取嵌入
    with torch.no_grad():
        outputs = model(tokens_tensor)
        # 取出[CLS]标记的嵌入作为词汇的嵌入表示
        embeddings.append(outputs[0][:, 0, :].numpy())

# 将嵌入表示转换为二维数组
embeddings = np.array(embeddings).reshape(len(embeddings), -1)

# 使用KMeans进行聚类
num_clusters = 3  # 你可以根据需要调整聚类的数量
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(embeddings)

# 输出每个词汇以及它所属的聚类
clusters = {}
for i, word in enumerate(vocab_list):
    cluster_label = kmeans.labels_[i]
    if cluster_label not in clusters:
        clusters[cluster_label] = []
    clusters[cluster_label].append(word)

for cluster_label, words in clusters.items():
    print(f"Cluster {cluster_label + 1}: {', '.join(words)}")
