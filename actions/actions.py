from typing import Any, Text, Dict, List
import logging
import pandas as pd
import random

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .utils import isHangul

logger = logging.getLogger(__name__)

VOCAB_FILE_PATH = "actions/vocab.csv"
# change for another ask_synonim, ask_comparison
# INI_DEFINITION_TEMPLATE = ["{id_word} adalah {ko_sound} {ko_word}.", # e.g)Tentara adalah gunin 군인
#                     "{ko_sound} {ko_word}"  #  e.g) Chinjolhada 친절하다
#                     ]
INI_DEFINITION_TEMPLATE = {
    "ask_definition" : "{id_word} adalah {ko_sound} {ko_word}",
    "ask_synonym" : "Selain {ko_sound}{ko_word}, ada kata lain yang dapat diartikan {id_word} yaitu {ko_synonym}.",
}
KOR_DEFINITION_TEMPLATE =  ["{ko_sound} {ko_word} adalah {id_word}", #  e.g) gyong-je-hak 경제학' adalah jurusan ekonomi
                        "{ko_sound} {ko_word} adalah ibu {id_word}" # e.g) jubu 주부 adalah ibu rumah tangga
                        ]


class ActionAskDefinition(Action):

    def name(self) -> Text:
        return "action_ask_definition"

    def __init__(self) -> None:
        self.df = pd.read_csv(VOCAB_FILE_PATH)
        self.df['ko_word'] = self.df['ko_word'].map(lambda x: x.replace('.',''))
        self.category = "Vocabulary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        word = tracker.get_slot("word")
        intent = tracker.latest_message['intent'].get('name')

        no_match=False
        if not isHangul(word):
            if word in self.df.id_short.values:
                answer_df = self.df[self.df["id_short"]==word]
                # response = random.sample(INI_DEFINITION_TEMPLATE, 1)[0]
                response = INI_DEFINITION_TEMPLATE[intent]
            else:
                no_match=True
        else:
            if word in self.df.ko_word.values:
                answer_df = self.df[self.df["ko_word"]==word]
                # response = random.sample(KOR_DEFINITION_TEMPLATE, 1)[0]
                response = INI_DEFINITION_TEMPLATE[intent]
            else:
                no_match=True
        #category, intent
        if not no_match:
            answer_dict = {"id_word":answer_df.id_word.values[0],"ko_sound":answer_df.ko_sound.values[0],"ko_word":answer_df.ko_word.values[0]}
            dispatcher.utter_message(text=f"entity:{word},category:{self.category},intent:{intent}")
            dispatcher.utter_message(text=response.format(**answer_dict))
        else:
            dispatcher.utter_message(text=f"entity:{word},category:{self.category},intent:{intent}")
            # dispatcher.utter_message(text="Please ask your teacher to exlain about "+word)
            dispatcher.utter_message(text="Silahkan bertanya langsung ke pengajar tentang kosa kata "+word)

class ActionAskSynonym(Action):
    def name(self) -> Text:
        return "action_ask_synonym"

    def __init__(self) -> None:
        self.df = pd.read_csv(VOCAB_FILE_PATH)
        self.df['ko_word'] = self.df['ko_word'].map(lambda x: x.replace('.',''))
        self.category = "Vocabulary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        word = ""
        intent = tracker.latest_message['intent'].get('name')

        entities = []
        for entity in tracker.latest_message['entities']:
            entities.append(
                {"entity": entity["entity"], "value": entity["value"],
                "role": entity.get("role") }
            )
            if entity.get("role") != "equalto":
                word = entity["value"]
        
        # msg = str(entities) + "\n"
        # dispatcher.utter_message(msg)
        dispatcher.utter_message(text=f"entity:{word},category:{self.category},intent:{intent}")
        dispatcher.utter_message(text="You asked the synonym of "+word)

        no_match=False
        if not isHangul(word):
            if word in self.df.id_short.values:
                answer_df = self.df[self.df["id_short"]==word]
                response = INI_DEFINITION_TEMPLATE[intent]
                print(f"response : {response}")
                print(f"answer_df = {answer_df}")
            else:
                no_match=True
        else:
            if word in self.df.ko_word.values:
                answer_df = self.df[self.df["ko_word"]==word]
                response = INI_DEFINITION_TEMPLATE[intent]
                print(f"response : {response}")
                print(f"answer_df = {answer_df}")
            else:
                no_match=True
        #category, intent
        if not no_match:
            answer_dict = {"ko_sound":answer_df.ko_sound.values[0],"ko_word":answer_df.ko_word.values[0],"id_word":answer_df.id_word.values[0],"ko_synonym":answer_df.ko_synonym.values[0]}
            dispatcher.utter_message(text=f"entity:{word},category:{self.category},intent:{intent}")
            dispatcher.utter_message(text=response.format(**answer_dict))
        else:
            dispatcher.utter_message(text=f"entity:{word},category:{self.category},intent:{intent}")
            # dispatcher.utter_message(text="Please ask your teacher to exlain about "+word)
            dispatcher.utter_message(text="Silahkan bertanya langsung ke pengajar tentang kosa kata "+word)
        