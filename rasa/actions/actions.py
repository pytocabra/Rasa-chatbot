# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import json
import random

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionIsOpen(Action):

    def name(self) -> Text:
        return "action_is_open"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        for blob in tracker.latest_message['entities']:
            print(tracker.latest_message)
            
            if blob['entity'] == 'day_name':
                day = blob['value'].lower()

                f = open('data/opening_hours.json')
                data = json.load(f)
                for dayy in data['items']:
                    if day == dayy.lower():
                        if data['items'][dayy]['open'] == 0 and data['items'][dayy]['close'] == 0:
                            results = [
                                f"I'm sorry, we are closed on {dayy}",
                                f"We are not opened on {dayy}",
                                f"Closed. Sorry.",
                            ]
                            dispatcher.utter_message(text=results[random.randint(0,2)])
                        else:
                            results = [
                                f"Restaurant is open from {data['items'][dayy]['open']} to {data['items'][dayy]['close']}",
                                f"On {dayy} we are open {data['items'][dayy]['open']}-{data['items'][dayy]['close']}",
                                f"Opening hours on {dayy} {data['items'][dayy]['open']}-{data['items'][dayy]['close']}"
                            ]
                            dispatcher.utter_message(text=results[random.randint(0,2)])
                f.close()
        return []

class ActionListMenu(Action):

    def name(self) -> Text:
        return "action_list_menu"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        f = open('data/menu.json')
        data = json.load(f)

        items = ', '.join([item['name']  for item in data['items']])

        results = [
            f"{items}",
            f"You can order:\n {items}",
            f"Here you have our menu: {items}",
        ]
        dispatcher.utter_message(text=results[random.randint(0,2)])

        f.close()
        return []

class ActionPlaceOrder(Action):

    def name(self) -> Text:
        return "action_place_order"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        for blob in tracker.latest_message['entities']:
            print(tracker.latest_message)
            
            if blob['entity'] == 'order_name':
                order_name = blob['value'].lower()

                f = open('data/menu.json')
                data = json.load(f)

                for item in data['items']:
                    if item['name'].lower() == order_name:
                        order_json = item

                results = [
                    f"Order confirmation: {order_json['name']} for {order_json['price']} USD will be ready in {order_json['preparation_time']} h",
                    f"Your order '{order_json['name']}' will be ready in {order_json['preparation_time']} h",
                    f"Here you have our menu: {order_json}",
                ]
                dispatcher.utter_message(text=results[random.randint(0,2)])
                f.close()
        return []

