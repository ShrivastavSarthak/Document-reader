import spacy

nlp = spacy.load("en_core_web_sm")

def create_chunk(text:str, max_word:int=100):
    doc = nlp(text)
    chunks = []
    current_chunk=[]
    word_count = 0
    for sentence in doc.sents:
        sentence_text = sentence.text.strip()
        sentence_word = len(sentence_text.split())
        
        if current_chunk and word_count + sentence_word > max_word:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            word_count = 0
        
        current_chunk.append(sentence_text)
        word_count +=sentence_word
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks