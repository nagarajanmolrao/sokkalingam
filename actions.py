from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker,events
from rasa_sdk.events import  FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
from datetime import datetime
from PIL import Image, ImageDraw
import pyqrcode
import png
import random


class AskDate(Action):

    def name(self) -> Text:
        return "ask_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open("data/movieSchedule.json", "r") as MS:
            movieSchedule = json.load(MS)
        dateList = []
        buttons = []
        dateList = movieSchedule.keys()
        today = datetime.now().strftime("%d-%m-%Y")
        today = datetime.strptime(today,"%d-%m-%Y")
        for i in dateList:
            temp_date = datetime.strptime(i,"%d-%m-%Y")
            if (temp_date < today):
                continue
            else:
                payload = str(i)
                buttons.append(
                {"title": "{}".format(i), "payload": payload})

        message = "Please select a date"
        dispatcher.utter_button_message(message, buttons)

        return []

class AskChoice(Action):

    def name(selfself) -> Text:
        return "ask_movieChoice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = []
        with open("data/movieSchedule.json", "r") as MS:
            movieSchedule = json.load(MS)
        with open("data/movieTime.json", "r") as MT:
            movieTime = json.load(MT)
        movieDate = str(tracker.get_slot("movieDate"))
        today_time = datetime.now().strftime("%I %p")
        today_time = datetime.strptime(today_time,"%I %p")
        today = datetime.now().strftime("%d-%m-%Y")
        for i in movieSchedule[movieDate].keys():
            temp_time = datetime.strptime(movieTime[i],"%I %p")
            if(movieDate == today):
                if( temp_time > today_time):
                    payload = "I choose "+ i
                    buttons.append(
                    {"title": "{}".format(movieSchedule[movieDate][i]), "payload": payload})
            else:
                payload = "I choose " + i
                buttons.append(
                    {"title": "{}".format(movieSchedule[movieDate][i]), "payload": payload})

        message = "Please select a movie"
        dispatcher.utter_button_message(message, buttons)

        return[]


class PrintImdbMovieDetails(Action):

    def name(selfself) -> Text:
        return "print_imdb_movie_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with open("data/movieScreen.json", "r") as MScreen:
            movieScreen = json.load(MScreen)
        with open("data/movieTime.json", "r") as MT:
            movieTime = json.load(MT)
        with open("data/movieSchedule.json", "r") as MS:
            movieSchedule = json.load(MS)
        with open("data/movieDetails.json", "r") as MD:
            movieDetails = json.load(MD)
        buttons = []
        movieDate = tracker.get_slot("movieDate")
        movieChoice = tracker.get_slot("movieChoice")
        movieName = movieSchedule[str(movieDate)][str(movieChoice)]
        message = "Here are the details of the selected movie, if you care ;)\n"
        imdbLink = "https://www.imdb.com/title/"+ movieDetails[str(movieDate)][str(movieChoice)]
        message = message + "View details of " + movieName + " in IMDB\n"
        message = message + imdbLink
        dispatcher.utter_message(message)
        return[]

