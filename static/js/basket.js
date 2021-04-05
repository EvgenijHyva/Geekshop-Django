window.onload = function () {
    $(".basket_list").on("click", "input[type=number]", function(){
        var t_href = event.target;
        console.log(t_href);
        $.ajax({
            url: "/baskets/edit/" + t_href.name + "/" + t_href.value + "/",
            success: function(data) { // тоесть отправятся данные по адресу, и получим данные с контроллера
            $(".basket_list").html(data.result) // которые нужно поставить на место basket_list
            // другими словами basket_list замени на html, который передается в data, и после обращаемся к result
            }
        });
        event.preventDefault();
    });
};