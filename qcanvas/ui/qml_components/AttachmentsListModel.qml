import QtQuick

ListModel {
    ListElement {
        file_name: "texas.pdf"
        resource_id: "1"
        download_state: "NOT_DOWNLOADED"
    }
    ListElement {
        file_name: "oh_no_what_a_terribly_long_file_name_its_not_like_someone_would_actually_do_this.pdf"
        resource_id: "2"
        download_state: "FAILED"
    }
    ListElement {
        file_name: "i was transported to another world where javascript doesn't exist.cbz"
        resource_id: "3"
        download_state: "DOWNLOADED"
    }
}
