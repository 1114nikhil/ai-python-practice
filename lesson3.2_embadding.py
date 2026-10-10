import os
import sys
import math

from dotenv import load_dotenv
import voyageai

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()
client=voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])

EMBED_MODEL="voyage-4"

def embed(texts:list[str],input_type:str)->list[list[float]]:
    result=client.embed(texts,model=EMBED_MODEL,input_type=input_type)
    return result.embeddings

def cosine_similarity(a:list[float],b:list[float]) ->float:
    dot=sum(x*y for x,y in zip(a,b))
    norm_a=math.sqrt(sum(x*x for x in a))
    norm_b=math.sqrt(sum(y*y for y in b))
    return dot/(norm_a*norm_b)

sentences = {
    "A":"My order never arived, it's been two weeks",
    "B": "The delivery hasn't shown up and it's been 14 days.",
    "C": "The weather has been really nice this week.",
    "D": "I want to cancel my subscription immediately.",
    "E": "My order #9912 never arrived, it's been two weeks."
}

keys= list(sentences.keys())
vectors_list=embed([sentences[k] for k in keys], input_type="document")
vectors = dict(zip(keys,vectors_list))

print(f"Vector dimensions: {len(vectors['A'])}\n")

pairs= [("A","B"),("A","C"),("A","D"),("B","C"),("E","A")]

for x,y in pairs:
    sim=cosine_similarity(vectors[x],vectors[y])
    print(f"{x} vs {y}: similarity = {sim:.4f}")
    print(f"   {x}: {sentences[x]!r}")
    print(f"   {y}: {sentences[y]!r}\n")