class SlotDisplay(Action):

    def name(selfself) -> Text:
        return "slot_display"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movieDate = tracker.get_slot("movieDate")
        movieChoice = tracker.get_slot("movieChoice")
        noTickets = tracker.get_slot("noTickets")
        with open("data/movieSchedule.json", "r") as MS:
            movieSchedule = json.load(MS)
        with open("data/movieSeatMap.json", "r") as SM:
            movieSeatMap = json.load(SM)
        # movieSeatMap = movieSeatMap[str(movieDate)][str(movieChoice)]
        reply = ""
        img = Image.new('RGB', (500, 525), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        r = 5
        c = 25
        for i in movieSeatMap[str(movieDate)][str(movieChoice)].keys():
            for j in movieSeatMap[str(movieDate)][str(movieChoice)][i].keys():
                if j == str(9):
                    c = c + 50
                    reply = ""
                    d.text((c, r), reply, fill=(255, 255, 0))
                if movieSeatMap[str(movieDate)][str(movieChoice)][i][j] == "1":
                    reply = str.upper(str(i + j))
                    d.text((c, r), reply, fill=(255, 255, 0))
                    c = c + 25
                else:
                    reply = "(X)"
                    d.text((c, r), reply, fill=(255, 0, 0))
                    c = c + 25

            reply = reply + "\n  "
            r = r + 30
            c = 25

        r = r + 20
        c = 175
        reply = "------- SCREEN -------"
        d.text((c, r), reply, fill=(0, 0, 0))
        imgName = "data/available_seats-" + datetime.now().strftime("%H%M") + ".png"
        img.save(imgName)
        imgURL = "http://localhost:7000/" + imgName
        text = "(X) represents that those seats are booked and are not available,Please select only " + str(noTickets) + " seats."
        text = text + "\n Please input your seat selection with a comma separating each seat like in the example,\nEx: a2,b7,c8"
        dispatcher.utter_message(image=imgURL)
        dispatcher.utter_message(text=text)
        return[]

class SlotCheck(Action):

    def name(selfself) -> Text:
        return "slot_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movieDate = tracker.get_slot("movieDate")
        movieChoice = tracker.get_slot("movieChoice")
        noTickets = tracker.get_slot("noTickets")
        with open("data/movieSchedule.json", "r") as MS:
            movieSchedule = json.load(MS)
        with open("data/movieSeatMap.json", "r") as SM:
            movieSeatMap = json.load(SM)
        movieSeatMap = movieSeatMap[str(movieDate)][str(movieChoice)]
        message = str((tracker.latest_message)['text'])
        seats = str(message).split(",")
        newSeats = []
        flag = 0
        for i in range(len(seats)):
            for i1 in range(len(seats)):
                if i != i1:
                    if seats[i] == seats[i1]:
                        flag = 1
        if(flag == 1):
            msg = "Invalid Seat selection detected !"
            dispatcher.utter_message(msg)
            return[FollowupAction("slot_display")]
        if (str(len(seats)) != str(noTickets)):
            msg = "Please select only  ", str(noTickets), " seats..."
            dispatcher.utter_message(msg)
            return[FollowupAction("slot_display")]
        else:
            newSeats = seats
        seatCount = 0
        for seat in newSeats:
            i = seat[0]
            j = seat[1:]
            try:
                if ((movieSeatMap[str(i)][str(j)]) == "1"):
                    seatCount = seatCount + 1
                else:
                    seatCount = seatCount + 0
            except:
                msg = "Invalid Seat selection detected !"
                dispatcher.utter_message(msg)
                return [FollowupAction("slot_display")]
        if(seatCount == int(noTickets)):
            return[FollowupAction("utter_seat_confirmation")]
        else:
            dispatcher.utter_message("One or More seats are booked.Please re-enter your selection!")
            return[FollowupAction("slot_display")]

class PersonalDetailsCheck(Action):

    def name(self):
        return "personal_details_check"


    def run(self,dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any],) -> List[Dict]:

        pdEmail = tracker.get_slot("pdEmail")
        pdNumber = tracker.get_slot("pdNumber")
        if "@" not in str(pdEmail):
            dispatcher.utter_message("Please enter a valid Email address")
            return [FollowupAction("utter_ask_pdEmail")]
        if (len(pdNumber) != 10):
            dispatcher.utter_message("Please enter a valid 10 digit phone number")
            return [FollowupAction("utter_ask_pdNumber")]
        message = ""
        movieChoice = tracker.get_slot("movieChoice")
        noTickets = tracker.get_slot("noTickets")
        movieDate = tracker.get_slot("movieDate")
        seats = tracker.get_slot("seats")
        with open("data/movieSchedule.json", "r") as MS:
            movieSchedule = json.load(MS)
        with open("data/movieScreen.json", "r") as MScreen:
            movieScreen = json.load(MScreen)
        with open("data/movieTime.json", "r") as MT:
            movieTime = json.load(MT)
        movieName = movieSchedule[str(movieDate)][str(movieChoice)]
        message = "SOKKALINGAM MOVIES PVT LTD.\nDubai Main Rd,\nDubai\n\nTICKET DETAILS :\n"
        message += "Movie : " + str(movieName) + "\nShow Date : " + str(movieDate)
        message += "\nShow time : " + str(movieTime[str(movieChoice)])
        message += "\nScreen : " + str(movieScreen[str(movieChoice)]) + "\nNo. of Tickets : " + str(noTickets)
        message += "\nSeats : " + str.upper(seats) + "\nTotal Amount : Rs." + str(int(noTickets)*250) +"/-\n"
        pdName = tracker.get_slot("pdName")
        pdEmail = tracker.get_slot("pdEmail")
        pdNumber = tracker.get_slot("pdNumber")
        message += "\nPERSONAL DETAILS : \nName : " + str(pdName) +"\nEmail address : " + str(pdEmail)
        message += "\nPhone Number : "+ str(pdNumber)
        dispatcher.utter_message(message)
        return [SlotSet("ticketDetails", message)]

