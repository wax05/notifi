function login(id,pw) { //ajax post
    var postdata = {
        'id':id, 'password':pw
    }
    $.ajax({
        type: 'POST',
        url: '/notifi/login',
        data: JSON.stringify(postdata),
        dataType : 'JSON',
        contentType: "application/json",
        success: function(data){
          var login = data.login;
          var id_ture = data.id;
          console.log(login);
          if (login == true) {
            location.replace('/notifi/user');
          } if (login == false) {
            if (id_ture == true) {
            alert('비밀번호가 맞지않습니다');
            } else{
            alert("아이디가 맞지 않습니다")
            }
          }
        },
        error: function(request, status, error){
          alert('에러가 발생했습니다')
        }
    });
  };

  function get_user_data() {
    var id = $('#user_id').val();
    var password = $('#password').val();
    var postdata = {
        'id':id, 'password':password
    }
    return postdata;
  };

  $(".user_input").keydown(function(e) {
          if (e.keyCode == 13) {
            var return_data = get_user_data();
            login(return_data.id,return_data.password);
          }
      });

  //로그인 버튼 누를때
  $('#login').click(function(){
    var return_data = get_user_data();
    login(return_data.id,return_data.password);
  });