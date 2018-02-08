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

    $(document).on('click', '#login_btn', function () {
        login_req()
    })

    $(document).on('keydown', '#login_password', function (e) {
        if (e.keyCode == 13) {
          login_req()
        }
    })

})(jQuery);
