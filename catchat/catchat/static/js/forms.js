$(document).ready(function () {
    //验证登陆表单
    $('.login.ui.form').form({
        fields:{
            email:{
                identifier: 'email',
                rules:[
                    {
                        type:'empty',
                        prompt: '请填写邮箱'
                    },
                    {
                        type:'email',
                        prompt: '请填写正确的格式'
                    }
                ]
            },
            password:{
                identifier: 'password',
                rules: [
                    {
                        type: 'empty',
                        prompt: '请填写密码'
                    },
                    {
                        type: 'minLength[6]',
                        prompt: '最少6位字符'
                    }
                ]
            }
        }
    });

    //验证注册表单
     $('.register.ui.form')
        .form({
            inline: true,
            fields: {
                nickname: {
                    identifier: 'nickname',
                    rules: [{
                        type: 'empty',
                        prompt: '请填写昵称'
                    },
                        {
                            type: 'maxLength[12]',
                            prompt: '昵称最少{ruleValue}位字符'
                        }
                    ]
                },
                email: {
                    identifier: 'email',
                    rules: [{
                        type: 'empty',
                        prompt: '请填写邮箱'
                    },
                        {
                            type: 'email',
                            prompt: '确保邮箱有效'
                        }
                    ]
                },
                password: {
                    identifier: 'password',
                    rules: [{
                        type: 'empty',
                        prompt: '请填写密码'
                    },
                        {
                            type: 'minLength[6]',
                            prompt: '密码最少{ruleValue}位'
                        }
                    ]
                },
                password2: {
                    identifier: 'password2',
                    rules: [{
                        type: 'empty',
                        prompt: '请填写密码'
                    },
                        {
                            type: 'minLength[6]',
                            prompt: '密码最少{ruleValue}位'
                        },
                        {
                            type: 'match[password]',
                            prompt: '确认两次密码是否一样'
                        }
                    ]
                },

                terms: {
                    identifier: 'terms',
                    rules: [{
                        type: 'checked',
                        prompt: '需要同意条款'
                    }]
                }
            }
        });

    // profile form
    $('.profile.ui.form')
        .form({
            inline: true,
            fields: {
                nickname: {
                    identifier: 'nickname',
                    rules: [{
                        type: 'empty',
                        prompt: '请输入昵称'
                    },
                        {
                            type: 'maxLength[12]',
                            prompt: '昵称最少{ruleValue}位字符'
                        }
                    ]
                },
                github: {
                    identifier: 'github',
                    optional: true,
                    rules: [{
                        type: 'url',
                        prompt: '确定url有效'
                    }]
                },
                website: {
                    identifier: 'website',
                    optional: true,
                    rules: [{
                        type: 'url',
                        prompt: '确定url有效'
                    }]
                },

                bio: {
                    identifier: 'bio',
                    optional: true,
                    rules: [{
                        type: 'maxLength[25]',
                        prompt: '简介最大{ruleValue}个字符'
                    }]
                }
            }
        });
})