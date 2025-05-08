## RADAR-Questionnaire

This application is used to carry out questionnaires in various areas of health. In the case of this repository, it is used to collect data and predict the level of social isolation that a person may have.

The application developed by RADAR BASE was used.


### Recommended Package Versions

It is recommended that you install the following versions or later:

```
node v16.13.0
ionic v5.4.16
npm v8.1.0
```

## Install

First install [Node.js](https://nodejs.org/) and [Yarn](https://yarnpkg.com/en/docs/install).

Globally install ionic and cordova:

```
$ npm i -g ionic cordova
```

In the project folder run `npm i` to install dependencies:

```
$ npm i
```

Cordova provides a simple command to install the plugins and platforms set in `package.json` or `config.xml`.

```
$ cordova prepare
```

To run the application in the browser use:

```
$ ionic serve
```

## Guidelines

Use the following command to sort, format and fix common css problems:

```
$ npm run fix:css
```

Use the following command before commiting to fix all common styling and sorting problems:

```
$ npm run fix:all
```

## Platforms

In order to add platforms to target, you must install the required SDKs.

### Android

To add the Android platform, you need to have the [Android SDK](https://developer.android.com/studio/index.html) pre installed. This step also adds the plugins listed in `config.xml` to the project.

```
$ ionic cordova platform add android
```

Run the app in an Android device:

```
$ ionic cordova run android
```

Run the app in an Android emulator:

```
$ ionic cordova emulate android
```

## Firebase

If using Firebase for notifications, analytics, or remote config, [create your Firebase project](https://console.firebase.google.com/). Then, add your iOS or Android app to the Firebase project. Once added, please download the app's `google-services.json` file (for Android) and `GoogleService-Info.plist` (for iOS), and add it to the root directory.

### Package Name

When you add your iOS or Android app to the Firebase project, make sure you name your `package name` as app-id

- Android : `org.phidatalab.radar_armt`
- iOS: `org.phidatalab.radar-armt`


## Questionnaire Input Types

The questionnaire input types supported are `audio`, `checkbox`, `descriptive`, `info-screen`, `matrix-radio`, `radio`, `range-info`, `range-input`, `slider`, `text`, `date`, `time`, and `timed-test`.
