#  Build An Alexa Restaurant Finder Skill 🇺🇸
<img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/quiz-game/header._TTH_.png" />

This sample skill showcase how to find nearby restaurant using Alexa [Geo-Location](https://developer.amazon.com/en-US/docs/alexa/custom-skills/location-services-for-alexa-skills.html) with [Google Place API](https://developers.google.com/maps/documentation/places/web-service/overview).

## Skill Architecture
Each skill consists of two basic parts, a front end and a back end.
The front end is the voice interface, or VUI.
The voice interface is configured through the voice interaction model.
The back end is where the logic of your skill resides.

## Three Options for Skill Setup
There are a number of different ways for you to setup your skill, depending on your experience and what tools you have available.

 * If this is your first skill, choose the [Alexa-Hosted](https://developer.amazon.com/en-US/docs/alexa/hosted-skills/build-a-skill-end-to-end-using-an-alexa-hosted-skill.html) to get started quickly.
 * If you want to manage the backend resources in your own AWS account, you can follow the [AWS-Hosted instructions](https://developer.amazon.com/en-US/docs/alexa/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html).
 * Developers with the ASK Command Line Interface configured may follow the [ASK CLI](https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html).

---

## Setup to run this demo
### How to create Google API key to access Google Place API

* Create Google Developer account and setup account by providing billing details. Remember to select "Google Map Service" and not "Google Cloud service" as billing service.
* Create Google project and Enabled "Google Place" API.
* Generate API Key which will be needed in skill backend code.

### Install "Google Maps" python library

* Add "googlemaps" library in requirements.txt file to be downloaded after deployment like below:
```
  googlemaps>=4.5.3
```

OR

* Run PIP to install "googlemaps" library.
```
    $ pip install -U googlemaps
```
### API documentation & Resources

- [Get Started with Google Maps Platform](https://developers.google.com/maps/gmp-get-started)
- [Generating/restricting an API key](https://developers.google.com/maps/gmp-get-started#api-key)
- [Places API](https://developers.google.com/places/)
- [Alexa Geo-Location SDK Library](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/models/ask_sdk_model.interfaces.geolocation.html)