class TicketGeneration(Action):

    def name(self) -> Text:
        return "ticket_generation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ticket_details = tracker.get_slot("ticketDetails")
        movieDate = tracker.get_slot("movieDate")
        movieChoice = tracker.get_slot("movieChoice")
        seats = str(tracker.get_slot("seats")).split(",")

        ticketID = "SLM-" + str(random.choice(range(1000,10000)))

        with open("data/movieSeatMap.json", "r") as SM:
            movieSeatMap = json.load(SM)
        for seat in seats:
            i = seat[0]
            j = seat[1:]
            movieSeatMap[str(movieDate)][str(movieChoice)][str(i)][str(j)] = "0"

        with open("data/movieSeatMap.json", "w") as SMw:
            json.dump(movieSeatMap,SMw)

        ticket_details = ticket_details + "\n\nTICKET ID : " + ticketID

        qrData = pyqrcode.create(ticket_details)
        ticketHistory = {}
        ticketHistory[ticketID] = str(ticket_details)
        with open("data/tickets/ticketHistory.json", "w") as outfile:
            json.dump(ticketHistory, outfile)

        ticket_file = "data/tickets/" + ticketID + ".png"
        qrData.png(ticket_file, scale=6)
        imgURL = "http://localhost:7000/" + ticket_file
        dispatcher.utter_message(image=imgURL)
        mesg = "TICKET ID : " + ticketID
        dispatcher.utter_message(mesg)
        dispatcher.utter_message("Your tickets have been booked successfully!\nSave the QRCode for easy check-in at the theatre\nPlease remember your TICKET ID in case of further reference")
        return []

    class HandlePayment(Action):

        def name(self) -> Text:
            return "handle_payment"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dispatcher.utter_message("We are happy to announce that we are giving away tickets that are booked through our chatBot as a token of thanks for using our ChatBot.")

            return [SlotSet("payment_flag", True)]

    class TicketRetrieval(Action):

        def name(self) -> Text:
            return "ticket_retrieval"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            ticketID = tracker.get_slot("ticketID")
            with open("data/tickets/ticketHistory.json", "r") as ticketfile:
                tickets = json.load(ticketfile)
            ticketID = "SLM-" + ticketID
            if(ticketID in tickets.keys()):
                dispatcher.utter_message("Ticket Found!")
                qrData = pyqrcode.create(tickets[ticketID])
                ticket_file = "data/tickets/" + ticketID + ".png"
                qrData.png(ticket_file, scale=6)
                imgURL = "http://localhost:7000/" + ticket_file
                dispatcher.utter_message(image=imgURL)
                mesg = "TICKET ID : " + ticketID
                dispatcher.utter_message(mesg)
            else:
                dispatcher.utter_message("Sorry! I could not find any ticket with the given Ticket ID")
            return []