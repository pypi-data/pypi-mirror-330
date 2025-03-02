from huggingface_hub import hf_hub_download
import floret

class FloretPipeline:   
    def __init__(self, model_name="floret_model.bin", repo_id="Maslionok/sudo_pipelines", revision="main"):
        model_path = hf_hub_download(repo_id=repo_id, filename=model_name, revision=revision)
        self.model = floret.load_model(model_path)

    def __call__(self, text):
        output = self.model.predict(text, k=1)
        language, value = output
        language = language[0].replace("__label__", "")


        return language
