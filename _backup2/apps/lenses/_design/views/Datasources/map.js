 
function(doc) {
    if (doc.doc_type == 'Datasource'){
        emit(doc._id, doc);
    }
}