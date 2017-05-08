function display_topics(topics, elem) {
    if(topics.length !== 0) {
        $('#temp').text("Some Results. KEEP CALM its still loading.. probably");
        for (i = 0; i < topics.length; i++) {
            let $li = $("<li>", {"class": "list-group-item"});
            let $link = "https://www.reddit.com/r/" + topics[i];
            let $a = $("<a>", {href: $link, target: "_blank"});
            let $h = $("<span>", {text: topics[i], class: "lead"});

            $a.append($h);
            $li.append($a);
            elem.append($li);
        }
        return;
    }

    $('#temp').text("Subreddit does not exist");
}


function finished_loading(l_elem) {
    let $spinner = l_elem;
    if($spinner.length > 0){
        $spinner.remove()
    }
}


function loading() {
    $('#temp').text("KEEP CALM");
    let $div1 = $("<div>", {"class":"loader l_LDA"});
    let $div2 = $("<div>", {"class":"loader l_notLDA"});
    $("#LDA").append($div1)
    $("#notLDA").append($div2)
}


function get_data_LDA(subreddit){
    $.ajax({
        type: "GET",
        url: '/topicsLDA',
        data: {'subreddit':subreddit},
        success: function (response) {
            finished_loading($(".l_LDA"));
            console.log(response);
            display_topics(JSON.parse(response), $(".list2"));
            $('#temp').text("Recommended Results");
        },
        error: function (error) {
            finished_loading($(".l_LDA"));
            console.log(error);
            $('#temp').text("Something went wrong with LDA. Maybe try another subreddit?");
        }
    });
}


function get_data_nonLDA(subreddit){
    $.ajax({
        type: "GET",
        url: '/topics',
        data: {'subreddit':subreddit},
        success: function (response) {
            finished_loading($(".l_notLDA"));
            console.log(response);
            display_topics(JSON.parse(response), $(".list1"));
        },
        error: function (error) {
            finished_loading($(".l_notLDA"));
            console.log(error);
            $('#temp').text("Something went wrong. Maybe try another subreddit?");
        }
    });
}


$('#topics-btn').click(function () {
    $('.list-group').empty();

    let sub = $('#subreddit').val();
    if(sub === ""){
        alert("Empty Search Field");
        return;
    }

    loading();
    console.log("Fetching data with subreddit " + subreddit);
    get_data_nonLDA(sub);
    get_data_LDA(sub);
});
