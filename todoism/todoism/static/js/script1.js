$(document).ready(function () {
    var ENTER_KEY = 13;
    var ESC_KEY = 27;

    //ajax错误统一接收函数
    $(document).ajaxError(function (event, request) {
        var message = null;

        if (request.responseJSON && request.responseJSON.hashOwnProperty('message')){
            message = request.responseJSON.message;
        } else if (request.responseText) {
            var IS_JSON = true;
            try {
                var data = JSON.parse(request.responseText);
            }
            catch (err) {
                IS_JSON = false;
            }

            if (IS_JSON && data !== undefined && data.hasOwnProperty('message')){
                message = JSON.parse(request.responseText).message;
            } else {
                message = default_error_message;
            }
        } else {
            message = default_error_message;
        }
        M.toast({html:message})
    });


    //设置csrf
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token)
            }
        }
    });


    //绑定一个回调函数，在url发生变化时，根据#后的内容执行
   $(window).bind('hashchange', function () {
       //有的浏览器不返回#，所以统一去掉#
       var hash = window.location.hash.replace('#', '');
       var url = null;
       if (hash === 'login') {
           url = login_page_url      //这些变量定义在index.html
       } else if (hash === 'app') {
           url = app_page_url
       } else {
           url = intro_page_url
       }

       $.ajax({
           type: 'GET',
           url: url,
           success: function (data) {
               $('#main').hide().html(data).fadeIn(800);
               activeM();   //激活新插入的页面中的materialize组件
           }
       });
   });


   if (window.location.hash === '') {
       window.location.hash = '#intro'; //主页跳转到默认页面
   } else {
       $(window).trigger('hashchange'); //出发hashchange，重新加载页面
   }


   function display_dashboard() {
       var all_count = $('.item').length;
       if (all_count === 0) {
           $('#dashboard').hide();
       } else {
           $('#dashboard').show();
           $('ul.tabs').tabs()
       }
   }


   function activeM() {
       $('.sidenv').sidenav();
       $('ul.tabs').tabs();
       $('.modal').modal();
       $('.tooltipped').tooltip();
       $('.dropdown-trigger').dropdown({
           constrainWidth: false,
           coverTrigger: false
       });
       display_dashboard()
   }


       //刷新条数
    function refresh_count() {
        var $items = $('.item');

        display_dashboard();
        var all_count = $items.length;
        var active_count = $items.filter(function(){
            return $(this).data('done') === false;
        }).length;
        var completed_count = $items.filter(function(){
            return $(this).data('done') === true;
        }).length;
        $('#all-count').html(all_count);
        $('#active-count').html(active_count);
        $('#active-count-nav').html(active_count);
        $('#completed-count').html(completed_count);
    }


    function remove_edit_input() {
        var $edit_input = $('#edit-item-input');
        var $input = $('#item-input');

        $edit_input.parent().prev().show();
        $edit_input.parent().remove();
        $input.focus();
    }


   //获取虚拟账户信息
    function register() {
        $.ajax({
            type: 'GET',
            url: register_url,
            success: function (data) {
                $('#username-input').val(data.username);
                $('#password-input').val(data.password);
                M.toast({html:data.message})
            }
        });
    }

    $(document).on('click', '#register-btn', register);


   //login_user登陆
    function login_user() {
        var username = $('#username-input').val();
        var password = $('#password-input').val();

        if (!username || !password) {
            M.toast({html:login_error_message});
            return;
        }

        var data = {
            'username':username,
            'password':password
        };
        $.ajax({
            type:'POST',
            url: login_url,
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            success:function (data) {
                if (window.location.hash === '#app' ||window.location.hash === 'app'){
                    $(window).trigger('hashchange');
                } else {
                    window.location.hash = '#app'
                }
                activeM();
                M.toast({html:data.message})
            }
        })
    }


   //登陆
   $('.login-input').on('keyup', function (e) {
       if (e.which === ENTER_KEY) {
           login_user();
       }
   });

   $(document).on('click', '#login-btn', login_user);


   //使密码可见
   function toggle_password() {
       var password_input = document.getElementById('password-input');
       if (password_input.type === 'password') {
           password_input.type = 'text';
       } else {
           password_input.type = 'password';
       }
   }

   $(document).on('click', '#toggle-password', toggle_password);


    //登出
   $(document).on('click', '#logout-btn', function () {
       $.ajax({
           type:'GET',
           url: logout_url,
           success: function (data) {
               window.location.hash = "#intro";
               activeM();
               M.toast({html: data.message})
           }
       })
   });


    //创建新条目
    function new_item(e) {
        var $input = $('#item-input');
        var value = $input.val().trim();   // 获取输入值
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $input.focus().val('');    // 聚焦到输入框并清空内容
        $.ajax({
            type: 'POST',
            url: new_item_url,
            data: JSON.stringify({'body': value}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                M.toast({html: data.message, classes: 'rounded'});
                $('.items').append(data.html);
                activeM();
                refresh_count();
            }
        });
    }

    $(document).on('keyup', '#item-input', new_item.bind(this));


    //编辑条目
    function edit_item(e) {
        var $edit_input = $('#edit-item-input');
        var value = $edit_input.val().trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $edit_input.val('');

        if (!value) {
            M.toast({html: empty_body_error_message});
            return;
        }

        var url = $edit_input.parent().prev().data('href');
        var id = $edit_input.parent().prev().data('id');

        $.ajax({
            type: 'PUT',
            url: url,
            data: JSON.stringify({'body': value}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                $('#body' + id).html(value);
                $edit_input.parent().prev().data('body', value);
                remove_edit_input();
                M.toast({html: data.message});
            }
        })
    }

    $(document).on('keyup', '#edit-item-input', edit_item.bind(this));


    $(document).on('click', '.done-btn', function () {
        var $input = $('#item-input');

        $input.focus();
        var $item = $(this).parent().parent();
        var $this = $(this);

        if ($item.data('done')) {
            $.ajax({
                type: 'PATCH',
                url: $this.data('href'),
                success: function (data) {
                    $this.next().removeClass('inactive-item');
                    $this.next().addClass('active-item');
                    $this.find('i').text('check_box_outline_blank');
                    $item.data('done', false);
                    M.toast({html:data.message});
                    refresh_count();
                }
            })
        } else {
            $.ajax({
                type: 'PATCH',
                url: $this.data('href'),
                success: function (data) {
                    $this.next().removeClass('active-item');
                    $this.next().addClass('inactive-item');
                    $this.find('i').text('check_box');
                    $item.data('done', true);
                    M.toast({html: data.message});
                    refresh_count();
                }
            })
        }
    });


    $(document).on('mouseenter', '.item', function () {
        $(this).find('.edit-btns').removeClass('hide');
    })
        .on('mouseleave', '.item', function () {
            $(this).find('.edit-btns').addClass('hide');
        });


    $(document).on('click', '.edit-btn', function () {
        var $item = $(this).parent().parent();
        var itemId = $item.data('id');
        var itemBody = $('#body' + itemId).text();
        $item.hide();
        $item.after(' \
                <div class="row card-panel hoverable">\
                <input class="validate" id="edit-item-input" type="text" value="' + itemBody + '"\
                autocomplete="off" autofocus required> \
                </div> \
            ');

        var $edit_input = $('#edit-item-input');
        // Focus at the end of input text.
        // Multiply by 2 to ensure the cursor always ends up at the end;
        // Opera sometimes sees a carriage return as 2 characters.
        var strLength = $edit_input.val().length * 2;

        $(document).on('keydown', function (e) {
            if (e.keyCode === ESC_KEY) {
                remove_edit_input();
            }
        });

         $edit_input.on('focusout', function () {
            remove_edit_input();
        })
    });


    $(document).on('click', '.delete-btn', function () {
        var $input = $('#item-input');
        var $item = $(this).parent().parent();

        $input.focus();
        $.ajax({
            type: 'DELETE',
            url: $(this).data('href'),
            success: function (data) {
                $item.remove();
                activeM();
                refresh_count();
                M.toast({html: data.message});
            }
        });
    });


    $(document).on('click', '#active-item', function() {
        var $input = $('item-input');
        var $items = $('.item');

        $input.focus();
        $items.show();
        $items.filter(function () {
            return $(this).data('done');
        }).hide();
    });


    $(document).on('click', '#completed-item', function () {
        var $input = $('#item-input');
        var $items = $('.item');

        $input.focus();
        $items.show();
        $items.filter(function () {
            return !$(this).data('done');
        }).hide();
    });


    $(document).on('click', '#all-item', function () {
        $('#item-input').focus();
        $('.item').show();
    });



     $(document).on('click', '#clear-btn', function () {
        var $input = $('#item-input');
        var $items = $('.item');

        $input.focus();
        $.ajax({
            type: 'DELETE',
            url: clear_item_url,
            success: function (data) {
                $items.filter(function () {
                    return $(this).data('done');
                }).remove();
                M.toast({html: data.message, classes: 'rounded'});
                refresh_count();
            }
        });
    });


     //语言切换
    $(document).on('click', '.lang-btn', function () {
        $.ajax({
            type: 'GET',
            url: $(this).data('href'),
            success: function (data) {
                $(window).trigger('hashchange');
                activeM();
                M.toast({html:data.message});
            }
        })
    })
    activeM() // initialize Materialize
})

