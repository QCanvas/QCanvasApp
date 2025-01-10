import QtQuick

Rectangle {
    id: root
    anchors.fill: parent

    function getTheme() {
        if (appTheme.theme === "native")
            return palette
        else if (appTheme.dark_mode === true)
            return darkTheme
        else
            return lightTheme
    }

    Palette {
        id: lightTheme
        base: "#f8f9fa"
        window: "#f8f9fa"
        midlight: "#f8f9fa"
        accent: "#e02424"
        link: accent
        dark: "#dadce0"
        text: "#4d5157"
    }

    Palette {
        id: darkTheme
        base: "#202124"
        window: "#f8f9fa"
        midlight: "#202124"
        accent: "#e02424"
        link: accent
        dark: "#3f4042"
        text: "#e4e7eb"
    }

    color: getTheme().base

    CommentsList {
        id: commentsList
        anchors.fill: parent
        model: comments
        palette: getTheme()
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
            root.color = getTheme().base
            commentsList.palette = getTheme()
        }
    }
}
