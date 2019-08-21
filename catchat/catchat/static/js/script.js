$(document).ready(function () {
    // var socket = io.connect();
    var ENTER_KEY = 13;
    var popupLoading = '<i class="notched circle loading icon green"></i> Loading...';

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain){
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    function scrollToBottom() {
        var $messages = $('.messages');
        $messages.scrollTop($messages[0].scrollHeight);
    }
    
    function activateSemantics() {
        $('.ui.dropdown').dropdown();
        $('.ui.checkbox').checkbox();

        $('.message .close').on('click', function () {
            $(this).closest('.message').transition('fade');
        });

        $('#toggle-sidebar').on('click', function () {
            $('.menu.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
        });

        $('.pop-card').popup({
            inline: true,
            on: 'hover',
            hoverable: true,
            html: popupLoading,
            delay: {
                show:200,
                hide:200
            },
            onShow: function () {
                var popup = this;
                popup.html(popupLoading);
                $.get({
                    url: $(popup).prev().data('href')
                }).done(function (data) {
                    popup.html(data);
                }).fail(function () {
                    popup.html('Failed to load profile');
                });
            }
        });
    }

    function new_message(e) {
        var $textarea = $('#message-textarea');
        var message_body = $textarea.val().trim();
        if (e.which === ENTER_KEY && !e.shiftKey && message_body) {
            e.preventDefault();       //阻止默认行为，即换行
            socket.emit('new message', message_body);
            $textarea.val('')
        }
    }
    $('#message-textarea').on('keydown', new_message.bind(this));


    socket.on('new message', function(data) {
        console.log(data.message_html)
        $('.messages').append(data.message_html);  // 插入新消息到页面
        flask_moment_render_all();  // 渲染消息中的时间戳
        scrollToBottom();  // 进度条滚动到底部
        activateSemantics();  // 激活Senmatic-ui组件
    });

    socket.on('user count', function (data) {
        $('#user-count').html(data.count)
    });


    //输入模态框
    $("#message-textarea").focus(function () {
        if (screen.width < 600) {
            $('#mobile-new-message-modal').modal('show');
            $('#mobile-message-textarea').focus()
        }
    });

    $('#send-button').on('click', function () {
        var $mobile_textarea = $('#mobile-message-textarea');
        var message = $mobile_textarea.val();
        if (message.trim() !== ''){
            socket.emit('new message', message);
            $mobile_textarea.val('')
        }
    });


    var page = 1;
    function load_messages() {
        var $messages = $('.messages');
        var position = $messages.scrollTop();
        if (position === 0 && socket.nsp !== '/anonymous') {
            page++;
            $('.ui.loader').toggleClass('active');
            $.ajax({
                url:messages_url,
                type:'GET',
                data:{page:page},
                success:function (data) {
                    var before_height = $messages[0].scrollHeight;
                    $(data).prependTo(".messages").hide().fadeIn(800); //插入消息
                    var after_height = $messages[0].scrollHeight;
                    flask_moment_render_all();      //渲染时间
                    $messages.scrollTop(after_height - before_height);
                    $('.ui.loader').toggleClass('active');
                    activateSemantics();
                },
                error: function () {
                    alert('已经到头了，没有更多了');
                    $('.ui.loader').toggleClass('active');
                }
            })
        }
    }

    $('.messages').scroll(load_messages);

    function init() {
        activateSemantics();
        scrollToBottom();
    }

    init();
})