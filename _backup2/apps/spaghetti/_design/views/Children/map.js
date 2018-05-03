function(doc) {
    if (doc.parent) {
        emit(doc.parent, doc._id);
    }
}