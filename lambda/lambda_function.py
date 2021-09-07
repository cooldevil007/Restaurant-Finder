# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

import logging
from ask_sdk_core.dispatch_components.request_components import AbstractRequestInterceptor, AbstractResponseInterceptor

from ask_sdk_core.skill_builder import CustomSkillBuilder, SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import AskForPermissionsConsentCard
from ask_sdk_core.api_client import DefaultApiClient

import requests
import pprint

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PERMISSIONS = ["alexa::devices:all:geolocation:read"]
ACCURACY_THRESHOLD = 100
# Add Google API Key here to access Google API.
API_KEY = ""
Restaurant_names = []
# Base URL of endpoint

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Restaurant Finder. Here you can say 'find restaurant' to find nearby restaurant."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("You can say 'find restaurant' to find out nearby restaurant")
                .response
        )

class FindRestaurantIntentHandler(AbstractRequestHandler):
    """Handler for Place API Intent"""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("FindRestaurantIntent")(handler_input)

    def handle(self, handler_input):
        # Check whether request support geolocation interface. Geolocation object will be added in request if user invoke skill using Alexa app in mobile device.
        is_geo_supported = handler_input.request_envelope.context.system.device.supported_interfaces.geolocation

        if is_geo_supported:
            # Get geolocation object which contains user co-ordinate once permission granted.
            geo_object = handler_input.request_envelope.context.geolocation
            pprint.pprint(geo_object)

            if not (geo_object or geo_object.coordinate):
                skill_permission_granted = handler_input.request_envelope.context.system.user.permissions.scopes.status == 'GRANTED'
                # If permission not granted send Alexa permission card for user in Alexa app to grant permission.
                if not (skill_permission_granted):
                    return handler_input.response_builder.speak("Restaurant Finder would like to use your location. To turn on location sharing, please go to your Alexa app, and follow the instructions.").set_card(AskForPermissionsConsentCard(permissions=PERMISSIONS)).response
                else:
                    # Location service should be "Running" and "Enabled".
                    if not (geo_object.location_services.status == 'RUNNING'):
                        return handler_input.response_builder.speak("Restaurant Finder is having trouble accessing your location. Please wait a moment, and try again later.").response
                    if not (geo_object.location_services.access == 'ENABLED'):
                        return handler_input.response_builder.speak("Please make sure device location tracking is enabled in your device.").response
                    else:
                        return handler_input.response_builder.speak("There was an error accessing your location. Please try again later.").response

            # Check user Geo-co-ordinate and accuracy less than 100 meters.
            if (geo_object and geo_object.coordinate and geo_object.coordinate.accuracy_in_meters < ACCURACY_THRESHOLD):
                # Retrieve Latitude & Longitude co-ordinate.
                latitude = geo_object.coordinate.latitude_in_degrees
                longitude = geo_object.coordinate.longitude_in_degrees
                location_data = str(latitude) + "," + str(longitude)
                
                 # Call Google Map "Place NearBy" service with location , radius within 4 KM, currently open and of type restaurant.
                response_data = requests.get(url + "location="+ location_data + "&radius=4000&type=restaurant" + "&key=" + API_KEY)
                result_data = response_data.json()["results"]
                if len(result_data)>=3:
                    restaurant_name1 = result_data[0]["name"]
                    restaurant_name2 = result_data[1]["name"]
                    restaurant_name3 = result_data[2]["name"]

                    speak_output = "Top three restaurant near your location are {}, {} and {}".format(restaurant_name1 , restaurant_name2, restaurant_name3)  

                    return (
                        # Remove any special character if present
                        handler_input.response_builder.speak(speak_output.replace("&", "")).response
                    )

                elif len(result_data)==2: 
                    restaurant_name1 = result_data[0]["name"]
                    restaurant_name2 = result_data[1]["name"]

                    speak_output = "Top two restaurant near your location are {} and {}".format(restaurant_name1 , restaurant_name2)

                    return (
                        # Remove any special character if present
                        handler_input.response_builder.speak(speak_output.replace("&", "")).response
                    )

                elif len(result_data)==1:
                    restaurant_name1 = result_data[0]["name"]

                    speak_output = "Top restaurant near your location are {}".format(restaurant_name1)

                    return (
                        # Remove any special character if present
                        handler_input.response_builder.speak(speak_output.replace("&", "")).response
                    )
                else:
                    
                    return(
                        handler_input.response_builder.speak("We didn't find any restaurant near to your location. Please try again later.").response
                    )

        return (
            handler_input.response_builder.speak("Please use Alexa app to use this skill.").response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say 'find restaurant' to find top three restaurant near me! How can I help?"

        return (
            handler_input.response_builder.speak(speak_output).ask(speak_output).response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder.speak(speak_output).response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder.speak(speak_output).response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder.speak(speak_output).ask(speak_output).response
        )

class LoggingRequestInterceptor(AbstractRequestInterceptor):
    """ Log the request envelope. """

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Received : {}".format(handler_input.request_envelope))


class LoggingResponseInterceptor(AbstractResponseInterceptor):
    """ Log the response envelope """

    def process(self, handler_input, response):
        logger.info("Response generated: {}".format(response))


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = CustomSkillBuilder(api_client=DefaultApiClient())

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(FindRestaurantIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

# Adding Request and response interceptor
sb.add_global_request_interceptor(LoggingRequestInterceptor())
sb.add_global_response_interceptor(LoggingResponseInterceptor())

lambda_handler = sb.lambda_handler()
