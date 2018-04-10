( function($) {

    function login_req() {
      var email = $('#login_email').val()
      var passwd = $('#login_password').val()
      $.ajax({
        method: "POST",
        url: '/login/',
        data: {
            'email': email,
            'password': passwd
        },
        success: function(data){
          if (data == 200) {
            location.href = '/marketsignal'
          } else if (data == 400) {
            var msg = '아이디/비밀번호를 다시 확인해주세요'
            $('#msg-area').text(msg)
            $('#login_email').val('')
            $('#login_password').val('')
            $('#login_email').focus()
          }

        },
        error: function(data){
          console.log(data.status)
        }
      })
    }

      function register_req() {
        // clear data
        $('#register_email').val('')
        $('#register_password').val('')
        $('#register_password_check').val('')
        $('#phone_check').val('')
      }


    function chkPwd(str){
     var pw = str;
     var num = pw.search(/[0-9]/g);
     var eng = pw.search(/[a-z]/ig);
     var spe = pw.search(/[`~!@@#$%^&*|₩₩₩'₩";:₩/?]/gi);

     if(pw.length < 6){
        $('#msg-pwd-invalid').text("6자 이상 입력해주세요.")
        return false;
      }else if (pw.search(/₩s/) != -1){
        $('#msg-pwd-invalid').text("비밀번호는 공백없이 입력해주세요.")
        return false;
      }else if (spe == -1 ){
        $('#msg-pwd-invalid').text("특수문자를 포함하여 입력해주세요.")
          return false;
      }else{
        $('#msg-pwd-invalid').text("")
        return true;
      }

   }

   function chkPhone(str){
    var phone_num = str;
    var num = phone_num.search(/[0-9]/g);
    var eng = phone_num.search(/[a-z]/ig);
    var spe = phone_num.search(/[`~!@@#$%^&*|₩₩₩'₩";:₩/?]/gi);

    if(eng != -1 || spe != -1){
     $('#msg-phone-invalid').text("전화번호에 숫자만 적어주세요.")
       return false;
     }else if (phone_num.length <= 0){
       $('#msg-phone-invalid').text("번호를 입력해주세요.")
       return false;
     }else{
       $('#msg-phone-invalid').text("")
       return true;
     }
  }

    // check validation of password email
    function ValidateEmail(mail){
      var regExp = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;
      if (regExp.test(mail) && mail.length < 100){
        return true
      }else{
        return false
      }
    }






    $(document).on('click', '#login_btn', function () {
        login_req()
    })

    $(document).on('keydown', '#login_password', function (e) {
        if (e.keyCode == 13) {
          login_req()
        }
    })


    //when click '새로운 비밀번호 설정' btn in password popwup
    $(document).on('click', '#password_email_check', function () {
      var email_valid = true;

      if(ValidateEmail($('#password_email').val())){
        $('#msg-password-change').text('비밀번호 변경을 위한 url이 전송되었습니다!')
        email_valid = true;
      }else{
        $('#msg-password-change').text('이메일 형식이 옳지 않습니다. 다시 입력해 주세요.')
        $('#password_email').val('')
        email_valid = false;
      }

      if(email_valid){
        setTimeout(function () {
          location.href = '/'
        }, 1000); // move to main home after 1.0 sec
      }

    })


    //register
    $(document).on('click', '#register_email_check', function () {
      var register = true;
      var msg_not_duplicate= '확인되었습니다!';
      var msg_duplicate = '중복된 이메일 입니다!';

      if (1) {
        $('#duplicate-email-check').text(msg_not_duplicate)
      }else{
        $('#duplicate-email-check').text(msg_duplicate)
      }
    })


    // sign up button implementation
    $(document).on('click', '#register_login_btn', function () {
        register = true;

        //check length and special char of passwoer
        if(!chkPwd( $.trim($('#register_password').val()))) {
          register = false;
        }

        //check password and password_check are equal
        if($.trim($('#register_password').val()) != $.trim($('#register_password_check').val())){
          $("#msg-pwd-confirm").text("패스워드가 다릅니다.");
          register = false;
        }

        //check phone vaildation
        if(!chkPhone($.trim($('#phone_check').val()))){
          register = false;
        }

        // sign up when register variable is true
        //if (register == true){
          register_req()
        //}

    })




})(jQuery);
