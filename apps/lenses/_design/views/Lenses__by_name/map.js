 
function(doc) {
    if (doc.doc_type == 'Lens'){
        for (n in doc.names) {
            emit(doc.names[n], null);
        }
    }
}