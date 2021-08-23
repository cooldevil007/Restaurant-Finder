# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

import logging
from os import name
from ask_sdk_core.dispatch_components.request_components import AbstractRequestInterceptor, AbstractResponseInterceptor

from ask_sdk_core.skill_builder import CustomSkillBuilder, SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import AskForPermissionsConsentCard
from ask_sdk_core.api_client import DefaultApiClient

import googlemaps
import pprint

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PERMISSIONS = ["alexa::devices:all:geolocation:read"]
ACCURACY_THRESHOLD = 100
API_KEY = "<Google API>"
Restaurant_names = []

gmaps = googlemaps.Client(key = API_KEY)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Restaurant Finder. Here you can say 'restaurant finder' to find nearby restaurant."

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

        is_geo_supported = handler_input.request_envelope.context.system.device.supported_interfaces.geolocation

        if is_geo_supported:
            geo_object = handler_input.request_envelope.context.geolocation
            pprint.pprint(geo_object)

            if not (geo_object or geo_object.coordinate):
                skill_permission_granted = handler_input.request_envelope.context.system.user.permissions.scopes.status == 'GRANTED'

                if not (skill_permission_granted):
                    return handler_input.response_builder.speak("Restaurant Finder would like to use your location. To turn on location sharing, please go to your Alexa app, and follow the instructions.").set_card(AskForPermissionsConsentCard(permissions=PERMISSIONS)).response
                else:
                    if not (geo_object.location_services.status == 'RUNNING'):
                        return handler_input.response_builder.speak("Restaurant Finder is having trouble accessing your location. Please wait a moment, and try again later.").response
                    if not (geo_object.location_services.access == 'ENABLED'):
                        return handler_input.response_builder.speak("Please make sure device location tracking is enabled in your device.").response
                    else:
                        return handler_input.response_builder.speak("There was an error accessing your location. Please try again later.").response


        if (geo_object and geo_object.coordinate and geo_object.coordinate.accuracy_in_meters < ACCURACY_THRESHOLD):
            latitude = geo_object.coordinate.latitude_in_degrees
            longitude = geo_object.coordinate.longitude_in_degrees
            location_data = str(latitude) + "," + str(longitude)
            place_result = gmaps.places_nearby(location = location_data , radius = 4000, open_now = True, type = 'restaurant')

            for place in place_result['results']:
                my_place_id = place['place_id']

                name_restaurant = ['name']

                restaurant_details = gmaps.place(place_id = my_place_id , fields = name_restaurant)
                Restaurant_names.append(restaurant_details['result'])


        return (
            handler_input.response_builder
                .speak("Top three restaurant near your locations are {}, {} and {} ".format(Restaurant_names[0], Restaurant_names[1], Restaurant_names[2]))
                .response
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
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
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
            handler_input.response_builder
                .speak(speak_output)
                .response
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
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
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
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
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

handler = sb.lambda_handler()
