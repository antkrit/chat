$('#joinModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget),
        title = button.data('title'),
        descr = button.data('descr'),
        href = button.data('href'),
        modal = $(this)

    modal.find('#modal-chat-name').text(title);
    modal.find('#modal-chat-descr').html(descr);
    modal.find('#enter-chat-form').attr('action', href);
});
