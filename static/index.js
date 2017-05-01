function display_topics(topics) {
    for(i=0; i < topics.length; i++){
        let $li = $("<li>", {"class":"list-group-item"});
        let $link = "https://www.reddit.com/r/" + topics[i];
        let $a = $("<a>", {text: topics[i], href: $link, target: "_blank"});
        $li.append($a);
        $(".list-group").append($li);
    }
}


function finished_loading() {
    let $spinner = $(".loader");
    if($spinner.length > 0){
        $spinner.remove()
    }
}


function loading() {
    $('#temp').text("loading");
    let $div = $("<div>", {"class":"loader"});
    $(".results").append($div)
}


function get_data(subreddit){
    $.ajax({
        type: "GET",
        url: '/topics',
        data: {'subreddit':subreddit},
        success: function (response) {
            finished_loading();
            console.log(response);
            $('#temp').text("Recommended Results");
            display_topics(JSON.parse(response));
        }
    });
}


$('#topics-btn').click(function () {
    $('.list-group').empty();

    let sub = $('#subreddit').val();
    if(sub === ""){
        alert("Empty Search Field");
        return
    }

    loading();
    get_data(sub);
});
