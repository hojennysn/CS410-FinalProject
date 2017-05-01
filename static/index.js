function display_topics(topics) {
    for(i=0; i < topics.length; i++){
        let $li = $("<li>", {"class":"list-group-item"});
        $li.text(topics[i]);
        $(".list-group").append($li);
    }
}


function get_data(subreddit){
    $.ajax({
        type: "GET",
        url: '/topics',
        data: {'subreddit':subreddit},
        success: function (response) {
            console.log(response);
            $('#temp').text("Success?");
            display_topics(JSON.parse(response));
        }
    });
}


$('#topics-btn').click(function () {
    $('.list-group').empty();

    let sub = $('#subreddit').val();
    $('#temp').text(sub);

    get_data(sub);
});
