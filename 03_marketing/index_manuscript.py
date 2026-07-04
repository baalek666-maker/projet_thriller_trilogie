#!/usr/bin/env python3
"""Indexe le manuscrit La Remplaçante avec LlamaIndex + embeddings locaux."""
import os
from pathlib import Path

from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file import MarkdownReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

REPO_ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = REPO_ROOT / "04_manuscrits" / "la_remplacante_tome1.md"
STORAGE_DIR = REPO_ROOT / "03_marketing" / "storage"

if not MANUSCRIPT.exists():
    raise FileNotFoundError(f"Manuscrit non trouvé : {MANUSCRIPT}")

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    trust_remote_code=True,
)

if STORAGE_DIR.exists():
    print("Chargement de l'index existant...")
    storage_context = StorageContext.from_defaults(persist_dir=str(STORAGE_DIR))
    index = load_index_from_storage(storage_context, embed_model=embed_model)
else:
    print("Lecture et découpage du manuscrit...")
    reader = MarkdownReader()
    documents = reader.load_data(file=MANUSCRIPT)
    parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = parser.get_nodes_from_documents(documents)
    print(f"{len(nodes)} blocs créés.")
    print("Indexation en cours (premier lancement = téléchargement du modèle)...")
    index = VectorStoreIndex(nodes, embed_model=embed_model, show_progress=True)
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    index.storage_context.persist(persist_dir=str(STORAGE_DIR))
    print(f"Index sauvegardé dans {STORAGE_DIR}")

print("Prêt pour les requêtes.")
