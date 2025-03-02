import os
import json
import trimesh
import numpy as np
from tqdm import tqdm 
from langchain_openai import OpenAIEmbeddings

# FUTURE_PATH = '/Users/kunalgupta/Documents/sceneprog-datasets/3D-FUTURE-models'
FUTURE_PATH = os.getenv('FUTURE_PATH')

from pathlib import Path
BASE = str(Path(__file__).parent)
# BASE=os.getcwd()+'/sceneprogdatasets/future/'
embd_location = os.path.join(BASE,'assets/embeddings_future.npz')
model2description_location = os.path.join(BASE,'assets/model2description.json')

def load_model(assetID):
    path = os.path.join(FUTURE_PATH, assetID+'.glb')
    return trimesh.load(path, process=False, force='mesh')

class AssetRetrieverFuture:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv("OPENAI_API_KEY"))

        with open(model2description_location, 'r') as f:
            self.MODEL_TO_DESCRIPTION = json.load(f)

        if not os.path.exists('assets/embedding_future.npz'):
            self.build()
        
        data = np.load(embd_location, allow_pickle=True)
        self.all_embeddings = data['all_embeddings']
        self.all_models = data['all_models']
        self.all_ratios = data['all_ratios']  
        
    
    def build(self):
        from_scratch=True
        if os.path.exists(embd_location):
            data = np.load(embd_location)
            all_embeddings = data['all_embeddings']
            all_models = data['all_models'].tolist()
            all_ratios = data['all_ratios']
            from_scratch=False
            
        else:        
            all_embeddings = []
            all_models = []
            all_ratios = []
        
            for file in tqdm(os.listdir(FUTURE_PATH)):
                if file.endswith('.glb'):
                    assetID = file.split('.')[0]
                    if assetID in all_models:
                        continue
                    try:
                        mesh = load_model(assetID)
                    except:
                        print("Error loading ", assetID)
                        continue
                    
                    bounds = mesh.bounds
                    width = bounds[1,0] - bounds[0,0]
                    depth = bounds[1,2] - bounds[0,2]
                    height = bounds[1,1] - bounds[0,1]
                    x0 = depth/width
                    y0 = height/width
                    
                    desc=self.MODEL_TO_DESCRIPTION[assetID]
                    emb = np.array(self.embeddings.embed_query(desc))
                    all_models.append(assetID)
                    if from_scratch:
                        all_ratios.append(np.array([x0, y0]))
                        all_embeddings.append(emb)
                        
                    else:
                        all_ratios = np.vstack((all_ratios, np.array([x0, y0])))
                        all_embeddings = np.vstack((all_embeddings, emb))
            
        np.savez(embd_location, all_embeddings=all_embeddings, all_models=all_models, all_ratios=all_ratios)

    def compute_ratio_sim(self, query):
        dims = ScaleObj().run(query)
        w,d,h = dims['width'], dims['depth'], dims['height']
        x0 = d/w
        y0 = h/w
        target_ratio = np.array([x0, y0])
        ratio_sim = np.linalg.norm(self.all_ratios - target_ratio, axis=1)
        return ratio_sim
    
    def run(self, query):
        emb = np.array(self.embeddings.embed_query(query))
        similarity = np.dot(self.all_embeddings, emb)
        ratio_sim = self.compute_ratio_sim(query)
        
        top_20_indices = np.argsort(similarity)[-20:][::-1]
        result = sorted([(i, similarity[i], ratio_sim[i]) for i in top_20_indices], key=lambda x: x[-1])[:10]
        top_10_indices = [i for i,_,_ in result]
        top_10_models = [self.all_models[i] for i in top_10_indices]

        scores = similarity[top_10_indices]
        models = top_10_models
        if np.max(scores) < 0.4:
            return "No models found"
        
        scores = 5*(scores-0.4)
        scores = np.exp(scores)/np.sum(np.exp(scores))
        model = np.random.choice(models, p=scores)

        path = os.path.join(FUTURE_PATH, model+'.glb')

        return path
    
class ScaleObj:
    def __init__(self):
        from sceneprogllm import LLM
        self.llm = LLM(name="dataset_scale_obj", system_desc="You are a large language model based assistant, your job is to scale the object to the given dimensions. You only answer in the way following examples do. Anyother type of response is strictly forbidden. Return the values in meters.")
        self.reset()

    def reset(self):
        self.prompt = """
User Input: A dining chair
Your Response: ```{''height'':1.0, 'width':0.5, 'depth':0.5}```
User Input: A king-size bed
Your Response: ```{'height':1.5, 'width':2.0, 'depth':2.1}```
User Input: A armchair
Your Response: ```{'height':1.0, 'width':0.9, 'depth':0.95}```
User Input: A coffee table
Your Response: ```{'height':0.6, 'width':1.0, 'depth':1.0}```
User Input: A really long dining table
Your Response: ```{'height':0.7, 'width':8.0, 'depth':3.0}```
User Input: A tall bookcase
Your Response: ```{'height':2.5, 'width':1.0, 'depth':0.5}```
User Input: A small nightstand
Your Response: ```{'height':0.5, 'width':0.5, 'depth':0.5}```
User Input: A large Chandelier
Your Response: ```{'height':0.8, 'width':0.5, 'depth':0.5}```
"""
    def run(self, query):
        self.prompt = f"{self.prompt}\n. User Input: {query}\n"
        self.prompt += "Your response:"
        return self._sanitize_output(self.llm(self.prompt))
    
    def _sanitize_output(self, text: str):
        import ast
        return ast.literal_eval(str(text.split("```")[1]))
    
# retriever = AssetRetrieverFuture()
# print(retriever.run("A dining table with a glass top"))

