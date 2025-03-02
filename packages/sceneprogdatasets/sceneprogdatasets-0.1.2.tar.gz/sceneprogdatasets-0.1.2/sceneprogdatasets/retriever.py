from .HSSD.hssd import AssetRetrieverHSSD
from .future.future import AssetRetrieverFuture

class SceneProgAssetRetriever:
    def __init__(self):
       
        import os
        from pathlib import Path
        path = Path(__file__).parent
        
        if os.getenv('FUTURE_PATH') is None or os.getenv('HSSD_PATH') is None:
            msg = f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
You need to set the FUTURE_PATH and HSSD_PATH environment variables first!

Run the following commands to set the environment variables:
export FUTURE_PATH=<path_to_future_assets>
export HSSD_PATH=<path_to_hssd_assets>

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
            raise Exception(msg)
        
            
        if not os.path.exists(os.path.join(path,'HSSD/assets/model2description.json')) or not os.path.exists(os.path.join(path,'future/assets/model2description.json')):
            msg = f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
You need to download the assets first!

Run the following commands to download the assets:

aws s3 cp s3://sceneprog-nautilus/sceneprogdatasets/future/ {os.path.join(path,'future/assets')} --recursive
aws s3 cp s3://sceneprog-nautilus/sceneprogdatasets/hssd/ {os.path.join(path,'HSSD/assets')} --recursive

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
            raise Exception(msg)
       
        self.hssd = AssetRetrieverHSSD()
        self.future = AssetRetrieverFuture()
    
    def __call__(self, description):
        ## first search in Future
        future_results = self.future.run(description)
        if not future_results == 'No models found':
            return ("FUTURE",future_results)
        
        ## then search in HSSD
        hssd_results = self.hssd.run(description)
        if not hssd_results == 'No models found':
            return ("HSSD",hssd_results)
        
        return "No models found"