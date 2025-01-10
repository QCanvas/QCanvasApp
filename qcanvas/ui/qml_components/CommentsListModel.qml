import QtQuick

ListModel {
    ListElement {
        body: "This is a comment. Gaze at it. Be amazed."
        author: "I am Steve"
        date: "2001-01-01 36:00"
        attachments: [
            ListElement {
                file_name: "texas.pdf"
                resource_id: "1"
                download_state: "NOT_DOWNLOADED"
            },
            ListElement {
                file_name: "oh_no_what_a_terribly_long_file_name_its_not_like_someone_would_actually_do_this.pdf"
                resource_id: "2"
                download_state: "FAILED"
            },
            ListElement {
                file_name: "i was transported to another world where javascript doesn't exist.cbz"
                resource_id: "3"
                download_state: "DOWNLOADED"
            }
        ]
    }
    ListElement {
        body: "If Morbius has a million fans, I am one of them.\nIf Morbius has 5 fans, I am one of them.\nIf Morbius has one fan, That one is me.\nIf Morbius has no fans, I am no longer alive.\nIf the world is against Morbius, I am against the world.\nTill my last breath, I'll love Morbius (2022)."
        author: "Goku"
        date: "1942-16-34 06:63"
        attachments: [
            ListElement {
                file_name: "morbius_x264_1080.mkv"
                resource_id: "blahblah"
                download_state: "NOT_DOWNLOADED"
            }
        ]
    }
    ListElement {
        body: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
        author: "Word Wrap Test"
        date: "2000-02-02"
        attachments: []
    }
    ListElement {
        body: "x264 forms the core of many web video services, such as Youtube, Facebook, Vimeo, and Hulu. It is widely used by television broadcasters and ISPs."
        author: "BideoJAN Wordsblahblah"
        date: "2027-07-28"
        attachments: [
            ListElement {
                file_name: "Ass1_SOMEDUDE_48.pdf"
                resource_id: "blah_v345"
                download_state: "DOWNLOADED"
            }
        ]
    }
}
