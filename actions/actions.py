from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import random
from datetime import date, timedelta

class ClientForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "client_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["client", "pesel"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "client": [
                self.from_entity(
                    entity="client",
                    intent="confirm_client"
                ),
            ],
            "pesel": [
                self.from_entity(
                    entity="pesel",
                    intent="confirm_pesel"
                ),
            ],
        }

    @staticmethod
    def client_db():
        """Database of supported cuisines"""

        return [["11111111","50102231284"],
                ["22222222","86071597139"],
                ["33333333","91031787413"],
                ["44444444","53100614985"],
                ["55555555","65062479537"],
                ["66666666","76052569857"],
                ["77777777","84102279913"],
                ["88888888","77081668908"],
                ["99999999","79051479923"],]

    def validate_client(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if value.lower() in [row[0] for row in self.client_db()]:
            # validation succeeded, set the value of the "client" slot to value
            return {"client": value}
        else:
            dispatcher.utter_message(template="utter_wrong_client")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"client": None}
    
    def validate_pesel(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if value.lower() in self.client_db()[[row[0] for row in self.client_db()].index(tracker.get_slot("client"))][1]:
            # validation succeeded, set the value of the "pesel" slot to value
            return {"pesel": value}
        else:
            dispatcher.utter_message(template="utter_wrong_pesel")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"pesel": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_submit")
        return []

class ActionMeterRead(Action):

    def name(self) -> Text:
        return 'action_meter_read'

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        if tracker.get_slot("client") != None and tracker.get_slot("pesel") != None:
            dispatcher.utter_message(text="Twój ostatni odczyt z dnia **{}** wyniósł: **{}** kWh".format((date.today() - timedelta(14)).strftime("%d-%m-%Y"), random.randint(100,1000)))  # send the message back to the user
            dispatcher.utter_message(template='utter_help')
            return []
        else:
            dispatcher.utter_message(template='utter_default')

class ActionBill(Action):

    def name(self) -> Text:
        return 'action_bill'

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        if tracker.get_slot("client") != None and tracker.get_slot("pesel") != None:
            dispatcher.utter_message(text="Twoja ostatnia faktura z dnia **{}** wyniosła: **{}** PLN ".format((date.today() - timedelta(14)).strftime("%d-%m-%Y"), random.randint(100,1000)))  # send the message back to the user
            dispatcher.utter_message(template='utter_help')
            return []
        else:
            dispatcher.utter_message(template='utter_default')

class ActionSaldo(Action):

    def name(self) -> Text:
        return 'action_saldo'

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        if tracker.get_slot("client") != None and tracker.get_slot("pesel") != None:
            dispatcher.utter_message(text="Twoje obecne saldo na dzień **{}** wynosi: **{}** PLN".format(date.today().strftime("%d-%m-%Y"), random.randint(100,1000)))  # send the message back to the user
            dispatcher.utter_message(template='utter_help')
            return []
        else:
            dispatcher.utter_message(template='utter_default')
