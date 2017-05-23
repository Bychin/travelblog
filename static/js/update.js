$(function () {
    var centrifuge = new Centrifuge({
        "url": "http://localhost:9000/connection/websocket",
        "insecure": true
    });
    centrifuge.subscribe("likes_updates", function(message) {
        handleLikesUpdate(message);
    });
    centrifuge.subscribe("comments_updates", function(message) {
        handleCommentsUpdate(message);
    });
    centrifuge.connect();
});

function handleLikesUpdate(message) {
    console.log(message);
    var itemID = message.data.item;
    var likes = message.data.likes;
    var dislikes = message.data.dislikes;
    var item = $("#item_like"+itemID);
    var number_of_likes = item.find(".likes");
    var number_of_dislikes = item.find(".dislikes");
    number_of_likes.text(likes);
    number_of_dislikes.text(dislikes);
}

function handleCommentsUpdate(message) {
    console.log(message);
    var itemID = message.data.item;
    var text = message.data.text;
    var author = message.data.author;
    var date = message.data.date;
    var likes = message.data.likes;
    var dislikes = message.data.dislikes;

    var item = $("#item_comment"+itemID);
    var number_of_likes = item.find(".likes");
    var number_of_dislikes = item.find(".dislikes");
    var text_in_html = item.find(".text");
    var author_in_html = item.find(".author");
    var date_in_html = item.find(".date");

    number_of_likes.text(likes);
    number_of_dislikes.text(dislikes);
    text_in_html.text(text);
    author_in_html.text(author);
    date_in_html.text(date);
}
