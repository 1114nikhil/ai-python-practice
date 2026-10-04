import sys 
import tiktoken

sys.stdout.reconfigure(encoding="utf-8")

enc= tiktoken.get_encoding("cl100k_base")

def show(text:str):
    token_ids=enc.encode(text)
    pieces= [enc.decode([tid]) for tid in token_ids]
    print(f"\nText: {text!r}")
    print(f"Tokens ({len(token_ids)}):")
    print(f"Pieces: {pieces}")

# show("I'm frustratred")
# show("unbelievable")
# show("BeanCurrentlyInCreationException")
# show("नमस्ते, कैसे हो आप?")   # Hindi: common everyday phrase
# # show("    ")                   # just whitespace
show("Hi, My order never arived, its been 2 week,")                  # just whitespace
# show("4471")