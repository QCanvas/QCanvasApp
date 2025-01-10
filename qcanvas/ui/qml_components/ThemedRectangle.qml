import QtQuick

Rectangle {
    property Palette theme: getTheme()

    function getTheme() {
        if (appTheme.theme === "native")
            return palette
        else if (appTheme.dark_mode === true)
            return darkTheme
        else
            return lightTheme
    }

    LightTheme {
        id: lightTheme
    }
    DarkTheme {
        id: darkTheme
    }

    Connections {
        target: appTheme

        function onThemeChanged() {
            updateTheme()
        }

        function onDarkModeChanged() {
            updateTheme()
        }

        function updateTheme() {
            theme = getTheme()
        }
    }
}
