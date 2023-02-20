from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

from konlpy.tag import Mecab

# TODO: Correctly register your component with its type
@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER], is_trainable=False
)
class MecabTokenizer(Tokenizer):
    
    def __init__(self,config: Dict[Text, Any]) -> None:
        super().__init__(config)

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns default config (see parent class for full docstring)."""
        return {
            # Flag to check whether to split intents
            "intent_tokenization_flag": False,
            # Symbol on which intent should be split
            "intent_split_symbol": "_",
            # Regular expression to detect tokens
            "token_pattern": None,
        }

    def tokenize(self,message: Message, attribute: Text) -> List[Token]:

        m= Mecab()
        text = message.get(attribute)
        words = m.morphs(text)
        # tokens = [Token(word, start) for (word, start, end) in tokenized]
        tokens = self._convert_words_to_tokens(words, text)
        return self._apply_token_pattern(tokens)
    
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        # TODO: Implement this
        return cls(config)

#     def train(self, training_data: TrainingData) -> Resource:
#         # TODO: Implement this if your component requires training
#         ...

#     def process_training_data(self, training_data: TrainingData) -> TrainingData:
#         # TODO: Implement this if your component augments the training data with
#         #       tokens or message features which are used by other components
#         #       during training.
#         ...

#         return training_data

#     def process(self, messages: List[Message]) -> List[Message]:
#         # TODO: This is the method which Rasa Open Source will call during inference.
#         ...
#         return messages

