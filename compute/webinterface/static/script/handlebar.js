var dataframeJSON;
var text;

$(document).ready(function() {

    // so this should enable JavaScript to call on python code, but it doesn't really work (yet).
    $('#regress').click(function() {

        $.ajax({
            type: 'POST',
            url: '../../web_gui.py', // this returns http://127.0.0.1:5000/web_gui.py which is weird haha
            data: { param: text }
        }).done(function (o) {
            console.log(o);
        });
    });
});
