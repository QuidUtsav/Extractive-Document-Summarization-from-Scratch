#Importing Libraries
import re


#Defining the preprocess function

def tokenize(text):
    return re.findall(r'\b\w+\b',text.lower())
def normalize_text(text):
    return text.lower().strip()

def clean_doc(text):
    cleaned_text= re.sub(r'\[.*?\]','',text)
    cleaned_text=re.sub(r'[\r\n]','\n',cleaned_text)
    return cleaned_text.strip()

def extract_keywords(text):
    
    return {k for k in tokenize(text) if len(k)>3}


def chunk_document(text):
    chunk = re.split(r'\n{2,}',text)
    refined_chunk=[]
    for index,chunk in enumerate(chunk):
        refined_obj={
            "Chunk_id":f"Document_overview_{index}",
            "text":chunk,
            "chunk_length":len(chunk),
            "Number_of_sentences":len(re.findall(r'[.!?]+',chunk)),
            "position":index
        }
        refined_chunk.append(refined_obj)
    return refined_chunk
    
def split_sentences(chunk):
    return re.split(r'[.!?]+',chunk)
     
def score_sentences(text,keywords):
    tokens = tokenize(text)
    return sum(1 for k in keywords if k in tokens)

def summarize_chunk(chunk_text,max_sentence=3):
    sentences = split_sentences(chunk_text)
    keywords = extract_keywords(chunk_text)
    
    scored_sentences = []
    for index,sentence in enumerate(sentences):
        score = score_sentences(sentence,keywords)
        if index==0:
            score+=1.5
        scored_sentences.append((score,index,sentence))
    top_sentences = sorted(scored_sentences, key=lambda x: x[0], reverse=True)[:max_sentence]
    
    top_sentences.sort(key=lambda x: x[1])
    
    return [s[2].strip() + "." for s in top_sentences]

#main function

RAW_DOC = """One Piece is set on the Blue Planet, populated by humans and other races such as dwarves (more akin to fairies in size), giants, merfolk, fish-men, long-limbed tribes, long-necked people known as the Snakeneck Tribe, and animal people, known as "Minks". The Blue Planet is governed by an authoritarian intercontinental organization known as the World Government, consisting of dozens of member countries. The Navy is the military branch of the World Government that protects the known seas from pirates and other criminals. Cipher Pol acts as the World Government's secret police. While pirates are major opponents of the Government, the ones who challenge their rule are the Revolutionary Army who seek to overthrow them. The central tension of the series pits the World Government and their forces against pirates. The series regularly emphasizes moral ambiguity over the label "pirate", which includes morally bankrupt individuals motivated by selfish gains, but also any individuals who do not submit to the World Government's authoritarian—and often morally ambiguous—rule. The One Piece world also has supernatural objects such as Devil Fruits,[Jp 1] which are mysterious fruits that grant consumers transformative powers at the cost of becoming weakened in bodies of water, causing users to lose the ability to swim. Another supernatural power is Haki,[Jp 2] which grants its users enhanced observation and fighting abilities based on their willpower; it is one of the only effective methods of inflicting bodily harm on certain Devil Fruit users.

The surface of the Blue Planet mainly consists of the Blue Sea, two vast oceans divided by a massive continental mountain range called the Red Line.[Jp 3] Within the oceans is a second global phenomenon known as the Grand Line,[Jp 4] which is a sea that runs perpendicular to the Red Line and is bounded by the Calm Belt,[Jp 5] strips of calm ocean infested with huge ship-eating monsters known as Sea Kings.[Jp 6] These geographical barriers divide the world into four seas: North Blue,[Jp 7] East Blue,[Jp 8] West Blue,[Jp 9] and South Blue.[Jp 10] Passage between the four seas, and the Grand Line, is therefore difficult. Unique and mystical features enable transport between the seas, such as the use of Sea Prism Stone[Jp 11] employed by government ships to mask their presence as they traverse the Calm Belt, or the Reverse Mountain[Jp 12] where water from the four seas flows uphill before merging into a rapidly flowing and dangerous canal that enters the Grand Line. The Grand Line itself is split into two separate halves, with the Red Line being between Paradise[Jp 13] and the New World.[Jp 14] """

cleand_doc =clean_doc(RAW_DOC)
chunks = chunk_document(cleand_doc)
for chunk in chunks:
    print(summarize_chunk(chunk['text']))
