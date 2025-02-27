from typing import List
from rara_meta_extractor.llama_api_wrapper import LlamaAPIConnector
from rara_meta_extractor.schema_generator import JSONSchemaGenerator
from rara_meta_extractor.config import DEFAULT_CONFIG


class LlamaExtractor:
    def __init__(
        self, 
        llama_host_url: str, 
        fields: List[str] | List[dict] = DEFAULT_CONFIG.get("fields"),    
        instructions: str = DEFAULT_CONFIG.get("instructions"),
        temperature: float = 0.7, 
        n_predict: int = 500,
        **kwargs
    ):
        self.llama_host_url: str = llama_host_url
        self.fields_schema: List[str] | List[dict] = fields

        self.llama_connector: LlamaAPIConnector = LlamaAPIConnector(
            host_url=llama_host_url, 
            temperature=temperature, 
            n_predict=n_predict,
            **kwargs
        )
        self.schema_generator: JSONSchemaGenerator = JSONSchemaGenerator()
        self.__fields: List[str]  = []
        self.__fields_str: str = ""
        self.__instructions: str = instructions.format(self.fields_str)
        self.__json_schema: dict = self.schema_generator.generate_json_schema(
            fields=self.fields_schema
        )
        
        
    @property
    def fields(self) -> List[str]:
        if not self.__fields:
            if isinstance(self.fields_schema[0], dict):
                self.__fields = [
                    field.get("name") 
                    for field in self.fields_schema
                ]
            else:
                self.__fields = self.fields_schema
        return self.__fields
    
        
    @property
    def fields_str(self) -> str:
        if not self.__fields_str:
            self.__fields_str = ", ".join(self.fields)
        return self.__fields_str
    
    @property
    def instructions(self) -> str:
        return self.__instructions
    
    @property
    def json_schema(self) -> str:
        return self.__json_schema
    
    
    def extract(self, text: str) -> dict:
        extracted_data = self.llama_connector.extract(
            instructions=self.instructions, 
            context=text, 
            json_schema=self.json_schema
        )
        return extracted_data
    
if __name__ == "__main__":
    from pprint import pprint
    from rara_meta_extractor.utils import load_txt
    import os
    
    TEST_FILE_PATH = os.path.join(".", "data", "test_text.txt")
    TEST_TEXT = load_txt(TEST_FILE_PATH)
    
    llama_extractor = LlamaExtractor(llama_host_url="http://dev-elastic1.texta.ee:8080")
   
    extracted_info = llama_extractor.extract(text=TEST_TEXT)
    pprint(extracted_info)